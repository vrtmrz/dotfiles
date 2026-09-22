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

## Waiting for agents and commands

- Give every `wait_agent` call an explicit `timeout_ms` with enough time for useful progress. Use roughly twice the estimated remaining work time; use `120000` when the duration is unclear. For substantial implementation or review, `300000` or longer is appropriate when supported by the estimate.
- Agent notifications can end a wait early. Read the notification, check whether the required work is complete, and wait again when it is still running. After a timeout, update the estimate before waiting again. Keep the timeout long enough for the work; avoid shortening it merely to check status or replacing the wait with repeated `list_agents` calls or requests for progress.
- For ongoing commands and CI, normally wait `30000` to `60000` milliseconds per tool call and collect the relevant status together. Avoid repeated one-second `write_stdin` polls. Use shorter waits when interactive input or a time-sensitive response requires them.
- These durations are waiting limits, not fixed sleeps. Clamp them to the tool's supported range and any higher-priority responsiveness or progress-reporting requirements. Completion or user input should be handled promptly when the tool returns early.

## Applicable guidance in delegated work

- Include the exact applicable guidance paths and reading triggers in the child's contract, especially with `fork_turns="none"`. Pass the relevant rules directly if the child cannot access those files.
- Give a child only the guidance needed for its task. A child must read newly applicable guidance before its work enters that scope; a model upgrade or an inherited summary does not replace the actual requirements.
