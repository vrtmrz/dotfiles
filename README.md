# dotfiles

Public, version-controlled personal configuration.

## Managed files

- `codex/AGENTS.md`: global guidance for Codex across repositories.

## Installation

Clone the repository, then run:

```sh
./install.sh
```

By default, the installer links `codex/AGENTS.md` to `${CODEX_HOME:-$HOME/.codex}/AGENTS.md`. If `${CODEX_HOME:-$HOME/.codex}/AGENTS.private.md` exists and is non-empty, the installer instead generates `AGENTS.md` from the public guidance followed by that private supplement. Run the installer again after changing either source.

Codex only reads one global guidance file, so this generated composition keeps intentionally public defaults separate from private, machine-local preferences. If a different file already exists at the destination, the installer preserves it as a timestamped backup.

## Security

Only intentionally public configuration belongs in this repository. Keep `AGENTS.private.md` outside the repository, and do not commit credentials, authentication files, shell history, logs, session data, private repository details, or machine-specific secrets.
