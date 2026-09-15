# dotfiles

Public, version-controlled personal configuration.

## Managed files

- `codex/AGENTS.md`: global guidance for Codex across repositories.
- `codex/agents/`: reusable GPT-5.6 Luna agent definitions.
- `codex/skills/`: reusable, user-scoped Codex skills which are safe to publish.

## AI-assisted maintenance

I use OpenAI Codex to help maintain my projects. My current default main-agent
model is GPT-6 Astra. This repository publishes the shared guidance and
GPT-5.6 Luna subagent definitions used in that workflow. I make the final design
decisions. The main agent develops design proposals, analyses options and
trade-offs, and coordinates implementation and integration within the agreed
design. Luna agents carry out bounded investigations and implementation tasks.

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
that private supplement. Run the installer again after changing guidance, an
agent definition, or a skill. Start a new Codex session to load updated global
guidance and agent definitions.

This generated composition keeps intentionally public defaults separate from
private, machine-local preferences. If a different file or skill path already
exists at a destination, the installer preserves it as a timestamped backup.
Identical installed agent files are retained, and agent files with other names
are left in place. Keep private custom agents under distinct names so that each
installed definition has one source of truth.

Edit the source files in this repository, then rerun the installer. The installed
agent copies are not the source of truth. See [CONTRIBUTING.md](CONTRIBUTING.md)
for installer validation.

## Security

Only intentionally public configuration belongs in this repository. Keep `AGENTS.private.md` outside the repository, and do not commit credentials, authentication files, shell history, logs, session data, private repository details, or machine-specific secrets.
