# Subagent delegation

<!-- @only: codex -->
- Use the custom Luna agents proactively when delegation would materially reduce wall-clock time or keep noisy intermediate work out of the main context. Delegate only when the benefit outweighs the coordination cost; the user does not need to request delegation explicitly.
<!-- @end -->
<!-- @only: agy -->
- Delegate proactively when bounded execution, independent read-only auditing, or parallel investigation reduces total cost (including verification and rework), saves wall-clock time, or keeps noisy intermediate output out of the main context; the user does not need to request delegation explicitly. Keep small or straightforward lookups, searches, and local edits in the main agent by batching independent tool calls per turn.
<!-- @end -->
- The user makes final design, architecture, and scope decisions. The main agent develops proposals, analyses trade-offs, coordinates implementation and integration within the agreed design, and communicates with the user. Keep ambiguous cross-cutting analysis and high-risk integration assessment in the main agent.

## Role selection

For an independent audit, use a fresh read-only reviewer on a provider other than Antigravity, separate from the implementer. Prefer a different provider from the implementer when suitably capable. If no eligible reviewer is available, report the audit as pending, state the options, and continue independent work.

<!-- @only: codex -->
- Use `luna_explorer` for bounded repository investigation, tracing, test and configuration inspection, and log analysis. Treat it as strictly read-only even if inherited runtime permissions would allow writes.
- Use `luna_worker` for straightforward implementation when the required behaviour, ownership boundary, and acceptance criteria are clear.
- The standard Luna explorer and worker use `max`. Choose `luna_lookup` or `luna_worker_light` at `medium` when the parent can name the exact source or file scope, the expected answer or transformation, and an existing way to verify it without causal diagnosis, design decisions, or compatibility judgement. A small diff alone does not make a task light.
- Use `luna_lookup` for direct, bounded factual retrieval, selected-field extraction, and comparisons with explicit criteria. Use `luna_worker_light` for an exact mechanical change within named files. If a material ambiguity appears, return the evidence and unresolved question to the parent. The parent should reuse that evidence when assigning any deeper work.
<!-- @end -->
<!-- @only: agy -->
- Prefer a provider other than Antigravity for substantial investigation, implementation, and tests. Keep small local checks with the parent. If substantial work would need to return to Antigravity, explain why and present the available alternatives first.
- Parallel subagents and `swarm` may be launched without an explicit user request when scopes are disjoint and concurrency materially improves turnaround or review independence. Keep concurrency focused rather than fanning out speculatively (typically 2–3 concurrent subagents unless more disjoint units clearly justify it), avoid redundant review passes, and do not nest subagents unless explicitly requested. For concurrent editors use `workspace: "share"` with disjoint file ownership; for readers and auditors use `inherit`.
<!-- @end -->
- Handle a small lookup or edit in the main agent when delegation would add more coordination than useful independent work.

## Contracts and coordination

Choose the model and its supported reasoning effort separately for each assignment. A bounded fix with a known cause and a discriminating test can use an economical worker. Give deeper reasoning to the specific uncertainty, such as recovery after an interrupted write. Reassess effort once the cause is established. On repeated failure, check the requirement, evidence, and environment before increasing effort.

- Give each agent one bounded contract with the question or requirements, relevant context, and a stop condition. For implementation, specify file or module ownership, required behaviour, compatibility constraints, acceptance criteria, and focused validation.
<!-- @only: codex -->
- Set `fork_turns="none"` explicitly for each child. Write a self-contained prompt with the objective, relevant evidence, permitted actions, and required result. Ask the child to return any question that would change the scope, together with the evidence needed to decide it.
<!-- @end -->
<!-- @only: agy -->
- Subagents start in a separate conversation context by default, so pass concise context, target paths, and exact constraints directly in the prompt rather than telling the child to reread large trees of files.
<!-- @end -->
- For diagnosis or design evidence, identify the decision to inform, the assigned behaviour, and the evidence needed to resolve the question. Trace that behaviour through the relevant entry points and effects, and check a concrete alternative or failure path that could overturn the conclusion. The agent definitions own the investigation and report format; avoid repeating them in each assignment.
- Start with one agent for each independently necessary question; delegate several questions only when their scopes are distinct and parallel execution has a concrete benefit. State the exact permitted search roots, shared evidence paths, and revision or version where relevant. If a child needs inaccessible dependency evidence, retrieve it once through an authorised route and provide the exact location.
- While an agent works, continue work outside its assigned investigation. At the dependency boundary, wait for its evidence. Verify decisive claims and integration risks without repeating the complete delegated search. Reuse evidence while its revision, environment, and other relevant assumptions remain valid.
- For an additional investigation or review, name the unresolved question, the evidence needed, and the decision that evidence could change. Prefer one focused follow-up for the same question and state. When the question or state has materially changed, pass the verified findings and remaining question to a fresh bounded agent instead of extending an unrelated investigation.
- Complete the repository's required validation. After it passes, repeat or broaden checks only for changed code, a failure, or a named unresolved risk. Do not start another review solely because the previous agent has finished or because time is available.
- Run implementation workers concurrently only when their file ownership and validation responsibilities are disjoint. Run broad or memory-intensive validation one process at a time across the parent and all agents, following the host resource limits.

