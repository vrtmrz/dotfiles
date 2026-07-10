# dotfiles

Public, version-controlled personal configuration.

## Managed files

- `codex/AGENTS.md`: global guidance for Codex across repositories.

## Installation

Clone the repository, then run:

```sh
./install.sh
```

The installer links `codex/AGENTS.md` to `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`. If a different file already exists at the destination, the installer preserves it as a timestamped backup.

## Security

Only intentionally public configuration belongs in this repository. Do not commit credentials, authentication files, shell history, logs, session data, private repository details, or machine-specific secrets.
