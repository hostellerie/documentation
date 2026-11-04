# Geeklog themes and templates

> **Modernization draft.** Consolidates recovered Wiki articles `Caching_Template_Library` and `Theme_Developers_Guide`. These pages span different Geeklog releases. Check the target release and the actual bundled theme before reusing configuration keys or code snippets.

## Overview

Geeklog uses template files to separate the presentation of a page from its PHP application logic. Themes define the site's layout and styling, while plugins can supply their own template files. The recovered Wiki describes a caching template library, multiple template search locations, variables, blocks and rendering logic.

## Working with a theme

1. Select a theme that ships with the Geeklog version you deploy.
2. Make a working copy in a staging environment. Keep a record of modified files.
3. Change one template or stylesheet at a time.
4. Check the site in logged-out and administrative views, and on narrow and wide screens.
5. Test plugin pages and views, not only the homepage.
6. Back up modifications before changing a theme or upgrading.

The legacy Wiki discusses template names such as `header.thtml`, `footer.thtml`, `blockheader.thtml`, `blockfooter.thtml` and story-body templates. **Check that these paths and names exist in your target theme**; do not assume an old theme directory structure is still current.

## Template variables, blocks and lookup paths

Templates can use variables supplied by the application. The Wiki also documents template blocks and searching multiple template locations, intended to let a site override selected files without replacing every theme template.

Verify precedence rules, default variable availability, caching and supported markup against the installed template engine before relying on these features in a new theme.

## Release-specific rendering APIs

The historical Theme Developers Guide mentions `COM_createHTMLDocument` alongside the older `COM_siteHeader` / `COM_siteFooter` approach and references legacy configuration and compatibility scripts. Their exact lifecycle and supported signatures **must be checked in the target Geeklog source**. This guide intentionally does not reproduce older compatibility JavaScript or deprecated template-engine settings as modern requirements.

## Quality and security checks

- Test generated HTML and accessibility.
- Escape untrusted dynamic values at the correct output boundary.
- Verify that cached pages do not reveal personalized or administrative content.
- Check plugin templates, responsive layout, and upgrade behavior.
- Confirm theme rendering against the target release's code and shipped themes.

**Source provenance:** 2024-11-02 recovered Wiki pages `Caching_Template_Library` and `Theme_Developers_Guide`. Licensing and technical validation pending.