## Choosing the unit of work

- Keep a small task local when that is simpler. Use scripts for deterministic repeated checks and status collection. Delegate when a focused context or bounded ownership saves enough parent work to outweigh handover and integration costs; creating more agents is not itself a token-saving measure.
- Assign one child a coherent, bounded work loop. An implementation worker should carry its authorised investigation, regression test, change, and focused validation through to the agreed completion condition. Keep scope/design decisions and integration judgement with the parent and user; return those questions before dependent work proceeds. Read-only roles remain read-only.
- Keep routine commands, retries within scope, and intermediate logs inside that work loop. The parent receives concise results, exact revisions, validation and evidence paths, and unresolved matters. Request intermediate information when it can change a decision or unblock independent work, rather than coaching each command or repeating the child's investigation.
- When a new objective or subsystem has its own acceptance criteria and substantial work, propose a dedicated session or separately accepted follow-up. Supply the canonical LabNote, prerequisites, protected changes, ownership, and approval boundaries. Reuse the same note for continuation; link a separate note for independent work. Continue currently authorised work until the user agrees to a session switch.
- Reuse completed validation for the same revision, artefact, and conditions. Repeat a check for changed code, missing coverage, a failure, or a named integration risk, while preserving the required repository checks and resource limits.

## Waiting for agents and commands

<!-- @only: codex -->
- Give every `wait_agent` call an explicit `timeout_ms` with enough time for useful progress. Use roughly twice the estimated remaining work time; use `120000` when the duration is unclear. For substantial implementation or review, `300000` or longer is appropriate when supported by the estimate.
- Agent notifications can end a wait early. Read the notification, check whether the required work is complete, and wait again when it is still running. After a timeout, update the estimate before waiting again. Keep the timeout long enough for the work; avoid shortening it merely to check status or replacing the wait with repeated `list_agents` calls or requests for progress.
- For ongoing commands and CI, normally wait `30000` to `60000` milliseconds per tool call and collect the relevant status together. Avoid repeated one-second `write_stdin` polls. Use shorter waits when interactive input or a time-sensitive response requires them.
- These durations are waiting limits, not fixed sleeps. Clamp them to the tool's supported range and any higher-priority responsiveness or progress-reporting requirements. Completion or user input should be handled promptly when the tool returns early.
<!-- @end -->
<!-- @only: agy -->
- Rely on reactive wakeup for subagents and background tasks: once a subagent or background command is running, continue independent work or end the turn rather than polling `manage_subagents` or `manage_task` in a loop.
- Use `schedule` with a `TimerCondition` rather than shell `sleep` when a timed wait or periodic check is genuinely needed.
<!-- @end -->

## Applicable guidance in delegated work

<!-- @only: codex -->
- Include the exact applicable guidance paths and reading triggers in the child's contract. Pass the relevant rules directly if the child cannot access those files.
<!-- @end -->
<!-- @only: agy -->
- Include the exact applicable guidance paths and reading triggers in the child's contract. Pass the relevant rules directly if the child cannot access those files.
<!-- @end -->
- Give a child only the guidance needed for its task. A child must read newly applicable guidance before its work enters that scope; a model upgrade or an inherited summary does not replace the actual requirements.
