# dotfiles

Public, version-controlled personal configuration.

## Managed files

- `codex/AGENTS.md`: core global guidance for Codex across repositories.
- `codex/guidance/`: detailed guidance read when its task conditions apply.
- `codex/agents/`: reusable GPT-6 Luna agent definitions.
- `codex/skills/`: reusable, user-scoped Codex skills which are safe to publish.

## AI-assisted maintenance

I use OpenAI Codex to help maintain my projects, with GPT-6 Sol at `xhigh` or
`max`, or GPT-6 Astra, as the main agent. This repository publishes the shared
guidance and GPT-6 Luna subagent definitions used in that workflow. I make the
final design decisions. The main agent develops design proposals, analyses
options and trade-offs, and coordinates implementation and integration within
the agreed design. Luna agents carry out bounded investigations and implementation tasks.

| Agent | Purpose | Reasoning effort | Access |
|---|---|---|---|
| `luna_explorer` | Investigation, diagnosis, and evidence for design decisions | `max` | Read-only |
| `luna_worker` | Defined implementation work and focused validation | `max` | Workspace-write |
| `luna_lookup` | Direct factual retrieval from named sources | `medium` | Read-only |
| `luna_worker_light` | Exact mechanical changes in named files | `medium` | Workspace-write |

The standard Luna agents use `max`. The lighter agents use `medium` when the
source or file scope, expected result, and verification method are already
clear. Work requiring diagnosis, compatibility judgement, or design analysis
goes to a standard agent or the main agent. Small tasks may stay with the main
agent when delegation would add unnecessary coordination.

The shared guidance limits searches to relevant sources and makes additional
investigation depend on a specific unresolved question. Agents report decisive
evidence and remaining uncertainty, and project-specific validation requirements
still apply.

## Installation

Clone the repository, then run:

```sh
./install.sh
```

By default, the installer copies the TOML files under `codex/agents/` into
`${CODEX_HOME:-$HOME/.codex}/agents/` as regular files with mode `600`. It links
each directory under `codex/skills/` into `$HOME/.agents/skills/`. It also links
`codex/AGENTS.md` to `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`. If
`${CODEX_HOME:-$HOME/.codex}/AGENTS.private.md` exists and is non-empty, the
installer instead generates `AGENTS.md` from the public guidance followed by
that private supplement. The installer also copies `codex/guidance/*.md` into
`${CODEX_HOME:-$HOME/.codex}/guidance/public/` with mode `600`. Run it again
after changing core or detailed guidance, an agent definition, or a skill. Start
a new Codex session to load updated global guidance and agent definitions.

This generated composition keeps intentionally public defaults separate from
private, machine-local preferences. If a different file or skill path already
exists at a destination, the installer preserves it as a timestamped backup.
Identical installed agent files are retained, and agent files with other names
are left in place. Keep private custom agents under distinct names so that each
installed definition has one source of truth.

Edit the source files in this repository, then rerun the installer. The installed
agent and guidance copies are not the source of truth. See [CONTRIBUTING.md](CONTRIBUTING.md)
for installer validation.

## Conditional guidance

The core `AGENTS.md` contains the reading conditions for each detailed file.
The files are ordinary Markdown: Codex reads them when the instructions call
for them, rather than importing their contents automatically at startup.

| File under `codex/guidance/` | Read before |
|---|---|
| `writing.md` | Documentation, comments, product text, or publication text |
| `git-workflow.md` | Branch naming, commit/PR/issue preparation, or remote Git operations |
| `delegation.md` | Assigning subagents or coordinating agents and command waits |
| `handovers.md` | Worktree creation, handovers, cleanup, or repeated operational inspections |

Core approval, scope, preservation, language, and validation rules remain
active throughout the task. Code identifiers follow existing module and API
conventions; British English prose rules do not require renaming them.
Task handovers and required attachments belong in a durable external location
accessible from every worktree. Creating a worktree alone does not require a
new handover.

Private detail files use the separate `guidance/private/` namespace. The public
installer leaves that namespace and unrelated files untouched. A missing
required detail file is reported before the dependent work proceeds; authorised
independent work can continue.

## Security

Only intentionally public configuration belongs in this repository. Keep `AGENTS.private.md` outside the repository, and do not commit credentials, authentication files, shell history, logs, session data, private repository details, or machine-specific secrets.
