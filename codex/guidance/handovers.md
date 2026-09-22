# Repeatable operational work and handovers

- When the same multi-step inspection, comparison, or state-reconciliation sequence is repeated, identify its stable inputs, outputs, and policy checks. If the workflow is sufficiently general, replace repeated manual reconstruction with a small read-only Inspector which has documented machine-readable output, validation, and focused tests.
- Keep Inspectors read-only by default. They may gather evidence, evaluate preconditions, and emit exact proposed commands, but they must not perform protected operations, interpret inspection as authorisation, or carry an approval into a later operation.
- Keep active handovers bounded. Separate current state, durable in-scope work, protected local changes, and next approval gates from dated historical evidence. Archive superseded checkpoints, and do not leave historical present-tense claims where a later agent may mistake them for current state.
- Store handovers, patches, and evidence which must survive cleanup outside the worktrees or temporary directories being removed. Preserve the required referenced artefacts as well as the memo, update their links, and verify the saved contents and any patches needed to resume work before deleting the originals.

## Worktrees and durable records

- Before creating a worktree, identify any existing task handover and a durable location outside the repository's worktrees. Creating a worktree alone does not require a new handover.
- Use one canonical handover for the task, accessible from every worktree. A handover stored only inside the project or one worktree is insufficient for work that must continue elsewhere. If a repository needs a pointer, keep durable state and required attachments in the external location.
- Resolve the destination and check that it lies outside any worktree or temporary directory scheduled for removal. Before deleting originals, verify the saved memo, linked evidence, and any patches needed to resume work. Report the canonical path when handing work over.
- Repository documentation should retain durable project knowledge; it is not the default home for personal task state. Follow the user's established external memo location when one is available.
