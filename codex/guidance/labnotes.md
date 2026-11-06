# LabNotes

## Purpose and scope

- Maintain one canonical Markdown LabNote for substantive, multi-step investigation, design, implementation, or review. Use it to preserve the purpose, decisions, evidence, current progress, and next action across context compaction and sessions. Routine questions and small, self-contained edits need no new note.
- Reuse an existing task note or handover where practical. A LabNote can serve as the canonical handover; keep one source of current task state. It complements the established task tracker and does not authorise external task or issue creation.
- Use `assets/labnote-template.md` in the installed `labnote` skill (normally `~/.agents/skills/labnote/`). Read the template when creating a note, and initialise it with known facts and explicit pending states before substantial exploration. Use the task's requested language. Keep sample implementations and measurements out of real notes unless independently established.

## Location and ownership

- Follow the configured permanent LabNote location and naming convention. Apply the external-record requirements in [handovers.md](handovers.md) and applicable private location guidance. Keep personal task records outside public repositories and project worktrees.
- Give the active main session responsibility for the canonical note. Pass its exact path to subagents and new sessions. Subagents return their findings and evidence to its owner rather than concurrently rewriting the same note.
- Give independently accepted follow-up work its own note, linked from the parent. Continue using the existing note when a new session continues the same objective.

## Content

- Put `# --- PROGRESS` immediately after the title. Include the last update, owner/session reference, target and revision where applicable, protected local changes, pending decisions or approvals, and a short checklist with one explicit next action. Link separate work rather than copying its history.
- Give checklist entries stable identifiers such as `[P01]` after their checkboxes. Retain those identifiers when reordering entries. Use the `labnote` skill's `list`, `mark`, and `comment` helper for repeated progress operations; changes to decisions or validation conditions also require corresponding body updates.
- Keep Abstract to three lines and Main Purpose to one line. Label the main purpose `[MP]` and normally at most three sub-purposes `[SP-1]`, `[SP-2]`, and `[SP-3]`, each on one line. Explain necessary exceptions. Link material choices, risks, changes, tests, and conclusions to the relevant purpose labels.
- Leave no unexplained blanks. Distinguish `N.P.` (considered, nothing particular), `N.A.` (not applicable, with a reason when useful), unknown, not yet considered, not started, and not yet verified. A pending state is a valid entry and does not itself require stopping authorised work.
- Separate observations, hypotheses, expected outcomes, and verified results. Identify the status of decisions: proposed, agreed, pending, or superseded. Record reasons for design changes and the relevant agreement before dependent implementation.
- For validation, record the target revision or artefact, conditions, commands, results, and evidence links. Preserve initial failures and their resolution. Keep detailed logs and historical evidence in linked attachments rather than copying them into the active note.
- Record useful decision rationales and alternatives, not a transcript of the conversation or internal deliberation. Keep acknowledgements factual and positive; credit actual contributions without inventing participants, feelings, results, or approval.

## Updating and resuming

- Update affected sections when the objective, scope, decision, implementation, validation, blocker, or approval state materially changes, and before a planned compaction, interruption, session transfer, or completion report. Save incrementally instead of waiting until the context window is nearly full.
- Patch changed sections and checklist items rather than regenerating the whole document after each command. Keep completed work concise, retain open work, and preserve superseded decisions as clearly dated history when they explain the current choice.
- After saving, read back the changed sections. Keep the exact canonical path in the active task state and handover. Report a failed save and use the recovery guidance while preserving the previous note.
- Surface the canonical path when the note is created or ownership changes. If the path is lost, recover its reference from the current task's supplied handover or scoped session messages; do not guess from an unrelated recent note.
- After compaction or resuming, first read PROGRESS, then the sections and evidence needed for the next action. Check the target revision, protected changes, prerequisites, and pending approvals before acting. Recover a specific gap from the named sources instead of rereading the entire conversation by default.
- Instructions alone cannot guarantee a model-written update immediately before every automatic compaction. A separately configured and tested lifecycle hook can check saved state; document what it checks and whether failure stops compaction. Do not claim that such enforcement is active until it is installed and tested.
