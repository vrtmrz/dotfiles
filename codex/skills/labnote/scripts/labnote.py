"""Safely inspect and update checklist progress in an explicit LabNote."""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import json
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, Sequence

try:
    import fcntl
except ImportError:  # pragma: no cover - exercised on Windows only
    fcntl = None

try:
    import msvcrt
except ImportError:  # pragma: no cover - exercised on POSIX only
    msvcrt = None


class LabnoteError(Exception):
    """An expected input, format, or conflict error."""


class ConflictError(LabnoteError):
    """The note changed while a write was being prepared."""


@dataclass(frozen=True)
class Snapshot:
    data: bytes
    identity: tuple[int, ...]
    mode: int


@dataclass(frozen=True)
class Section:
    start: int
    end: int


@dataclass(frozen=True)
class Task:
    id: str
    state: str
    text: str
    line_index: int
    checkbox_index: int
    comment_indent: int


FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
ATX_HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+.*|[ \t]*)$")
PROGRESS_HEADING_RE = re.compile(r"^ {0,3}#[ \t]+---[ \t]+PROGRESS[ \t]*$")
SETEXT_RE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
CHECKBOX_ITEM_RE = re.compile(
    r"^[ \t]*(?:[-*+]|[0-9]+[.)])[ \t]+\[[ xX]\](?:[ \t]+|$)"
)
TASK_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<marker>[-*+]|[0-9]+[.)])[ \t]+"
    r"\[(?P<state>[ xX])\][ \t]+\[P(?P<digits>[0-9]+)\]"
    r"(?:[ \t]+(?P<text>.*?))?[ \t]*$"
)
UPDATED_RE = re.compile(r"^(?P<prefix>[ \t]*Updated:[ \t]*).*$")


