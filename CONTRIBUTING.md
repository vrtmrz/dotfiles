# Contributing

Edit shared guidance in `codex/AGENTS.md` and `codex/guidance/`, agent definitions
in `codex/agents/`, and reusable skills in `codex/skills/`. Keep private
configuration and session records outside this repository.

## Installer validation

Run the shell syntax check and the focused installer tests:

```sh
bash -n install.sh
python3 -m unittest discover -s tests -v
```

The tests use temporary home and configuration directories. They cover public
agent definitions and guidance files, permissions, backup preservation,
repeated installation, composition with an existing `AGENTS.private.md`, skill
links, and preservation of unrelated files in the guidance namespaces. They do
not change the normal installed configuration.

After changing an agent definition, validate its TOML syntax and confirm the
intended model, reasoning effort, and access settings. Installation checks do
not measure model behaviour or token use; assess those separately with
representative tasks when changing agent instructions.
