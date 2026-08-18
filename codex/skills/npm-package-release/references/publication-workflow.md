# npm publication workflow

## Separate operations

- Treat release preparation, pushing, pull-request creation, staged-publication approval, registry publication, and dist-tag promotion as separate operations.
- Preserve explicit human gates for release-note review, runtime or consumer validation, publication, tagging, promotion, and merging.
- Prefer manually dispatched automation for deterministic release-pull-request preparation, including version metadata, checks, the release commit, and a draft pull request.

## Staging and publication

- Before approving a staged package, confirm its package name, version, registry access, dist-tag, trusted actor or provenance, and checksum.
- Keep pre-releases on a pre-release dist-tag such as `next`; do not promote them to `latest`.
- When a trusted staged-publishing workflow sends every release to `next`, publish a stable version there first, validate the exact registry artefact, and promote that same version to `latest` as a separate operation.
- After publication, compare the registry version, checksum, provenance where available, and dist-tags with the reviewed stage.
- If publication or validation fails after a version is public, leave that version immutable and prepare a new patch or otherwise valid successor version.
