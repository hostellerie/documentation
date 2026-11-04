# Fast path to an accessible Geeklog Wiki archive

The original 2024 Wiki dump is available only on the contributor's Chromebook, not in this repository. Do not commit or publish the archive, SQL, passwords, user tables, or all 360 pages without review.

## Release strategy

1. **Local read-only preview**: select 14 technical articles using `page_latest → revision.rev_text_id → text.old_id` and generate static HTML with escaped raw wikitext. This verifies extraction without executing a historical MediaWiki install. The initial preview is **not** a full wikitext renderer and is **not yet suitable for public documentation**.
2. **Expand coverage**: run the same local extraction for 351 non-redirect historical namespace-0 articles, keeping 9 redirects in a separate mapping. Review content for private information, outdated instructions and licensing. Resolve 2024 redirect targets via `redirect.rd_from` and page ID. The 155 non-main-namespace records need independent selection, not automatic release.
3. **Public searchable legacy snapshot**: once reviewed, publish safe static archival pages under a versioned `legacy-wiki/` URL with prominent historical status, navigation, cross-page links, and search/index, preserving historical titles where possible. Test that all outgoing links and templates are either mapped or visibly marked unsupported. Never deploy this snapshot as current instructions.
4. **Modern docs**: migrate high-value verified articles to Markdown under topic folders; keep existing Geeklog 2.2.2 HTML help URL/fragment compatibility. Prefer one Markdown source to generate both online and embedded help.
5. **Deploy**: fork publishing workflow currently checks out `prototype/dual-output-222` even if triggered from other branches; incorporate vetted legacy output into that build in a separate, reviewed change. Confirm deployment via Actions and published URL before announcing it as live.

## Current status

360 Wiki 2024 namespace-0 pages inventoried; 9 redirects. The user's CSV reviewed with 53 proposed technical-first pages; title-based classification only. Source texts have not yet been uploaded, analyzed, verified, or published. No GitHub Pages deployment is implied by this plan.

**Immediate next action**: run the separately provided local extraction utility against the ZIP and check it retrieves all 14 requested pages. Report failures of unsupported SQL formats or storage flags rather than silently dropping content.
