# Release note examples

Read these examples with [the writing guidance](writing.md#release-notes-and-change-explanations). They illustrate relevance, purpose, and proportionate detail; they do not prescribe a fixed number of headings or bullets for every release.

## Start with the reader's purpose

A release note should answer a practical question: what can we now do, what obstacle has gone away, or what choice has become easier? Explain the change at that level before naming the implementation.

The following examples paraphrase the intent of Self-hosted LiveSync's historical notes in current English. They are editorial examples, not current feature, setup, or recovery instructions. The original wording and historical conditions remain in the [0.23 and 0.24 release history](https://github.com/vrtmrz/obsidian-livesync/blob/1.0.44/docs/releases/legacy.md).

| Historical example | Reader's purpose and a suitable way to express it | What to retain |
|---|---|---|
| 0.23.0: Object Storage synchronisation | 'We can synchronise using our own Object Storage, giving us another way to host and control our data.' | Explain the practical choice and its purpose. Follow with the relevant limitations, such as the cost of the first transfer, rather than leading with the storage architecture. |
| 0.23.5: configuration mismatch detection | 'Configuration mismatches are checked before synchronisation to prevent failed transfers and wasted storage.' | Connect the check to the problem it helps us avoid; include the setting or default when it affects adoption. |
| 0.24.19: QR configuration transfer | 'We can transfer the configuration to another device using a QR code.' | Put the task before the mechanism. Explain how to use it and, where applicable, the security limitation. |
| 0.24.22: Fetch while keeping local files | 'We can Fetch the remote database while keeping local files intact.' | Put preservation of the reader's work first. Explain the option and subsequent merge or conflict handling underneath. This is a historical example, not a present-day Fetch guarantee. |
| 0.24.11: selectable messages on mobile devices | 'We can copy and share messages more easily on mobile devices.' | Name the useful activity; selecting text is the method which enables it. |

The useful precedent is the connection to the reader's work, not the historical grammar, every old claim, or a requirement to use 'we' in every sentence. Preserve the repository's established voice.

## Better and weaker entries

The weaker examples below are illustrative alternatives, not quotations from published notes.

| Weaker | Better | Why |
|---|---|---|
| 'Added a QR-code generator.' | 'We can transfer the configuration to another device using a QR code.' | Names the task the feature enables. |
| 'Refactored the conflict queue.' | 'A queued conflict check no longer gets stuck waiting for a response to an outdated comparison of the same file.' | Explains the observed problem and correction. |
| 'The journal receiver now preserves content and revisions correctly.' | 'Files containing a raw unit separator are no longer truncated when received through S3-compatible Object Storage.' | Identifies the affected files, operation, and failure; avoids promoting ordinary internal invariants into separate benefits. |
| 'Improved synchronisation reliability.' | 'We can continue CouchDB synchronisation after rebuilding an encrypted remote when **Use Internal API** is enabled.' | Gives the operation and conditions under which the improvement matters. |
| 'Fixed damaged files.' | 'New transfers no longer truncate affected files. Copies already damaged require recovery from a verified intact source.' | Distinguishes prevention from repair and retains the required action. |
| 'Removed the old cleanup implementation.' | 'Recovery from old cleanup locks is now unified around the standard recovery dialogue.' | Leads with the supported workflow; explain the retired operation and recovery precautions underneath. |
| A list of library names, versions, and internal changes | 'Updated dependencies.' under `Miscellaneous` | Gives routine maintenance proportionate space when no further user-facing explanation is needed. |
| A separate feature description for an upstream utility the application does not use | Omit that utility. Describe any relevant application effect briefly and acknowledge the contribution where appropriate. | Keeps scope tied to the released product and its readers. |

The concise dependency style also appears in 0.24.27 ('Some dependencies have been updated to the latest version.') and 0.23.21 (`Miscellaneous`: 'Dependency updated.'). Preserve that restraint while using current spelling and grammar. If a dependency update fixes a concrete product problem, explain that problem under the appropriate change type instead of burying it in a generic maintenance summary.

## Choosing structure and length

- Put `Fixed`, `Improved`, or other applicable change types above feature groups. Introduce feature subsections only where they help readers find a change; small releases may need just a heading and a few bullets.
- Separate a distinct audience, such as CLI users, when their changes would otherwise be difficult to find. Do not copy the same explanation into every section.
- Put useful instructions and significant conditions beneath the outcome. Ordinary fixes may need only one sentence. Recovery, changed defaults, and compatibility changes may need more detail.
- Separate author motivation from the change list. A maintainer-supplied introduction can explain why a broader change was undertaken; it does not replace concrete outcomes. Preserve the maintainer's tone and strength of claim rather than making uncertainty or reflection sound decisive. Do not invent a personal note.
- For a retired path, use `Sunset` where appropriate and explain the supported replacement. Follow the repository's established headings if it uses different terminology.
- Preserve issue references and acknowledgements at the level needed to trace the relevant change. Do not infer the purpose or classification from the implementation alone.

# Published sample: Self-hosted LiveSync 1.0.44

This is a frozen example from the [published 1.0.44 notes](https://github.com/vrtmrz/obsidian-livesync/blob/1.0.44/updates.md). It demonstrates concise fixes, a fuller recovery entry, a separate CLI audience, restrained miscellaneous items, and acknowledgements. The introduction was supplied by the maintainer. Its length and recovery precautions are specific to this release, not minimum requirements for other notes.

The text below is preserved from the approved published notes; the relative recovery link is expanded to its tagged source so it works outside the product repository. Treat this as historical evidence, not a maintained recovery guide.

---

## 1.0.44

1st November, 2026

Recently, I have been concentrating on maintenance and improvements to individual features. I began to wonder whether I had been focusing a little too closely on the details and could give more attention to the overall picture. That led me to a somewhat broader round of changes, including reworking parts of the architecture. Along the way, I was able to bring several implementations of the same concepts together, introduce shared abstractions, and tidy up the codebase a little.

Please let me know if any problems arise from these changes.

### Fixed

#### Synchronisation

- Files containing a raw unit separator (`U+001F`) are no longer truncated when received through S3-compatible Object Storage. (#1303)
    - Update every participating client to prevent further truncation. Updating alone does not repair copies already damaged.
    - Before recovery, preserve verified intact copies, unique unsynchronised edits, and any required history, then follow the [recovery procedure](https://github.com/vrtmrz/obsidian-livesync/blob/1.0.44/docs/recovery.md#recover-files-truncated-during-object-storage-reception).
    - Rebuild and Fetch leave Hidden File Sync and Customisation Sync disabled. Initialise them deliberately after ordinary file recovery is complete.

- We can continue CouchDB synchronisation after rebuilding an encrypted remote when **Use Internal API** is enabled. (#1234)
    - Cached responses encrypted with the previous Security Seed no longer interfere with subsequent reads.

#### Conflict resolution

- A queued conflict check no longer gets stuck waiting for a response to an outdated comparison of the same file.

#### Hidden File Sync and Customisation Sync

- Newer local hidden files are no longer omitted when initialising Hidden File Sync with `Merge`.
- Refreshing the Customisation Sync catalogue no longer brings back outdated items from an earlier scan.

### Improved

#### Hidden File Sync

- We can review the latest hidden-file revisions when changes arrive during a manual JSON comparison.
    - The earlier comparison closes, and the latest revisions are checked again. If another device has resolved the conflict, the comparison closes without asking for another selection.

### Sunset

#### Recovery

- Recovery from old cleanup locks is now unified around the standard recovery dialogue, including on devices using the legacy IndexedDB adapter.
    - Use Fetch to reconstruct the local database from the remote, unlock the device when both databases are already aligned, or dismiss the dialogue.
    - These choices replace the legacy in-place `Cleanup` operation. Garbage Collection V3 remains available.
    - Before Fetch, preserve unsynchronised work and any required local history, as it replaces the local database.

### CLI

#### Fixed

- We can continue using the reconstructed database after CLI `fetch` or `rebuild`, avoiding the empty-database restart and file deletion reported in #1304.
    - Subsequent commands retain the selected database even without `--write-settings`. Interrupted reconstruction blocks ordinary synchronisation until recovery.
    - Older runtime state with no recorded owner requires explicit reconstruction from a verified source. Back up unique edits before choosing Fetch or Rebuild.

- The CLI mirror starts correctly on Windows when the Vault path is omitted and the database directory is also used as the Vault.

### Miscellaneous

- Installation and update downloads are smaller.
- Database initialisation handles encrypted change notifications more reliably. (Commonlib #191)

### Acknowledgements

Thank you for your contributions!

- @AdrianNicu, for improving decryption handling during database initialisation (Commonlib #191).