def split_lines(text: str) -> list[str]:
    """Split on physical CRLF, LF, or CR endings without normalising them."""
    if not text:
        return []
    lines = re.findall(r"[^\r\n]*(?:\r\n|\n|\r|$)", text)
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def line_parts(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n") or line.endswith("\r"):
        return line[:-1], line[-1:]
    return line, ""


def logical_body(lines: Sequence[str], index: int) -> str:
    body, _ = line_parts(lines[index])
    if index == 0 and body.startswith("\ufeff"):
        return body[1:]
    return body


def replace_logical_body(lines: list[str], index: int, new_body: str) -> None:
    old_body, ending = line_parts(lines[index])
    bom = "\ufeff" if index == 0 and old_body.startswith("\ufeff") else ""
    lines[index] = bom + new_body + ending


def fence_mask(lines: Sequence[str]) -> list[bool]:
    """Return which lines are outside fenced code blocks."""
    outside: list[bool] = []
    fence_char: str | None = None
    fence_size = 0

    for index, line in enumerate(lines):
        body = logical_body(lines, index)
        if fence_char is not None:
            outside.append(False)
            close = re.match(
                rf"^ {{0,3}}{re.escape(fence_char)}{{{fence_size},}}[ \t]*$",
                body,
            )
            if close:
                fence_char = None
                fence_size = 0
            continue

        outside.append(True)
        opening = FENCE_OPEN_RE.match(body)
        if opening:
            marker, info = opening.groups()
            if marker[0] == "`" and "`" in info:
                continue
            fence_char = marker[0]
            fence_size = len(marker)

    return outside


def is_setext_content(body: str) -> bool:
    if not body.strip():
        return False
    if ATX_HEADING_RE.match(body):
        return False
    if re.match(r"^ {0,3}(?:[-*+]|[0-9]+[.)])[ \t]+", body):
        return False
    if re.match(r"^ {0,3}>", body):
        return False
    if re.match(r"^ {0,3}(?:\*{3,}|-{3,}|_{3,})[ \t]*$", body):
        return False
    return True


def heading_starts(lines: Sequence[str], outside: Sequence[bool]) -> set[int]:
    headings: set[int] = set()
    for index, is_outside in enumerate(outside):
        if not is_outside:
            continue
        body = logical_body(lines, index)
        if ATX_HEADING_RE.match(body):
            headings.add(index)
        if (
            index > 0
            and outside[index - 1]
            and SETEXT_RE.match(body)
            and is_setext_content(logical_body(lines, index - 1))
        ):
            headings.add(index - 1)
    return headings


def parse_progress(lines: Sequence[str]) -> tuple[Section, list[Task], list[bool]]:
    outside = fence_mask(lines)
    progress_starts = [
        index
        for index, is_outside in enumerate(outside)
        if is_outside and PROGRESS_HEADING_RE.match(logical_body(lines, index))
    ]
    if not progress_starts:
        raise LabnoteError("missing real '# --- PROGRESS' heading")
    if len(progress_starts) != 1:
        raise LabnoteError("multiple real '# --- PROGRESS' headings")

    start = progress_starts[0]
    headings = heading_starts(lines, outside)
    end = min((index for index in headings if index > start), default=len(lines))
    section = Section(start=start, end=end)

    tasks: list[Task] = []
    seen: set[str] = set()
    for index in range(section.start + 1, section.end):
        if not outside[index]:
            continue
        body = logical_body(lines, index)
        match = TASK_RE.match(body)
        if not match:
            if CHECKBOX_ITEM_RE.match(body):
                raise LabnoteError(
                    "progress task is missing a stable ID such as [P01]"
                )
            continue
        task_id = f"P{match.group('digits')}"
        if task_id in seen:
            raise LabnoteError(f"duplicate task ID [{task_id}] in PROGRESS")
        seen.add(task_id)
        state = "done" if match.group("state").lower() == "x" else "todo"
        indent = match.group("indent")
        marker = match.group("marker")
        comment_indent = visual_indent(indent) + visual_indent(marker) + 1
        tasks.append(
            Task(
                id=task_id,
                state=state,
                text=(match.group("text") or "").rstrip(),
                line_index=index,
                checkbox_index=match.start("state"),
                comment_indent=comment_indent,
            )
        )
    return section, tasks, outside


def visual_indent(value: str) -> int:
    column = 0
    for char in value:
        if char == "\t":
            column += 4 - (column % 4)
        else:
            column += 1
    return column


def timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def replace_updated_field(
    lines: list[str], section: Section, outside: Sequence[bool], value: str
) -> None:
    for index in range(section.start + 1, section.end):
        if not outside[index]:
            continue
        body = logical_body(lines, index)
        match = UPDATED_RE.match(body)
        if match:
            replace_logical_body(lines, index, match.group("prefix") + value)
            return


def decode_note(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise LabnoteError("note is not valid UTF-8") from exc


def encode_note(lines: Sequence[str]) -> bytes:
    return "".join(lines).encode("utf-8")


def format_task_list(tasks: Sequence[Task], as_json: bool) -> str:
    if as_json:
        return json.dumps(
            {
                "tasks": [
                    {"id": task.id, "state": task.state, "text": task.text}
                    for task in tasks
                ]
            },
            ensure_ascii=False,
        )
    if not tasks:
        return "No progress tasks."
    return "\n".join(f"{task.id}  {task.state}  {task.text}" for task in tasks)


def _stat_identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
        metadata.st_uid,
        metadata.st_gid,
    )


def read_snapshot(path: Path) -> Snapshot:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise LabnoteError("note path must refer to a regular file")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read()
        after = os.fstat(fd)
        if _stat_identity(before) != _stat_identity(after):
            raise ConflictError("note changed while it was being read; retry the command")
        return Snapshot(
            data=data,
            identity=_stat_identity(after),
            mode=stat.S_IMODE(after.st_mode),
        )
    finally:
        os.close(fd)


@contextlib.contextmanager
def writer_lock(path: Path) -> Iterator[None]:
    lock_path = path.with_name(path.name + ".labnote.lock")
    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(lock_path, flags, 0o666)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise LabnoteError("sidecar lock path must refer to a regular file")
        if fcntl is not None:
            fcntl.flock(fd, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
        elif msvcrt is not None:  # pragma: no cover - exercised on Windows only
            if os.fstat(fd).st_size == 0:
                os.write(fd, b"\0")
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        else:
            raise LabnoteError("platform has no supported advisory file lock")
    finally:
        os.close(fd)


def atomic_replace(path: Path, expected: Snapshot, new_data: bytes) -> None:
    temp_path: Path | None = None
    fd: int | None = None
    try:
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".labnote.tmp", dir=path.parent
        )
        temp_path = Path(temp_name)
        with os.fdopen(fd, "wb") as stream:
            fd = None
            stream.write(new_data)
            stream.flush()
            os.chmod(temp_path, expected.mode)
            os.fsync(stream.fileno())

        latest = read_snapshot(path)
        if latest != expected:
            raise ConflictError(
                "note changed before replacement; no update was applied, retry the command"
            )

        os.replace(temp_path, path)
        temp_path = None
        if os.name != "nt":
            try:
                directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                directory_fd = os.open(path.parent, directory_flags)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError as exc:
                raise LabnoteError(
                    f"note was replaced, but the directory sync failed: {exc}"
                ) from exc
    finally:
        if fd is not None:
            os.close(fd)
        if temp_path is not None:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                pass


def resolve_note(note: str) -> Path:
    if not note.strip():
        raise LabnoteError("NOTE must be an explicit non-empty path")
    try:
        return Path(note).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise LabnoteError(f"cannot resolve NOTE path: {exc}") from exc


def write_operation(
    path: Path, transform: Callable[[bytes], tuple[bytes | None, str]]
) -> str:
    initial = read_snapshot(path)
    new_data, message = transform(initial.data)
    if new_data is None:
        return message

    with writer_lock(path):
        current = read_snapshot(path)
        if current != initial:
            raise ConflictError(
                "note changed before the update began; no update was applied, retry the command"
            )
        atomic_replace(path, current, new_data)
        return message


def list_command(path: Path, as_json: bool) -> str:
    snapshot = read_snapshot(path)
    lines = split_lines(decode_note(snapshot.data))
    _, tasks, _ = parse_progress(lines)
    return format_task_list(tasks, as_json)


def mark_transform(task_id: str, desired_state: str) -> Callable[[bytes], tuple[bytes | None, str]]:
    def transform(data: bytes) -> tuple[bytes | None, str]:
        lines = split_lines(decode_note(data))
        section, tasks, outside = parse_progress(lines)
        task = next((item for item in tasks if item.id == task_id), None)
        if task is None:
            raise LabnoteError(f"unknown task ID [{task_id}]")
        if task.state == desired_state:
            return None, f"{task_id} is already {desired_state}"

        body = logical_body(lines, task.line_index)
        replacement = "x" if desired_state == "done" else " "
        changed = (
            body[: task.checkbox_index]
            + replacement
            + body[task.checkbox_index + 1 :]
        )
        replace_logical_body(lines, task.line_index, changed)
        replace_updated_field(lines, section, outside, timestamp())
        return encode_note(lines), f"{task_id} marked {desired_state}"

    return transform


def comment_transform(task_id: str, comment_text: str) -> Callable[[bytes], tuple[bytes | None, str]]:
    if not comment_text.strip():
        raise LabnoteError("comment text must not be blank")

    def transform(data: bytes) -> tuple[bytes | None, str]:
        lines = split_lines(decode_note(data))
        section, tasks, outside = parse_progress(lines)
        task = next((item for item in tasks if item.id == task_id), None)
        if task is None:
            raise LabnoteError(f"unknown task ID [{task_id}]")

        stamp = timestamp()
        replace_updated_field(lines, section, outside, stamp)

        indentation = " " * task.comment_indent
        quote_prefix = indentation + "> "
        insert_at = task.line_index + 1
        while insert_at < section.end:
            body = logical_body(lines, insert_at)
            if body.startswith(indentation + ">"):
                insert_at += 1
            else:
                break

        newline = line_parts(lines[task.line_index])[1] or dominant_newline(lines)
        comment_lines = [
            quote_prefix + f"Comment ({stamp}):",
            *(quote_prefix + line for line in comment_text.splitlines()),
        ]
        has_final_newline = bool(lines and line_parts(lines[-1])[1])
        has_following_line = insert_at < len(lines)
        if insert_at > 0 and not line_parts(lines[insert_at - 1])[1]:
            prior_body, _ = line_parts(lines[insert_at - 1])
            lines[insert_at - 1] = prior_body + newline
        for offset, value in enumerate(comment_lines):
            if (
                offset < len(comment_lines) - 1
                or has_following_line
                or has_final_newline
            ):
                value += newline
            lines.insert(insert_at + offset, value)

        return encode_note(lines), f"Comment added to {task_id}"

    return transform


def dominant_newline(lines: Sequence[str]) -> str:
    counts = {"\r\n": 0, "\n": 0, "\r": 0}
    first_seen: list[str] = []
    for line in lines:
        ending = line_parts(line)[1]
        if ending:
            counts[ending] += 1
            first_seen.append(ending)
    if not first_seen:
        return "\n"
    max_count = max(counts.values())
    return next(ending for ending in first_seen if counts[ending] == max_count)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="labnote.py",
        description="Inspect and explicitly update a LabNote PROGRESS checklist.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="list tasks in the progress section")
    list_parser.add_argument("note", metavar="NOTE", help="explicit path to a LabNote")
    list_parser.add_argument("--json", action="store_true", help="print structured JSON")

    mark_parser = subparsers.add_parser("mark", help="change one task checkbox")
    mark_parser.add_argument("note", metavar="NOTE", help="explicit path to a LabNote")
    mark_parser.add_argument("task_id", metavar="ID", help="stable task ID, such as P02")
    mark_parser.add_argument("state", choices=("done", "todo"))

    comment_parser = subparsers.add_parser("comment", help="append a dated task comment")
    comment_parser.add_argument("note", metavar="NOTE", help="explicit path to a LabNote")
    comment_parser.add_argument("task_id", metavar="ID", help="stable task ID, such as P02")
    comment_parser.add_argument("text", metavar="TEXT", help="comment text; may contain newlines")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        path = resolve_note(args.note)
        if args.command == "list":
            print(list_command(path, args.json))
        elif args.command == "mark":
            print(write_operation(path, mark_transform(args.task_id, args.state)))
        elif args.command == "comment":
            print(write_operation(path, comment_transform(args.task_id, args.text)))
        return 0
    except (LabnoteError, OSError, UnicodeError) as exc:
        print(f"labnote: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
