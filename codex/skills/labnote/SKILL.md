---
name: labnote
description: Inspect and make explicit checklist updates in an existing LabNote at a specified path, using the bundled progress CLI.
---

# LabNote progress

Use the bundled CLI to inspect or update progress in an existing LabNote within the authorised task. Supply the note path every time; the CLI does not choose a recent note or infer task completion.

Run the script from the installed skill directory:

```sh
python3 "$HOME/.agents/skills/labnote/scripts/labnote.py" list /path/to/note.md
python3 "$HOME/.agents/skills/labnote/scripts/labnote.py" list /path/to/note.md --json
python3 "$HOME/.agents/skills/labnote/scripts/labnote.py" mark /path/to/note.md P02 done
python3 "$HOME/.agents/skills/labnote/scripts/labnote.py" mark /path/to/note.md P02 todo
python3 "$HOME/.agents/skills/labnote/scripts/labnote.py" comment /path/to/note.md P02 "Observed result; evidence: evidence/run.json"
```

If the skill is installed elsewhere, use that installed path. IDs are stable labels such as `P02`; keep them unchanged when reordering tasks. Use `mark` only after the task state has been decided from the work and its evidence. Use `comment` to record dated results, reasons, evidence, or explicit pending states. The script makes no semantic judgement.

The script reads and changes only the real `# --- PROGRESS` section, ending at the next Markdown heading. Tasks must be Markdown checkbox items whose text begins with a stable ID such as `[P02]`; an ID-less checkbox is a format error and the CLI does not assign IDs. The bundled template is [assets/labnote-template.md](assets/labnote-template.md).

The template records session and device references, execution environment,
repository and portable worktree identity, branch and revision, preservation
state, and the exact resume source. Follow the applicable LabNote and handover
guidance when creating or resuming a note. The progress CLI updates only the
requested checklist state or comment; it neither discovers the environment nor
archives a note. Preservation at session end follows the chosen Notion, Git, both,
or local-continuation scope and its current authorisation.

`list` is read-only and creates no lock or temporary file. `mark` and `comment` update the first existing `Updated:` field in the progress section; they do not add one. An already satisfied `mark` does not rewrite the note.

Writers coordinate through a sibling `.labnote.lock` advisory lock and check the note snapshot before replacement. This catches changes observed before replacement, but an editor that does not use the lock can still race in the brief interval after the final check. Review and resolve such edits manually. Atomic replacement preserves permission mode bits; it replaces the file inode. If syncing the containing directory fails after replacement, the CLI reports that the note was replaced but the sync was not confirmed.
