# Historical Geeklog Wiki recovery — inventory and migration plan

> Status: **private archival inventory in progress; no restored SQL or extracted article text has been imported into GitHub**. This is an independent workstream from installation-documentation PR #4. All numbers below are user-provided results of local read-only inspections, not results of our own execution against the archive.

## Source provenance

Tom supplied `Geeklog_wiki-hG5d78A6hD.zip` (~197 MB), a bundle of backup pairs from 2012-09, 2012-11-14, 2022-10-02, 2024-11-02 and 2025-10-02, plus an archived caching-template-library MHTML page.

- Prefer **2024-11-02** as a candidate documentation baseline, not necessarily the final authority.
- **2025-10-02** is labeled `Spam pages most likely`; investigate changes without auto-publishing or auto-discarding everything.
- Archives include full SQL backups with potentially sensitive user, authentication, and configuration data. **Never commit entire ZIP, nested tarballs, SQL, raw user rows, credential-bearing config, or unreviewed Wiki wikitext.** Preserve the originals intact and work offline.

## Confirmed structural inventory

The local inspection found 61 SQL tables in each of the 2024 and 2025 dumps, including `page`, `revision`, `text`, `redirect`, `categorylinks`. The two dumps have the same reported relevant table definitions. The 2024 SQL inside tarball is ~33.52 MB; 2025 is ~106.63 MB.

| Metric | 2024 | 2025 |
| --- | ---: | ---: |
| Total pages | 515 | 7503 |
| Namespace 0 | 360 | 7348 |
| Other namespaces | 155 | 155 |
| Redirects within 2024 ns0 | 9 | — |

User's exact title comparison: **360 namespace-0 titles shared**, **6988 new titles in 2025**, **0 titles removed**. Comparison of the correct `page_latest` (field index 8) gave **360 of 360 unchanged revision IDs** with zero parser errors. Identical revision IDs are strong evidence that the stored newest version pointers did not change, **not proof of byte-identical old_text payloads or the absence of later malicious edits to other database fields**.

The user's 2024 CSV catalog contains **360 page rows + header**, `wiki-2024-catalogue.csv`, with columns `page_id,titre_wiki,namespace,revision_id,taille_octets,redirection,rubrique_proposee,ancien_titre_url,nouvelle_url,statut_migration`. Classification is heuristic: Administration 19, Configuration 34, Développement 35, Installation 31, Plugins 44, À classer 197. These categories do not establish quality/relevance; 9 redirects are included in totals.

The 9 ns0 redirect titles as reported: `Category:MediaWiki_User's_Guide`, `MediaWiki_User's_Guide`, `Multi-Language_Support`, `Multilanguage_FAQ_Plugin`, `Setting_up_an_account_on_cvs.geeklog.net`, `SoC_improve_multi-language_feature`, `SoC_more_Spam-X_modules`, `UnOfficial_Plugins`, `Upgrading_Hudson`. The `Category:` title was observed **in ns0**, so namespace must always be read from metadata, not inferred from the title. **Redirect targets have NOT yet been resolved from the `redirect` table.**

## First editorial candidates — **must be reviewed, not automatically published**

**Current technical documentation candidates**, to reconcile against current Geeklog 2.2.2 source and the Markdown docs already published:

- `Plugin_API`, `Plugin_APIG2`, `Plugin_Autoinstall`
- `Functions.inc_-_Listing_of_the_Plugin_Functions`, `AddToConfiguration`
- `DatabaseSchema`, `Caching_Template_Library`, `Webservices_API`
- `Multi-Site_Setup`, `Integrating_the_Comment_Engine`
- `Static_Pages_Plugin`, `Theme_Developers_Guide`, `Coding_Guidelines`, `Adding_Moderation_Capability`

**Historical / version-specific archive candidates**, not current instructions: `ConfigFile14`, `Coding_StandardsG2`, `ThemePort:step_two`, `Using_Mercurial`, `Geeklog_Release_Procedures`, Summer of Code / Google Code-in pages.

**Licensing/reuse review required** for historic content: e.g. `GNU_Free_Documentation_License` is a document title, not a blanket license permission for all recovered material. Verify actual licensing, contributors, attribution and file provenance before publication.

## Migration gates

1. **Catalog hygiene:** validate the CSV's 360 ns0 rows, nine redirects, field structure and encoding. Re-classify all 197 `À classer` only after reviewing titles and relevant content. Record `topic, era, status, source URL`.
2. **Redirection mapping:** parse only the **2024 `redirect` table** into `rd_from, rd_namespace, rd_title, rd_fragment`, join `rd_from` to `page_id`; inspect possible cross-namespace redirect semantics. Never infer destination from the redirect title.
3. **Public article extraction:** recover only public, permitted `page` / `revision` / `text` fields; join `page_latest=rev_id` and `rev_text_id=old_id`; consider MediaWiki `old_flags` and compressed storage; exclude deleted/suppressed revisions, private namespaces, user data, credentials, spam, and executable markup by default. Never run archived PHP or restore a historic wiki Web stack.
4. **Technical validation:** test every modernized code sample/API against the exact target Core release; distinguish historical instructions with prominent version warnings.
5. **Link mapping:** retain `old wiki URL → reviewed new docs URL` mappings; use safe landing pages for unmigrated topics. Do not bulk-redirect every legacy link to a generic homepage where a specific destination exists, or silently break existing Core/plugin anchors.
6. **Publication:** review content, licenses, privacy and provenance before merging into official `Geeklog-Core/documentation`. The live GitHub Pages homepage may explain the transition and point to Geeklog.net/forum separately from this archival work.

## Concrete next output

Run `tools/wiki_catalog_review.py` locally against `wiki-2024-catalogue.csv`. It will write an offline **sanitized review CSV** and print summary counts. Inspect the CSV and provide it via the conversation if help with manual classification is desired. **Do not commit raw SQL or unreviewed article text.**

Keep this branch separate from `docs/installation-release-audit-222` / PR #4; one scoped PR for Wiki recovery once verified.
