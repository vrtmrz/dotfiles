---
name: npm-package-release
description: Prepare, stage, publish, validate, or promote npm package releases. Use for release pull requests, trusted or staged publication, provenance and checksum review, registry artefact validation, pre-release and stable dist-tags, consumer verification, or publication failure recovery; do not use for ordinary dependency installation or unreleased package development.
---

# npm package releases

Apply shared npm release policy while leaving exact commands and repository-specific mechanics to the local runbook.

## Workflow

1. Read the applicable `AGENTS.md` files and repository release runbook before proposing or performing release work.
2. Establish the current stage: preparation, push or pull request, staged-publication review, registry publication, exact-artefact validation, or dist-tag promotion.
3. Record the exact package name, version, source revision, registry, access, requested dist-tag, trusted actor or provenance, and available checksum.
4. Load only the references needed:
   - Read [publication-workflow.md](references/publication-workflow.md) for staged publication, operation boundaries, dist-tags, and post-publication reconciliation.
   - Read [artefact-validation.md](references/artefact-validation.md) for exact registry artefact, consumer, and runtime validation.
5. Perform all authorised local preparation and focused checks before the next protected operation.
6. Report the completed stage, exact artefact identity, verification evidence, unresolved risks, and next approval gate separately.

## Boundaries

- Start with the release runbook and the release candidate, package, or plug-in currently in scope. Keep repository exploration bounded; inspect unrelated packages, implementation files, or workflows only when a stated dependency or validation risk requires them.
- Let the repository runbook own exact commands, paths, workflow names, supported consumers, and project-specific checks.
- Treat preparation, remote state changes, registry publication, validation, and promotion as distinct states; do not describe a prepared release as published or a published release as validated.
- Do not infer approval to push, create a pull request, approve a staged package, publish, tag, promote a dist-tag, merge, or close from approval for another operation.
- Do not overwrite or reuse a published version. Prepare a new version after a failed published release.
