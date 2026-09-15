# Contributing

Edit shared guidance in `codex/AGENTS.md`, agent definitions in `codex/agents/`,
and reusable skills in `codex/skills/`. Keep private configuration and session
records outside this repository.

## Installer validation

Run the shell syntax check and the focused installer tests:

```sh
bash -n install.sh
python3 -m unittest discover -s tests -v
```

The tests use temporary home and configuration directories. They cover agent
file installation, permissions, backup preservation, repeated installation,
private-guidance composition, and skill links without changing the normal
installed configuration.

After changing an agent definition, validate its TOML syntax and confirm the
intended model, reasoning effort, and access settings. Installation checks do
not measure model behaviour or token use; assess those separately with
representative tasks when changing agent instructions.
