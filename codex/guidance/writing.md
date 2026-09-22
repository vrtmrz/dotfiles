# Documentation audiences

- Decide who a statement is for before adding it to a repository, and keep these audiences separate:
  - **Users:** root and package `README.md` files explain how to use the project, supported behaviour, and stable operational constraints.
  - **Developers:** `CONTRIBUTING.md` and developer documentation explain architecture, implementation details, validation, and release work.
  - **Agents:** `AGENTS.md` records working rules and repository-specific constraints needed to perform changes safely.
- Do not copy incidental local diagnostics, handover state, or agent-only reasoning into user or developer documentation unless that audience gains a durable, actionable benefit from it.
- Where a repository maintains an `Unreleased` section or another mechanism for release notes, include user-facing changes in that mechanism in the same pull request as the implementation. During release preparation, reconcile the changes included in the release with its notes and address missing entries before finalising them.

# Documentation language and style

- Write repository documentation and product text in the language required by the repository or explicitly requested for the artefact. When neither specifies a language, follow the repository's established primary language.
- Apply the following spelling, grammar, and punctuation rules to English prose. Use British English (BrE), unless a repository-specific rule requires another variety of English. Use traditional British spellings, including `-ise` and `-isation` rather than `-ize` and `-ization`.
- Use the serial (Oxford) comma in lists of three or more items.
- Use logical punctuation: place commas, full stops, and other punctuation outside quotation marks unless they are part of the quoted material.
- Prefer single quotation marks in general prose. Use double quotation marks where the format or context requires them, such as JSON.
- Avoid contractions in English prose: write `do not`, `cannot`, and `is not` rather than `don't`, `can't`, and `isn't`.
- Prefer clear affirmative wording, especially in instructions, labels, and questions. Avoid negative questions or controls whose `yes` or `no` response may be ambiguous in translation.
- Follow the terminology and spelling established by a technology or interface where they are idiomatic or exact. Preserve code identifiers, command-line options, API names, product names, proper nouns, and verbatim quotations; for example, use `color` for the CSS property. In general prose, prefer `dialogue`; retain `dialog` in code or established technical names.
- Before pushing changes which include documentation or user-facing text, review newly added prose for coined or project-specific terminology. Prefer terms already defined by the project, including any glossary or `docs/terms.md`, or explain the behaviour using established general language. Present any necessary new term, its intended meaning, audience, and affected locations to the user for review before the push.
- Exact code identifiers, established product names, standards terminology, and verbatim interface labels are not new terminology merely because they are absent from the glossary.
- Use the BBC News style guide as a reference when the preferred British English form is unclear.
- In projects with multilingual resources, keep changes to the primary-language resources and changes to their translations in separate commits and pull requests.

## Identifiers and interface terminology

- British English is a prose convention, not an instruction to rename code. Preserve existing identifiers, exported names, configuration keys, protocol fields, and external API spellings.
- For new functions, variables, types, and files, follow the naming and spelling of the surrounding module and the technology it integrates with. Use an established project convention when there is one. Do not introduce `colour` beside an existing `color` API, or rename `initialize` solely to match prose spelling.
- If the surrounding code already mixes spelling conventions, keep the change consistent with the specific interface or module being extended. Treat a broader naming clean-up as separate work, with compatibility considered explicitly.
