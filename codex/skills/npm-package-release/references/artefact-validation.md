# Published artefact validation

- Validate the exact published registry version rather than a local pack, workspace link, or rebuilt source tree.
- Use representative consumers and include clean installation, builds, focused automated tests, and a real-runtime smoke test when UI or platform-adapter behaviour is involved.
- Where validation requires the published artefact, keep publication, real-environment validation, dist-tag promotion, and merging into the main branch as separate checkpoints.
- Keep the release pull request in draft and the main branch unchanged until the required validation succeeds.
- Regenerate and verify externally consumed release-time artefacts, such as package metadata, generated type definitions, manifests, and scanner inputs.
- Before requiring real-runtime or device validation, distinguish consumer-owned behaviour covered by mocks or injected tests, unchanged framework or kit behaviour guaranteed by upstream contracts and end-to-end tests, and device-specific integration which remains unverified.
- Prefer explicit injectable boundaries when designing APIs and tests so consumer behaviour can be verified independently without duplicating upstream test suites.
- Report local-source results, exact-registry-artefact results, and real-runtime confirmation as separate evidence.
