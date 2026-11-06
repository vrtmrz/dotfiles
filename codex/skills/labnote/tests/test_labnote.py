import contextlib
import io
import json
import multiprocessing
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import labnote


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "labnote.py"
BASE_NOTE = (
    "# Note\n"
    "# --- PROGRESS\n"
    "Updated: old\n"
    "- [ ] [P02] second task [SP-2]\n"
    "- [ ] [P01] first task [MP]\n"
    "## Implementation\n"
    "Keep this body unchanged.\n"
)


def simultaneous_comment(note, barrier, queue, text):
    original = labnote.read_snapshot
    first = True

    def coordinated_snapshot(path):
        nonlocal first
        result = original(path)
        if first:
            first = False
            barrier.wait(timeout=10)
        return result

    labnote.read_snapshot = coordinated_snapshot
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        result = labnote.main(['comment', str(note), 'P01', text])
    queue.put((result, stderr.getvalue()))


class LabnoteCliTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.directory = Path(self.tempdir.name)

    def write_note(self, content, name="note.md"):
        note = self.directory / name
        note.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
        return note

    def invoke(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(argument) for argument in arguments)],
            capture_output=True,
            text=True,
            check=False,
        )

    def call_main(self, *arguments):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = labnote.main([str(argument) for argument in arguments])
        return result, stdout.getvalue(), stderr.getvalue()

    def test_reordered_ids_update_only_the_selected_checkbox_and_progress_timestamp(self):
        note = self.write_note(BASE_NOTE)
        os.chmod(note, 0o640)
        result = self.invoke("mark", note, "P01", "done")
        self.assertEqual(result.returncode, 0, result.stderr)

        content = note.read_text(encoding="utf-8")
        lines = content.splitlines()
        self.assertIn("- [ ] [P02] second task [SP-2]", lines)
        self.assertIn("- [x] [P01] first task [MP]", lines)
        self.assertRegex(lines[2], r"^Updated: \d{4}-\d\d-\d\dT.*\+00:00$")
        self.assertEqual(content.split("## Implementation\n", 1)[1], "Keep this body unchanged.\n")
        self.assertEqual(stat.S_IMODE(note.stat().st_mode), 0o640)

    def test_mark_todo_clears_a_completed_checkbox(self):
        note = self.write_note("# Note\n# --- PROGRESS\n- [X] [P02] completed task\n")
        result = self.invoke("mark", note, "P02", "todo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("- [ ] [P02] completed task", note.read_text(encoding="utf-8"))

    def test_list_json_reports_file_order_and_ignores_fenced_examples(self):
        note = self.write_note(
            "# Note\n"
            "```markdown\n"
            "# --- PROGRESS\n"
            "- [ ] [P99] example task\n"
            "```\n"
            "# --- PROGRESS\n"
            "- [x] [P02] second task [SP-2]\n"
            "- [ ] [P01] first task [MP]\n"
            "- [ ] [P100] long ID task\n"
            "## Body\n"
            "- [ ] [P88] not progress\n"
        )
        result = self.invoke("list", note, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "tasks": [
                    {"id": "P02", "state": "done", "text": "second task [SP-2]"},
                    {"id": "P01", "state": "todo", "text": "first task [MP]"},
                    {"id": "P100", "state": "todo", "text": "long ID task"},
                ]
            },
        )

    def test_unknown_duplicate_and_missing_section_errors_leave_note_bytes_untouched(self):
        cases = [
            ("unknown", BASE_NOTE, ("mark", "P90", "done")),
            (
                "duplicate",
                "# Note\n# --- PROGRESS\n- [ ] [P01] first\n- [ ] [P01] repeat\n",
                ("mark", "P01", "done"),
            ),
            ("missing", "# Note\n- [ ] [P01] outside progress\n", ("mark", "P01", "done")),
        ]
        for label, content, command in cases:
            with self.subTest(label=label):
                note = self.write_note(content, f"{label}.md")
                before = note.read_bytes()
                before_mtime = note.stat().st_mtime_ns
                result = self.invoke(*command[:1], note, *command[1:])
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(note.read_bytes(), before)
                self.assertEqual(note.stat().st_mtime_ns, before_mtime)
                self.assertFalse(list(self.directory.glob(f".{note.name}.*.labnote.tmp")))
                self.assertFalse(note.with_name(note.name + ".labnote.lock").exists())

    def test_task_without_stable_id_is_reported_instead_of_silently_omitted(self):
        note = self.write_note("# Note\n# --- PROGRESS\n- [ ] task without an ID\n")
        before = note.read_bytes()
        result = self.invoke("list", note, "--json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing a stable ID", result.stderr)
        self.assertEqual(note.read_bytes(), before)

    def test_multiline_comments_are_appended_as_quoted_text_without_creating_tasks_or_headings(self):
        note = self.write_note(
            "# Note\n"
            "# --- PROGRESS\n"
            "Updated: old\n"
            "- [ ] [P01] task [SP-1]\n"
            "- [ ] [P02] next task [MP]\n"
            "## Scope\n"
            "Body.\n"
        )
        first_stamp = "2026-11-06T12:00:00+00:00"
        second_stamp = "2026-11-06T12:01:00+00:00"
        with mock.patch.object(labnote, "timestamp", side_effect=[first_stamp, second_stamp]):
            result, stdout, stderr = self.call_main(
                "comment", note, "P01", "first result\n# fake heading\n\n- [ ] [P99] fake task"
            )
            self.assertEqual(result, 0, stderr)
            result, stdout, stderr = self.call_main(
                "comment", note, "P01", "second result"
            )
            self.assertEqual(result, 0, stderr)

        lines = note.read_text(encoding="utf-8").splitlines()
        self.assertIn("Updated: " + second_stamp, lines)
        self.assertIn("  > Comment (" + first_stamp + "):", lines)
        self.assertIn("  > Comment (" + second_stamp + "):", lines)
        self.assertLess(lines.index("  > Comment (" + first_stamp + "):"), lines.index("  > Comment (" + second_stamp + "):"))
        self.assertIn("  > # fake heading", lines)
        self.assertIn("  > - [ ] [P99] fake task", lines)
        self.assertIn("- [ ] [P01] task [SP-1]", lines)
        self.assertIn("- [ ] [P02] next task [MP]", lines)
        listed = json.loads(labnote.list_command(note, as_json=True))
        self.assertEqual([task["id"] for task in listed["tasks"]], ["P01", "P02"])

    def test_crlf_unicode_bom_and_missing_final_newline_are_preserved(self):
        content = (
            "\ufeff# 日本語のノート\r\n"
            "# --- PROGRESS\r\n"
            "Updated: old\r\n"
            "- [ ] [P01] 検証を確認する [MP]\r\n"
            "## 本文\r\n"
            "最後の行"
        )
        note = self.write_note(content)
        result = self.invoke("comment", note, "P01", "結果を記録\n次の行")
        self.assertEqual(result.returncode, 0, result.stderr)

        updated = note.read_bytes()
        text = updated.decode("utf-8")
        self.assertTrue(text.startswith("\ufeff# 日本語のノート\r\n"))
        self.assertNotIn(b"\n", updated.replace(b"\r\n", b""))
        self.assertFalse(text.endswith("\r\n"))
        self.assertIn("  > 結果を記録\r\n  > 次の行\r\n## 本文", text)
        self.assertIn("## 本文\r\n最後の行", text)

    def test_comment_at_eof_adds_only_the_separator_newline(self):
        note = self.write_note("# Note\n# --- PROGRESS\n- [ ] [P01] task")
        result = self.invoke("comment", note, "P01", "one\ntwo")
        self.assertEqual(result.returncode, 0, result.stderr)
        content = note.read_text(encoding="utf-8")
        self.assertTrue(content.endswith("  > one\n  > two"))
        self.assertNotIn("task  > Comment", content)

    def test_blank_comments_are_rejected_without_rewriting(self):
        note = self.write_note(BASE_NOTE)
        before = note.read_bytes()
        result = self.invoke("comment", note, "P01", " \n\t ")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(note.read_bytes(), before)

    def test_idempotent_mark_does_not_rewrite_or_touch_updated_field(self):
        note = self.write_note(
            "# Note\n# --- PROGRESS\nUpdated: keep this value\n- [x] [P01] task\n"
        )
        before = note.read_bytes()
        before_stat = note.stat()
        with mock.patch.object(labnote, "atomic_replace", side_effect=AssertionError("rewrite")):
            result, stdout, stderr = self.call_main("mark", note, "P01", "done")
        self.assertEqual(result, 0, stderr)
        self.assertEqual(stdout.strip(), "P01 is already done")
        self.assertEqual(note.read_bytes(), before)
        self.assertEqual(note.stat().st_ino, before_stat.st_ino)
        self.assertEqual(note.stat().st_mtime_ns, before_stat.st_mtime_ns)

    def test_list_is_read_only_and_creates_no_lock_or_temp_file(self):
        note = self.write_note(BASE_NOTE)
        entries_before = sorted(item.name for item in self.directory.iterdir())
        note_mtime = note.stat().st_mtime_ns
        directory_mtime = self.directory.stat().st_mtime_ns

        result = self.invoke("list", note)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("P02  todo  second task [SP-2]", result.stdout)
        self.assertEqual(sorted(item.name for item in self.directory.iterdir()), entries_before)
        self.assertEqual(note.stat().st_mtime_ns, note_mtime)
        self.assertEqual(self.directory.stat().st_mtime_ns, directory_mtime)

    def test_injected_replace_failure_preserves_original_and_cleans_temp_file(self):
        note = self.write_note(BASE_NOTE)
        before = note.read_bytes()
        before_mtime = note.stat().st_mtime_ns
        with mock.patch.object(labnote.os, "replace", side_effect=OSError("injected failure")):
            result, stdout, stderr = self.call_main("mark", note, "P01", "done")
        self.assertEqual(result, 2)
        self.assertIn("injected failure", stderr)
        self.assertNotIn("Traceback", stderr)
        self.assertEqual(note.read_bytes(), before)
        self.assertEqual(note.stat().st_mtime_ns, before_mtime)
        self.assertFalse(list(self.directory.glob(f".{note.name}.*.labnote.tmp")))

    def test_detected_concurrent_change_is_not_overwritten(self):
        note = self.write_note(BASE_NOTE)
        original = labnote.read_snapshot
        reads = 0
        human_edit = b"# Human edit\n"

        def read_with_intervening_edit(path):
            nonlocal reads
            reads += 1
            if reads == 3:
                note.write_bytes(human_edit)
            return original(path)

        with mock.patch.object(labnote, "read_snapshot", side_effect=read_with_intervening_edit):
            result, stdout, stderr = self.call_main("mark", note, "P01", "done")
        self.assertEqual(result, 2)
        self.assertIn("changed before replacement", stderr)
        self.assertEqual(note.read_bytes(), human_edit)
        self.assertFalse(list(self.directory.glob(f".{note.name}.*.labnote.tmp")))

    @unittest.skipUnless(os.name == 'posix', 'POSIX process-lock validation')
    def test_simultaneous_cli_writers_retain_the_first_save_and_report_the_conflict(self):
        note = self.write_note(BASE_NOTE)
        context = multiprocessing.get_context('fork')
        barrier = context.Barrier(2)
        queue = context.Queue()
        children = [context.Process(target=simultaneous_comment, args=(note, barrier, queue, text))
                    for text in ['writer alpha', 'writer beta']]
        try:
            for child in children:
                child.start()
            for child in children:
                child.join(timeout=15)
                self.assertFalse(child.is_alive(), 'CLI writer did not finish')
                self.assertEqual(child.exitcode, 0)
            results = [queue.get(timeout=2) for _ in children]
            self.assertEqual(sorted(code for code, _ in results), [0, 2])
            self.assertTrue(any('changed before the update began' in error for _, error in results))
            saved = note.read_text()
            self.assertEqual(saved.count('Comment ('), 1)
            self.assertEqual(('writer alpha' in saved) + ('writer beta' in saved), 1)
            self.assertIn('- [ ] [P01] first task [MP]', saved)
        finally:
            for child in children:
                if child.is_alive():
                    child.terminate()
                    child.join()
            queue.close()
            queue.join_thread()


if __name__ == "__main__":
    unittest.main()
