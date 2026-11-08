# Documentation audiences

- Decide who a statement is for before adding it to a repository, and keep these audiences separate:
  - **Users:** root and package `README.md` files explain how to use the project, supported behaviour, and stable operational constraints.
  - **Developers:** `CONTRIBUTING.md` and developer documentation explain architecture, implementation details, validation, and release work.
  - **Agents:** `AGENTS.md` records working rules and repository-specific constraints needed to perform changes safely.
- Do not copy incidental local diagnostics, handover state, or agent-only reasoning into user or developer documentation unless that audience gains a durable, actionable benefit from it.
- Where a repository maintains an `Unreleased` section or another mechanism for release notes, include user-facing changes in that mechanism in the same pull request as the implementation. During release preparation, reconcile the notes with the cumulative user-facing changes since the last stable release. Include changes from intervening pre-releases which never became stable, without presenting older stable behaviour as new. Preserve historical entries and address missing changes before finalising the target notes.

# Reader benefit, notices, and diagnostics

- Identify the intended reader and the understanding, decision, or action each statement should enable. State developer benefits as such; support a claimed user benefit with an actual effect on the user's work.
- User-facing notices present a coherent account of the event relevant to the user, its consequences for the user's work, and the action the user can take. Relate these parts to the user's activity and choices, with enough context to understand the situation and act. Distinguish complete, partial, and failed outcomes, and preserve uncertainty about causes and effects. When no action is needed, state that only where it is useful and supported.
- Internal terms can help connect the relevant event, its effect on the user's work, and the next action. Use them for that explanatory purpose, with causal links where established. Naming an internal error and listing system states leaves the reader to reconstruct their practical meaning. Detailed diagnostics retain the operation, affected target, result, and remaining state or retry behaviour.
- When adapting a message for a UI, CLI, or another audience, preserve the event, outcome, affected scope, and uncertainty. Add effects on particular features, assurances about continued use, navigation paths, log locations, or retry commands only when those details are established.
- Keep recovery actions distinct from requests to collect evidence for investigation. A report request explains how to obtain the report through an available route; it does not imply that generating a report restores operation.

For a hypothetical application where a failed file scan prevents local database initialisation and the operational effect is not yet established:

- **Not good:** 'An internal error has occurred. The local database has not been initialised.' This lists what the system reports without relating it to an event relevant to the user, its practical consequences, or a useful response.
- **Good:** 'Several files could not be scanned. As a result, the local database could not be initialised. Normal operation may be affected. Please check the log for details.' This connects an event relevant to the user's activity, its possible effect on operation, and the user's next action. The internal state explains the connection; it does not stand alone as the message's purpose.

Use a more specific operational effect when it is known, and identify the log or its access route when the reader would otherwise have to guess. These are explanation criteria, not a fixed sentence count or a requirement to invent a cause or consequence.

# Recommendations and instructions

- Optional, low-risk advice is normally expressed as an impersonal statement of the recommendation, preferably with passive wording such as 'Verification is recommended'. State the useful check or benefit where it adds context. 'Verification should be recommended' instead instructs someone to make a recommendation; use it only when that is the intended meaning.
- When an action is needed to prevent concrete harm, use a clear imperative with 'please', identify the action and its timing, and explain the relevant consequence. Courtesy preserves the strength of the instruction; avoid wording which makes a necessary safeguard sound optional.
- Preserve actual requirements, approval boundaries, and required steps in a procedure, including requirements whose purpose is correctness rather than safety. This preference applies to the strength of advice and warnings; it does not convert requirements into recommendations or require passive wording throughout a procedure.

For an optional visual check of a reversible formatting change:

- **Not good:** 'Verify the preview before continuing.' This presents optional advice as a prerequisite.
- **Good:** 'A preview check is recommended to confirm the layout.' This states the recommendation and its purpose.

For a database replacement which would discard changes absent from the replacement:

- **Not good:** 'A backup is recommended before replacing the database.' This makes a necessary safeguard sound optional.
- **Good:** 'Please back up the current database before replacing it. Changes absent from the replacement would otherwise be lost.' This gives a courteous, direct instruction and explains the concrete harm.

# Release notes and change explanations

- Before drafting release notes, read [the examples and published sample](release-notes-examples.md). Use them to judge relevance and detail, while following the repository's own release format.
- Start from the reader's goal: what they want to do, what previously prevented or complicated it, and what the release now enables or resolves. A feature name, implementation change, or claim of greater robustness does not establish that purpose. If the pull request does not explain it, follow the relevant issue, design decision, or specification. Check that the implementation and verification support the claimed benefit.
- Structure substantive notes as reader outcome, how to use or obtain it when action is needed, then supporting explanation:
  1. State what the reader can now do, the problem resolved, or the supported behaviour that changes.
  2. Give any relevant operation, setting, or migration needed to obtain that result. Do not invent a user action for an automatic correction.
  3. Add the conditions, defaults, compatibility effects, remaining limitations, and precautions needed to use it correctly. Explain implementation only where it helps the reader understand the outcome or make a decision.
- Keep ordinary entries short. One clear sentence can be enough; use subordinate items for necessary methods, conditions, and precautions. Do not force every entry into three parts, repeat the outcome, or turn test assertions and ordinary correctness guarantees into additional release highlights.
- Distinguish existing behaviour, corrections, new improvements, and retired behaviour against the previous release baseline. Use change-type sections such as `Fixed`, `Improved`, and `Sunset` above feature groups where the repository has no contrary convention. Give independent audiences, such as CLI users, a separate section when this makes their changes easier to find.
- For retired behaviour, lead with the supported replacement or unified workflow, then explain what has been retired, the compatibility effects, and any action required. Do not hide removal under a vague improvement or imply that a newly removed behaviour was already unavailable.
- Keep package-consumer outcomes distinct from application end-user outcomes. For routine dependency updates with no benefit or action needing separate explanation, a single summary such as 'Updated dependencies.' under `Miscellaneous` is sufficient. Do not list every package, version, internal API, or upstream fix. When an update has a material user-visible effect, describe that effect in the relevant section, with package detail only where useful. Omit upstream changes which do not affect the released product.
- Preserve relevant issue or contribution references and acknowledgements without expanding an upstream change into an unrelated product feature. A brief, supported outcome under `Miscellaneous` can be enough; do not invent a benefit merely to justify an acknowledgement.
- Distinguish removing a cause, reducing occurrence, detecting a problem, limiting harm, and restoring use. An update which prevents new damage does not necessarily repair existing copies. Describe the scope established by the evidence rather than implying a universal guarantee.

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
