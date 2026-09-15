# Documentation audiences

- Decide who a statement is for before adding it to a repository, and keep these audiences separate:
  - **Users:** root and package `README.md` files explain how to use the project, supported behaviour, and stable operational constraints.
  - **Developers:** `CONTRIBUTING.md` and developer documentation explain architecture, implementation details, validation, and release work.
  - **Agents:** `AGENTS.md` records working rules and repository-specific constraints needed to perform changes safely.
- Do not copy incidental local diagnostics, handover state, or agent-only reasoning into user or developer documentation unless that audience gains a durable, actionable benefit from it.

# Documentation language and style

- Write repository documentation and user-facing text in British English (BrE), unless a repository-specific rule requires another variety of English. Use traditional British spellings, including `-ise` and `-isation` rather than `-ize` and `-ization`.
- Use the serial (Oxford) comma in lists of three or more items.
- Use logical punctuation: place commas, full stops, and other punctuation outside quotation marks unless they are part of the quoted material.
- Prefer single quotation marks in general prose. Use double quotation marks where the format or context requires them, such as JSON.
- Avoid contractions in documentation and user-facing text: write `do not`, `cannot`, and `is not` rather than `don't`, `can't`, and `isn't`.
- Prefer clear affirmative wording, especially in instructions, labels, and questions. Avoid negative questions or controls whose `yes` or `no` response may be ambiguous in translation.
- Follow the terminology and spelling established by a technology or interface where they are idiomatic or exact. Preserve code identifiers, command-line options, API names, product names, proper nouns, and verbatim quotations; for example, use `color` for the CSS property. In general prose, prefer `dialogue`; retain `dialog` in code or established technical names.
- Before pushing changes which include documentation or user-facing text, review newly added prose for coined or project-specific terminology. Prefer terms already defined by the project, including any glossary or `docs/terms.md`, or explain the behaviour using established general language. Present any necessary new term, its intended meaning, audience, and affected locations to the user for review before the push.
- Exact code identifiers, established product names, standards terminology, and verbatim interface labels are not new terminology merely because they are absent from the glossary.
- Use the BBC News style guide as a reference when the preferred British English form is unclear.
- In projects with multilingual resources, keep changes to the primary-language resources and changes to their translations in separate commits and pull requests.

# Search scope and evidence retrieval

- Begin content searches in the task's repository or worktree and any exact evidence paths supplied for the task. Follow imports, dependency manifests, runtime resolution, or explicit references into the particular dependency, related repository, or artefact needed to answer the question. State the missing evidence and the specific additional location before broadening the search; this does not itself require user approval for an otherwise authorised read.
- Locate external dependency sources through package metadata, the package manager's resolution or cache information, or a supplied checkout path. Discover candidate paths before searching their contents. Verify that the selected source version matches the behaviour being investigated.
- Keep recursive content searches out of home-directory roots, collections of repositories or worktrees, agent state directories, conversation histories, and shared temporary-directory roots. Search an exact task-relevant subdirectory instead. Explicitly requested history or environment investigations may inspect the relevant records within their stated scope. Read applicable AGENTS.md files and selected skills normally; the location of an active worktree inside an agent state directory does not exclude that worktree.
- Return file names or counts first when matches may be numerous, then read bounded excerpts. Limit both line count and line width; parse JSON and JSONL into selected fields instead of printing matching records wholesale. Treat truncated output as a reason to narrow the query or extract the needed fields.
- Apply the same restraint to tool discovery: list matching tool names and short descriptions first, then inspect only the definitions needed for the next operation.

# Defect handling

- Before changing production code for a defect, add the smallest practical automated regression test that reproduces the reported behaviour.
- Run the new test against the unmodified implementation, and confirm that it fails for the expected behavioural reason. Treat dependency, fixture, permission, and environment failures as test setup problems rather than evidence that the defect has been reproduced.
- Apply the fix only after reproducing the defect, then run the same regression test to demonstrate the behaviour change. Run broader checks in proportion to the risk and scope of the change.
- If automated reproduction is genuinely impractical, document why, define a repeatable manual reproduction and verification procedure before changing the implementation, and state the remaining coverage limitation clearly.

# Repeatable operational work and handovers

- When the same multi-step inspection, comparison, or state-reconciliation sequence is repeated, identify its stable inputs, outputs, and policy checks. If the workflow is sufficiently general, replace repeated manual reconstruction with a small read-only Inspector which has documented machine-readable output, validation, and focused tests.
- Keep Inspectors read-only by default. They may gather evidence, evaluate preconditions, and emit exact proposed commands, but they must not perform protected operations, interpret inspection as authorisation, or carry an approval into a later operation.
- Keep active handovers bounded. Separate current state, durable in-scope work, protected local changes, and next approval gates from dated historical evidence. Archive superseded checkpoints, and do not leave historical present-tense claims where a later agent may mistake them for current state.

# Coordination and approval prompts

- At each user checkpoint, state the current position and briefly outline the next actions. When waiting, identify where the action is needed, what response will resume the work, and which later operations remain paused.
- Write questions and approval requests as natural prose rather than as a checklist. Use bullets for exact targets, revisions, inputs, alternatives, or decisions when they make the request easier to scan, but keep the question itself in a natural sentence.
- Present a request in this order: what will be done, what outcome it enables, which exact targets and revisions are included, and how the user should respond or act.
- Give each requested action a short, easy-to-type response word which is clearly distinct from the other choices currently offered and tersely describes the action.
- For browser or device authentication, identify the exact operation which is paused, state why authentication is needed, provide the URL, one-time code, and requested scopes when available, specify the reply which will resume work, and list later sensitive operations which remain paused. Resume promptly after confirmation, verify both the authentication result and the external operation, and issue a fresh URL when the authentication session has expired.

