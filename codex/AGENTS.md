# Documentation audiences

- Decide who a statement is for before adding it to a repository, and keep these audiences separate:
  - **Users:** root and package `README.md` files explain how to use the project, supported behaviour, and stable operational constraints.
  - **Developers:** `CONTRIBUTING.md` and developer documentation explain architecture, implementation details, validation, and release work.
  - **Agents:** `AGENTS.md` records working rules and repository-specific constraints needed to perform changes safely.
- Do not copy incidental local diagnostics, handover state, or agent-only reasoning into user or developer documentation unless that audience gains a durable, actionable benefit from it.

# Documentation language and style

- Write repository documentation and user-facing text in British English (BrE), unless a repository-specific rule requires another variety of English. Use traditional British spellings, including `-ise` and `-isation` rather than `-ize` and `-ization`.
- Use the serial (Oxford) comma in lists of three or more items.
- Use logical punctuation: place commas, full stops, and other punctuation outside quotation marks unless they are part of the quoted material.
- Prefer single quotation marks in general prose. Use double quotation marks where the format or context requires them, such as JSON.
- Avoid contractions in documentation and user-facing text: write `do not`, `cannot`, and `is not` rather than `don't`, `can't`, and `isn't`.
- Prefer clear affirmative wording, especially in instructions, labels, and questions. Avoid negative questions or controls whose `yes` or `no` response may be ambiguous in translation.
- Follow the terminology and spelling established by a technology or interface where they are idiomatic or exact. Preserve code identifiers, command-line options, API names, product names, proper nouns, and verbatim quotations; for example, use `color` for the CSS property. In general prose, prefer `dialogue`; retain `dialog` in code or established technical names.
- Use the BBC News style guide as a reference when the preferred British English form is unclear.
