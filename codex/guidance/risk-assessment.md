# Proportionate defect and risk assessment

Use this guidance when the assessment could change corrective priority, a release decision, or the agreed design. Keep routine, unambiguous corrections brief. These are working weights for software maintenance, not a standard FMEA or DRBFM scale, measured probabilities, or a requirement to complete a full worksheet.

## Establish the failure and its effects

- Describe the necessary conditions, the reachable execution path, the resulting state, and the effect on the user. Separate observations, supported inference, hypothetical scenarios, and unknowns. Specification non-compliance and a failing test do not establish severe harm by themselves.
- Separate cases with different consequences. Expected conflicts, unnecessary conflicts with both versions preserved, and loss during automatic resolution are different cases. Check lifecycle ordering and prerequisites before treating a theoretical interleaving as reachable.
- Distinguish retained but temporarily unavailable information from irretrievable loss. A backup proves recoverability only for edits it actually contains. Regenerable caches and redundant internal records are not equivalent to unique user work.
- Assess the current system and its existing controls. A proposed test, a future safeguard, or the agent finding the problem is not an existing detection control. Reassess residual effects only after the relevant protection or recovery guarantee has been verified.

## Use separate severity, occurrence, and detection weights

State the scenario, exposed users or operations, assessment conditions, and evidence. Use `unknown` where an axis cannot be supported; missing evidence is not a weight of 1. The gaps between weights emphasise changes in consequence, not a measured ratio of harm or frequency.

### Severity (S)

Assess the effect if the stated scenario occurs. Emphasise preservation and recoverability of needed user information, while describing the actual interruption to work.

| Weight | Consequence |
|---|---|
| 1 | Information and normal work are preserved; effects are limited to minor overhead or verified automatic recovery. |
| 2 | All needed information is retained and ordinary, safe operations allow work to continue or the state to be restored. A manageable manual conflict or simple undo can belong here. |
| 8 | Work is substantially interrupted or a difficult restoration is required, although all affected information can be recovered from a verified source. |
| 32 | Some needed user information is irretrievably lost or corrupted. State what is lost, its extent, and the evidence for the loss. |

Manual action alone does not raise severity. Describe the number of affected items, effort, reversibility, and ability to continue work. A large volume of conflicts can cause substantial interruption; a single safe selection need not. Do not classify every operation called a deletion as irreversible loss, or every operation called a restore as difficult recovery. An old backup which lacks newer edits does not make those edits recoverable.

### Occurrence (O) and detection difficulty (D)

For occurrence, state the unit of exposure and the necessary conditions. A successful forced-crash reproduction or a short timing window does not establish the frequency in ordinary use. Keep any hypothetical frequency assumptions explicit.

For detection, state the deadline at which detection would permit a useful response, such as before an incorrect result is accepted or before harm spreads to other data or devices. Use the same deadline when comparing scenarios. Detecting an error after irretrievable loss cannot undo that loss; detection and recovery are separate claims.

| Weight | O: occurrence under the stated exposure | D: difficulty of detection by the stated deadline |
|---|---|---|
| 1 | Evidence supports an exceptional combination of conditions. | An existing control reliably detects the condition in time for a useful response. |
| 2 | Particular but realistic, limited conditions can produce the failure. | Ordinary checks make the problem apparent with time to respond. |
| 4 | Common operations or conditions produce the failure. | Detection depends on targeted comparison or investigation. |
| 8 | The failure recurs throughout ordinary use under the stated assessment conditions. | Current controls leave the condition undetected past the deadline; the problem can remain unnoticed. |

The absence of complaints is not evidence of a low occurrence weight. Novel design increases uncertainty and may identify a verification need; it is not an automatic extra multiplier. User reports inform the consequence and exposure without adding a separate complaint factor.

## Choose a proportionate response

- Where every axis has supporting evidence, `R = S * O * D` can help compare cases assessed on the same basis. Always retain the individual weights and reasons. It is not a failure probability, expected loss, or automatic release threshold; do not compute a definitive product with an unknown axis.
- Give credible irreversible information loss explicit consideration even when its product is below a frequent inconvenience. Equal products do not imply equal consequences or the same response. Distinguish a demonstrated loss from an unverified possibility.
- Verify automatic recovery against the required contents, relevant history, convergence, and retained alternatives. A completion flag or the absence of a prompt is insufficient. Describe the remaining harm after recovery separately from the original failure.
- Prefer a change which addresses the cause at its owning boundary. Distinguish cause removal, prevention, detection, containment, and recovery. Compare the remaining harm with the new failure paths, persistent state, performance cost, and maintenance burden introduced by the proposed remedy. An accepted, bounded limitation can be a proportionate outcome.
- Preserve the original scenario and its behavioural assertions when the accepted requirement changes. Record the user-approved interpretation and remaining uncertainty rather than describing a changed expectation as a production fix.

## Review ambiguity with the user

If these criteria do not clearly settle preservation, recoverability, the rating, the acceptable residual risk, or the remedy, review the ambiguity with the collaborating user before choosing the disputed interpretation or implementing a dependent change. Present the facts, missing evidence, plausible interpretations, and how the options affect behaviour and scope. Pause only the dependent decision or work; continue useful investigation and independently authorised work. Do not force a score, silently assume acceptance, or invent an additional approval gate for a clear decision already within the agreed scope.

## Calibration examples

These examples illustrate severity only; they do not establish occurrence or detection weights for a real defect.

| Scenario | Assessment |
|---|---|
| Concurrent edits produce a visible conflict as specified, with both versions available. | Expected behaviour; the conflict alone is not a defect. |
| An unnecessary conflict retains every edit and can be safely reviewed and resolved through ordinary operations. | S = 2; describe the actual effort separately. |
| An erroneous deletion retains complete information and has a safe, simple undo. | S = 2 can be appropriate; the operation's name does not establish information loss. |
| A verified source contains all affected edits, but restoration substantially interrupts work. | S = 8; recoverability and disruption both matter. |
| A backup restores yesterday's file but cannot recover today's lost edits. | S = 32 for those edits; restoration of the older file does not remove the loss. |
| Local edits remain intact but have not yet synchronised. | Assess delay or interruption; evaluate a subsequent loss path separately if evidence supports it. |
| A successful automatic merge silently discards unique edits which no retained source can recover. | S = 32; automation does not establish correctness. |
