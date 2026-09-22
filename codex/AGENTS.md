# Task-specific guidance

- The core rules below apply throughout the task. Detailed Markdown guidance is read on demand; these files are not automatically imported. Resolve the guidance root as `${CODEX_HOME:-$HOME/.codex}/guidance`. Use the public or private subdirectory shown in each reference.
- Read applicable files before their triggering action. Re-evaluate when the task changes or resumes after handover. Reuse current guidance already read; do not load all files by default.
- If a required file is missing or unreadable, report the exact path, recover it from its owning source where authorised, and pause only work that depends on it. Continue independently authorised work. Pass applicable paths and requirements to subagents.

| Before this work | Read under the guidance root |
|---|---|
| Drafting or editing repository documentation, code comments, product text, handovers, commit messages, or PR/issue text; pushing changes containing documentation or user-facing text | `public/writing.md` |
| Naming a branch; preparing a commit, PR, or issue; updating public progress; performing a Git or release operation that changes remote state | `public/git-workflow.md` |
| Starting or assigning work to a subagent, or coordinating ongoing agents and command/CI waits | `public/delegation.md` |
| Creating a worktree; preparing a handover, session transition, or worktree cleanup; designing a repeated operational inspection | `public/handovers.md` |

# Language and identifiers

- Follow the repository's required language for documentation and product text, or the requested artefact language; otherwise use the repository's established primary language.
- For English prose, use British `-ise`/`-isation` spellings, the Oxford comma, logical punctuation, single quotation marks unless the format requires otherwise, and no contractions. Detailed writing guidance applies before the tasks listed above.
- Preserve existing code identifiers and exact API, protocol, command-line, and interface spellings. New identifiers follow the surrounding module's established conventions; do not impose prose spelling on code or rename an interface merely to make it British English.

# Task progress and design changes

- Continue work authorised by the user's request and earlier approvals. Make routine implementation decisions within the established scope and design, stating material assumptions when useful.
- When a design has been agreed with the user or presented as the basis for implementation, explain any necessary change, its reason, and its effect on behaviour, compatibility, and scope. Obtain the user's agreement before implementing that change. Approval of the original design does not authorise a revised design.
- Investigation needed to assess a possible design change and work independent of that change may continue within existing authorisation. Pause the work that depends on the unresolved decision.
- Before requesting approval for an operation subject to a user checkpoint, complete the preparation already authorised and present a concrete, reviewable target. Preparation must remain within the agreed or declared design. Identify the affected files or logical change groups, their purpose, and the uncommitted changes included in the operation; a file count alone is insufficient.

# Coordination and approval prompts

- Approval wording and signal tokens apply only when input is needed; they create no new approval gates and do not cancel existing authorisation.
- At a checkpoint, state the current position, what will be done and why, exact targets and revisions, and how to respond. Explain where action is needed, what resumes work, and which later operations remain paused.
- Ask naturally in prose. Use bullets for targets or alternatives when helpful. Give each requested action a short, distinct response word.
- For browser/device authentication, identify the paused operation and reason, URL, one-time code, scopes when available, resume reply, and later sensitive operations still paused. After confirmation, promptly verify authentication and the external operation; replace expired authentication URLs.

# Protected changes and durable state

- Preserve existing user changes and other agents' work. Keep edits within the authorised scope and ownership boundaries.
- Respect explicit user checkpoints before pushing, creating pull requests, approving staged publication, publishing, tagging, promoting releases or dist-tags, merging, or closing. Approval for one action is not approval for a later action.
- Keep canonical handovers, required patches, and evidence outside project worktrees and temporary directories. Before cleanup, verify that their saved contents and links suffice to resume work. Read the handover guidance before creating worktrees or preparing cleanup.
- Keep credentials, private service details, and personal task records out of public repositories and guidance.

# Search scope and evidence retrieval

- Start in the task's repository/worktree and exact supplied evidence paths. Follow imports, manifests, runtime resolution, or explicit references to the particular dependency, related repository, or artefact needed. Before broadening, state the missing evidence and additional location; an authorised read needs no extra approval.
- Discover dependency source paths through package metadata, package-manager resolution/cache information, or supplied checkouts before searching contents. Verify the selected version matches the behaviour under investigation.
- Avoid recursive content searches over home roots, repository/worktree collections, agent state, conversation histories, or shared temporary roots. Search an exact task-relevant directory. Explicitly requested history/environment investigations may inspect scoped records. Read applicable AGENTS and selected skills normally, including in active worktrees inside agent state directories.
- For numerous matches, obtain filenames or counts first, then bounded excerpts. Limit lines and width; parse JSON/JSONL into selected fields. Narrow truncated output instead of requesting more raw data.
- Discover tools with matching names and short descriptions first; inspect only definitions needed next.

# Defect handling

- Before changing production code for a defect, add the smallest practical automated regression test. Run it against the unmodified implementation and confirm failure for the expected behaviour; dependency, fixture, permission, and environment failures are setup problems.
- Fix only after reproducing the defect, then rerun that test and broader checks proportionate to risk and scope.
- If automated reproduction is genuinely impractical, document why and define repeatable manual reproduction and verification before editing; report the coverage limitation.
- When changing an expectation, explain how the original fixture maps to the agreed behaviour and retain coverage of that scenario with behavioural assertions.
- A passing rerun alone proves no fix. Record the initial failure, rerun revision and conditions, and remaining uncertainty; distinguish a demonstrated fix from an unreproduced failure.

# Delegation and validation

- Use Luna agents when bounded delegation saves time or keeps noisy intermediate work out of the main context and its benefit exceeds coordination cost. Keep small tasks local when that is simpler.
- The user makes final design, architecture, and scope decisions. The main agent develops proposals, assesses trade-offs, coordinates implementation, and owns integration. Keep ambiguous cross-cutting analysis and high-risk integration assessment in the main agent.
- `luna_explorer` is read-only investigation and `luna_worker` is implementation within clear requirements and ownership; both use their configured `max` effort. Use `luna_lookup` or `luna_worker_light` at `medium` only for named sources or files, a known result or exact transformation, and an existing verification method. A small diff alone does not qualify. Read `public/delegation.md` before assigning work.
- Complete required repository validation. After it passes, broaden or repeat checks only for changed code, a failure, or a named unresolved risk. Avoid duplicate investigations and reviews that cannot change a decision.
- Parallel implementation requires disjoint ownership and validation responsibilities. Run broad or memory-intensive validation one process at a time across all agents and worktrees.

# Local paths

- Prefer repository-relative paths when referring to files in a repository. Use a machine-specific absolute path only when it is necessary to identify a local target unambiguously in direct coordination with the user.
- Do not put machine-specific absolute local paths into committed content. Replace them with repository-relative paths, placeholders, or portable discovery instructions, as appropriate.

# Maintaining shared configuration

- Edit the owning sources: `codex/AGENTS.md`, `codex/guidance/`, `codex/agents/`, and `codex/skills/` in the public configuration repository. Run its `./install.sh` after changes; installed agent and guidance files are copies.
- Keep private guidance, skills, and service details in their owning private repository. Keep private agent names distinct from public ones, with one source of truth for each installed definition.
