# LabNotes

## Purpose and scope

- Maintain one canonical Markdown LabNote for substantive, multi-step investigation, design, implementation, or review. Use it to preserve the purpose, decisions, evidence, current progress, and next action across context compaction and sessions. Routine questions and small, self-contained edits need no new note.
- Reuse an existing task note or handover where practical. A LabNote can serve as the canonical handover; keep one source of current task state. It complements the established task tracker and does not authorise external task or issue creation.
- Use `assets/labnote-template.md` in the installed `labnote` skill (normally `{{SKILLS_ROOT}}/labnote/`). Read the template when creating a note, and initialise it with known facts and explicit pending states before substantial exploration. Use the task's requested language. Keep sample implementations and measurements out of real notes unless independently established.

## Location and ownership

- Follow the configured permanent LabNote location and naming convention. Apply the external-record requirements in [handovers.md](handovers.md) and applicable private location guidance. Keep personal working records outside public repositories and the development worktrees they document. A separately selected private archive stores snapshots; preparing one does not move the active note.
- Give the active main session responsibility for the canonical note. Pass its exact path to subagents and new sessions. Subagents return their findings and evidence to its owner rather than concurrently rewriting the same note.
- Give independently accepted follow-up work its own note, linked from the parent. Continue using the existing note when a new session continues the same objective.

## Environment and working context

- Record the owning session, known related sessions, explicit device ID, OS and architecture, and execution route such as host, sandbox, or container. State relevant observed restrictions and unknowns. These describe the environment at the recorded time; they do not grant access or authorise later operations.
- Identify the repository or source, the main working copy or linked worktree, its branch and HEAD or other revision, and protected local changes. Associate portable paths such as `~/dev/...` or paths relative to configured roots with the recorded device ID. Put additional repositories and execution environments in a concise body table when needed.
- On resuming, identify the exact note or verified saved copy, map its recorded paths to the current device, and inspect the actual repository identity, worktree, revision, local changes, and permissions before acting. Retain previous session and environment information as dated evidence; update the current context only after checking it.

## Content

- Put `# --- PROGRESS` immediately after the title. Include the last update, owner and related sessions, recorded device and environment, target, worktree and revision where applicable, protected local changes, pending decisions or approvals, preservation state, resume source, and a short checklist with one explicit next action. Link separate work rather than copying its history.
- Give checklist entries stable identifiers such as `[P01]` after their checkboxes. Retain those identifiers when reordering entries. Use the `labnote` skill's `list`, `mark`, and `comment` helper for repeated progress operations; changes to decisions or validation conditions also require corresponding body updates.
- Keep Abstract to three lines and Main Purpose to one line. Label the main purpose `[MP]` and normally at most three sub-purposes `[SP-1]`, `[SP-2]`, and `[SP-3]`, each on one line. Explain necessary exceptions. Link material choices, risks, changes, tests, and conclusions to the relevant purpose labels.
- Leave no unexplained blanks. Distinguish `Not reached` (the relevant stage has not yet been reached; include a brief reason, prerequisite, or condition for reaching it), `not started` (the stage or task is already applicable but its action has not begun), `not verified` (verification is outstanding), unknown (factual evidence is missing), `N.A.` (outside agreed scope, with a reason), and `N.P.` (considered, nothing particular). Use `not yet considered` for a question or option that has not been examined, not as a stage marker. `Not reached` does not prescribe a universal phase order; in Japanese notes, use `未到達` for this marker. A pending state is a valid entry and does not itself require stopping authorised work.
- Before declaring the work complete, review every required, in-scope section. None may remain `Not reached`: replace the marker with supported evidence, or replace it with an explicit description of the unfinished work and keep the task marked incomplete. Do not fabricate completion evidence.
- Separate observations, hypotheses, expected outcomes, and verified results. Identify the status of decisions: proposed, agreed, pending, or superseded. Record reasons for design changes and the relevant agreement before dependent implementation.
- For validation, record the target revision or artefact, conditions, commands, results, and evidence links. Preserve initial failures and their resolution. Keep detailed logs and historical evidence in linked attachments rather than copying them into the active note.
- Record useful decision rationales and alternatives, not a transcript of the conversation or internal deliberation. Keep acknowledgements factual and positive; credit actual contributions without inventing participants, feelings, results, or approval.

## Preservation at session end or handover

- Keep the local Markdown note as the canonical working record during the task. At an agreed session end, interruption, or handover, refresh its current position, necessary evidence, and next action, then follow the destination and scope already chosen by the user or an applicable standing policy. Ordinary progress updates and compaction do not publish a record.
- A Notion article supports reading and knowledge capture. Git preservation retains the selected Markdown snapshot and necessary attachments for later inspection or continuation. Use both when both purposes are requested; local continuation can use the existing note without an external save. Ask only when an unresolved destination or scope is needed to proceed.
- Distinguish a prepared copy, a local commit, and a remotely saved and verified record. Respect the current authorisation and any publication checkpoint; a stored plan or a completed earlier approval does not authorise another upload or push.
- For Git, use the configured private archive and preserve the note's root-relative identity and sibling evidence links. Select only the intended notes and attachments. Keep device-local session pointers, lock files, caches, and credentials out of the archive. Existing non-portable content needs a reviewed portable copy before publication; retain the original and describe any transformation rather than claiming an exact copy.
- After verifying a remote save, record its URL or repository, path, and immutable commit, together with the captured source's update time and SHA-256. State whether the result is a readable article or an unchanged file snapshot, and identify missing evidence. Adding the save reference to the local note is a subsequent change and is not part of the already captured source hash.

## Updating and resuming

- Update affected sections when the objective, scope, decision, implementation, validation, blocker, or approval state materially changes, and before a planned compaction, interruption, session transfer, or completion report. Save incrementally instead of waiting until the context window is nearly full.
- Patch changed sections and checklist items rather than regenerating the whole document after each command. Keep completed work concise, retain open work, and preserve superseded decisions as clearly dated history when they explain the current choice.
- After saving, read back the changed sections. Keep the exact canonical path in the active task state and handover. Report a failed save and use the recovery guidance while preserving the previous note.
- Surface the canonical path when the note is created or ownership changes. If the path is lost, recover its reference from the current task's supplied handover or scoped session messages; do not guess from an unrelated recent note.
- After compaction or resuming, first read PROGRESS, then the sections and evidence needed for the next action. Check the target revision, protected changes, prerequisites, and pending approvals before acting. Recover a specific gap from the named sources instead of rereading the entire conversation by default.
- Instructions alone cannot guarantee a model-written update immediately before every automatic compaction. A separately configured and tested lifecycle hook can check saved state; document what it checks and whether failure stops compaction. Do not claim that such enforcement is active until it is installed and tested.
