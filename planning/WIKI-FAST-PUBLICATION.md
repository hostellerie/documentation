# Single modern Geeklog documentation — publication plan

## Decision, 2026-11-04

**One maintained documentation, not a public legacy archive.** The historical MediaWiki backups and locally generated HTML are offline sources for content recovery only.

**One reviewed Markdown source** feeds two required outputs:
- The searchable online Geeklog documentation on GitHub Pages.
- Embedded HTML documentation for Geeklog distributions, maintaining existing `docs/english/` help URLs and anchors.

Never deploy the raw `wiki-preview-local` folder as a public alternative to the maintained documentation.

## Extraction verified on contributor's Chromebook

2024 backup: 360 namespace-0 pages, 9 redirects. Latest-revision IDs of all 360 titles agree with 2025. The local `wiki_preview.py` has successfully produced an initial 14 pages and then **351 non-redirect HTML previews** via `--all`. They contain raw, unrendered historical Wiki markup; they have **not** yet been verified or modernized.

## Migration stages

1. Select high-value pages from the 351 recovered topics: plugin API, database schema, configuration, themes, caching, Webservices, installation and admin help.
2. Extract the selected public wikitext for offline review, excluding user tables, sensitive material, and private details. Check license and attribution.
3. Compare with existing Geeklog 2.2.2 embedded docs and prototype Markdown. Merge and modernize useful content; do not bulk-import 351 outdated pages.
4. Build topic-based English Markdown, including version caveats and verified code examples; resolve all 9 Wiki redirects to their true targets for link mapping.
5. Generate **both** online and embedded HTML from the canonical Markdown. Validate existing links/anchors, site navigation, internal links, search and code snippets.
6. Publish the same documentation site incrementally. No second legacy Wiki site. Review and merge in a dedicated PR, independently of installation PR #4.

## Status and next gate

- Title-level review inventory exists; 53 proposed technical priorities, 9 redirects.
- Actual article bodies have not been received for editorial review; do not claim publication or content validation.
- The fork Pages workflow on main explicitly checks out `prototype/dual-output-222`. Updating this inventory branch alone **does not deploy** the recovered contents.

Next: collect a small, sanitized pilot set of actual public Wiki article bodies from the user's local Chromebook extraction, then convert/verify them into Markdown in the existing dual-output architecture.
