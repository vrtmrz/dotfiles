---
name: obsidian-plugin-release
description: Prepare, review, validate, publish, or promote Obsidian plug-in releases. Use for BRAT pre-releases, Community Directory review, scanner and official ESLint constraints, manifest and version consistency, GitHub Release promotion, release notes, or Obsidian-specific runtime validation; do not use for ordinary feature development with no release-readiness work.
---

# Obsidian plug-in releases

Apply shared Obsidian release policy without replacing the repository's own release runbook.

## Workflow

1. Read the applicable `AGENTS.md` files and the repository release runbook, such as `docs/releasing.md`, before proposing or performing release work.
2. Establish the current stage: readiness review, pre-release preparation, published-artefact validation, stable promotion, or Community Directory review.
3. Identify the exact version, commit, tag, GitHub Release, manifests, and derived artefacts in scope. Keep proposed, published, validated, and promoted state distinct.
4. Load only the references needed for the stage:
   - Read [release-lifecycle.md](references/release-lifecycle.md) for version metadata, BRAT pre-releases, promotion, immutable releases, and runtime-validation boundaries.
   - Read [community-directory.md](references/community-directory.md) for scanner scope, build and lint ordering, listing delays, or directory administration.
   - Read [release-notes.md](references/release-notes.md) when drafting or reviewing release notes.
5. If the work also publishes an npm package, use `$npm-package-release` for the registry publication and dist-tag portion.
6. Run focused local checks before any protected operation, then report completed evidence, remaining real-environment validation, and the next approval gate separately.

## Boundaries

- Start with the release runbook and the release candidate, package, or plug-in currently in scope. Keep repository exploration bounded; inspect unrelated packages, implementation files, or workflows only when a stated dependency or validation risk requires them.
- Let the repository runbook own exact commands, paths, automation names, and project-specific verification. Keep cross-repository policy here.
- Verify current external scanner, directory, and platform behaviour from authoritative sources when a decision depends on it; do not rely on a remembered implementation detail.
- Do not infer permission to push, publish, tag, promote, merge, close, or change Community Directory administration from permission for another operation.
- Do not weaken production review by suppressing findings or relocating production source into ignored development paths.
