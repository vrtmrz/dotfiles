# Obsidian Community Directory review

## Scanner and build scope

- Treat the Community Directory scanner's repository scope as independent from Git, ESLint, and TypeScript exclusions.
- Before relying on an ignored path or file extension for tests, mocks, generated files, documentation, translations, or build tooling, inspect the current scanner list and use an exact recognised name.
- Keep the first root package script recognised by the scanner as the production plug-in build. Do not repurpose it as an aggregate monorepo or development build.
- Do not assume the production build runs before source lint. If type-aware review needs generated inputs, use only an audit-stage installation mechanism explicitly supported by the current scanner; `prebuild`, `build`, and `postbuild` are not substitutes when source lint precedes the build.

## Official review

- Run the official Obsidian ESLint plug-in locally, but treat remote Community Directory review as authoritative for actual file scope, dependency resolution, and current rule versions.
- Correct production findings rather than hiding them with suppression directives or by moving production source into an ignored development location.
- When a directory entry appears missing or stale, distinguish automated-review failure from documented indexing or README refresh delays. Request the directory's manual release check once before publishing another version solely to refresh the listing.

## Directory administration

- Treat a published Community Directory identifier as immutable.
- Require explicit maintainer approval and a documented user-impact assessment before changing an identifier, payment classification, archive state, ownership, or other directory administration.
