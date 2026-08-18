# Obsidian release lifecycle

## Release identity and metadata

- Keep `package.json`, the lockfile, `manifest.json`, and `versions.json` consistent.
- Record every released plug-in version in `versions.json`, including versions whose `minAppVersion` is unchanged.
- Regenerate and include externally consumed release-time artefacts, such as package metadata, generated type definitions, manifests, and scanner inputs. Verify them in the release pull request.
- Identify the exact reviewed commit, version, immutable tag, GitHub Release, and packaged artefact before publication.

## Pre-release and promotion

- When automated coverage is sufficient for users, an `x.y.z` version and immutable tag may initially be published as a GitHub pre-release for BRAT installation.
- Keep the release pull request in draft and the main branch unchanged while published-artefact or real-environment validation remains.
- After validation, remove the pre-release designation and make that exact GitHub Release the latest stable release before merging its reviewed commit into the main branch.
- Confirm the promotion succeeded. Community Directory review may reject a stable manifest version while its matching GitHub Release remains a pre-release.
- If validation fails, leave the published tag and release identity unchanged and prepare the next patch version.

## Validation boundaries

- Before requiring real-runtime or device validation, distinguish:
  1. consumer behaviour and failure paths covered by mocks or injected tests;
  2. unchanged framework or kit behaviour covered by upstream contracts and end-to-end tests; and
  3. device-specific integration which remains unverified.
- Do not repeat upstream real-device testing without a remaining consumer-owned risk.
- When designing APIs and tests, prefer explicit injectable boundaries so consumer-owned behaviour can be verified without duplicating framework or kit test suites.
- State whether a result is locally expected, verified against the exact published artefact, or confirmed in a real Obsidian instance.
