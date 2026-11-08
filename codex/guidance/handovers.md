# Repeatable operational work and handovers

- When the same multi-step inspection, comparison, or state-reconciliation sequence is repeated, identify its stable inputs, outputs, and policy checks. If the workflow is sufficiently general, replace repeated manual reconstruction with a small read-only Inspector which has documented machine-readable output, validation, and focused tests.
- Keep Inspectors read-only by default. They may gather evidence, evaluate preconditions, and emit exact proposed commands, but they must not perform protected operations, interpret inspection as authorisation, or carry an approval into a later operation.
- Keep active handovers bounded. Separate current state, accepted decisions and exclusions, durable in-scope work, protected local changes, and next approval gates from dated historical evidence. Record the base revision, prerequisite pull requests or versions, and agreed publication policy where relevant. Link to the owning project specification or runbook for durable policy rather than duplicating it. Archive superseded checkpoints; do not leave historical present-tense claims where a later agent may mistake them for current state.
- When resuming a task, read its canonical handover and the specifications or runbooks relevant to the next action. Check that prerequisite revisions and decisions still apply before implementation. Follow the named sources rather than searching conversation history by default; investigate a specific gap only when needed.
- Store handovers, patches, and evidence which must survive cleanup outside the worktrees or temporary directories being removed. Preserve the required referenced artefacts as well as the memo, update their links, and verify the saved contents and any patches needed to resume work before deleting the originals.

## LabNotes and session boundaries

- An active LabNote can be the canonical task handover. Refresh its PROGRESS, decisions, validation, and next approval gate before a transfer; preserve the same path for continuation instead of creating a second competing account of the task.
- Include the recorded session and device, execution environment, repository identity, portable worktree path, branch and HEAD, and protected local changes. Supply the exact local note or a verified preserved copy and its required evidence. The receiving session verifies its own working context; the source environment and a saved approval are historical information, not current access or authority.
- Follow the LabNote preservation choice at an agreed session end or transfer: a readable Notion article, a selected Git snapshot with attachments, both, or local continuation. Keep preparation and verified remote preservation distinct. Routine updates do not start synchronisation or archive unrelated notes.
- A change of objective or subsystem with recoverable completed work and distinct acceptance criteria is a useful session boundary. Propose a focused new session with the note and prerequisites, and continue authorised work until the user agrees. A completed phase alone does not authorise stopping or moving the remaining work.
- Keep the parent note concise when work is split: link independent notes, their owners and dependencies, and the results needed for integration. Apply [LabNote guidance](labnotes.md) when creating or updating these records.

## Worktrees and durable records

- Before creating a worktree, identify any existing task handover and a durable location outside the repository's worktrees. Creating a worktree alone does not require a new handover.
- Use one canonical handover for the task, accessible from every worktree. A handover stored only inside the project or one worktree is insufficient for work that must continue elsewhere. If a repository needs a pointer, keep durable state and required attachments in the external location.
- Resolve the destination and check that it lies outside any worktree or temporary directory scheduled for removal. Before deleting originals, verify the saved memo, linked evidence, and any patches needed to resume work. Report the canonical path when handing work over.
- Repository documentation should retain durable project knowledge; it is not the default home for personal task state. Follow the user's established external memo location when one is available.