# Local paths

- Prefer repository-relative paths when referring to files in a repository. Use a machine-specific absolute path only when it is necessary to identify a local target unambiguously in direct coordination with the user.
- Do not put machine-specific absolute local paths into committed content. Replace them with repository-relative paths, placeholders, or portable discovery instructions, as appropriate.

# Git, pull requests, and issues

- Begin every pull request description with one concise sentence that identifies the kind of change, its purpose, and its principal effect; place the detailed summary, rationale, and verification after it.
- Choose branch names, commit messages, pull request titles, and pull request bodies for future readers. Describe the purpose and behaviour of the change, rather than the tool or agent that produced it.
- Do not include assistant or tool branding such as `codex` in branch names, commits, or pull request text unless the user explicitly requests it or the repository has an established requirement.
- Keep pull request descriptions focused on durable context: the problem, the intended behaviour, important trade-offs, and verification. Exclude incidental handover state and internal agent reasoning.
- Write pull request descriptions and issue bodies for readers who do not know the local worktrees, handover, or agent terminology. When repository history matters, describe it in ordinary terms, such as previously completed local work which was not incorporated into the integration branch. Do not use internal labels such as 'recovered work', 'checkpoint', 'slice', or handover headings as the public explanation.
- Keep maintainer-only preparation and coordination out of public pull request and issue checklists unless a public contributor must act on it. This includes requests for a personal release-note message, approval tokens, local sequencing, and private stopping rules. Translate any relevant state into a reader-facing release condition, such as remaining real-runtime validation.
- In public progress checklists, distinguish completed behaviour, genuinely remaining release work, and deferred future work. Do not present an undecided contribution or internal candidate as committed release scope.
- When verification depends on the reporter's environment, distinguish a fix that is expected to resolve an issue from one the reporter has confirmed. Leave the issue open for that confirmation unless the user or repository workflow directs otherwise.
- Respect explicit user checkpoints before remote state changes such as pushing, creating pull requests, approving staged publication, publishing, tagging, promoting releases or dist-tags, merging, or closing. Announce the intended action at the requested checkpoint, and do not treat approval for one action as approval for a later action.

# Subagent delegation

- Use the custom Luna agents proactively when delegation would materially reduce wall-clock time or keep noisy intermediate work out of the main context. Delegate only when the benefit outweighs the coordination cost; the user does not need to request delegation explicitly.
- The user makes final design, architecture, and scope decisions. The main agent develops proposals, analyses trade-offs, coordinates implementation and integration within the agreed design, and communicates with the user. Keep ambiguous cross-cutting analysis and high-risk integration assessment in the main agent.

## Role selection

- Use `luna_explorer` for bounded repository investigation, tracing, test and configuration inspection, and log analysis. Treat it as strictly read-only even if inherited runtime permissions would allow writes.
- Use `luna_worker` for straightforward implementation when the required behaviour, ownership boundary, and acceptance criteria are clear.
- Use the standard Luna explorer and worker at their configured `max` effort by default. Use `luna_lookup` or `luna_worker_light` at `medium` only when the parent can name the exact source or file scope, the expected answer or transformation, and an existing way to verify it without causal diagnosis, design decisions, or compatibility judgement. A small diff alone does not make a task light.
- Use `luna_lookup` for direct, bounded factual retrieval, selected-field extraction, and comparisons with explicit criteria. Use `luna_worker_light` for an exact mechanical change within named files. If a material ambiguity appears, return the evidence and unresolved question to the parent. The parent should reuse that evidence when assigning any deeper work.
- Handle a small lookup or edit in the main agent when delegation would add more coordination than useful independent work.

## Contracts and coordination

- Give each agent one bounded contract with the question or requirements, relevant context, and a stop condition. For implementation, specify file or module ownership, required behaviour, compatibility constraints, acceptance criteria, and focused validation.
- Default to `fork_turns="none"` and pass the required context explicitly. Use a short recent-turn fork only when necessary, and use `all` only with a stated justification.
- For diagnosis or design evidence, identify the decision to inform, the assigned behaviour, and the evidence needed to resolve the question. Trace that behaviour through the relevant entry points and effects, and check a concrete alternative or failure path that could overturn the conclusion. The agent definitions own the investigation and report format; avoid repeating them in each assignment.
- Start with one agent for each independently necessary question; delegate several questions only when their scopes are distinct and parallel execution has a concrete benefit. State the exact permitted search roots, shared evidence paths, and revision or version where relevant. If a child needs inaccessible dependency evidence, retrieve it once through an authorised route and provide the exact location.
- While an agent works, continue work outside its assigned investigation. At the dependency boundary, wait for its evidence. Verify decisive claims and integration risks without repeating the complete delegated search. Reuse evidence while its revision, environment, and other relevant assumptions remain valid.
- For an additional investigation or review, name the unresolved question, the evidence needed, and the decision that evidence could change. Prefer one focused follow-up for the same question and state. When the question or state has materially changed, pass the verified findings and remaining question to a fresh bounded agent instead of extending an unrelated investigation.
- Complete the repository's required validation. After it passes, repeat or broaden checks only for changed code, a failure, or a named unresolved risk. Do not start another review solely because the previous agent has finished or because time is available.
- Run implementation workers concurrently only when their file ownership and validation responsibilities are disjoint. Run broad or memory-intensive validation one process at a time across the parent and all agents, following the host resource limits.

# Maintaining shared guidance and agents

- Treat `codex/AGENTS.md`, `codex/agents/`, and `codex/skills/` in this repository as the sources for the shared configuration. Edit those sources and run `./install.sh`; installed agent files are copies.
- Keep private custom-agent definitions under distinct names, with one source of truth for each installed agent. Maintain private guidance and service-specific instructions in their owning private repository.
