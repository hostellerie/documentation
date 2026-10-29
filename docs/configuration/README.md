# Geeklog configuration reference

> **Work in progress.** This is a documentation migration scaffold, **not** the complete reference. Refer to the configuration documentation shipped with your Geeklog release for the authoritative options.

## Configuration locations

Geeklog administers most settings through its **Configuration** administration panel. Some settings, including database/bootstrap configuration, are retained in files such as `db-config.php` and `siteconfig.php`. The precise behavior should be checked against the target release.

## Context-sensitive help

The Core configuration UI constructs help URLs ending in `config.html#desc_<option>` when a tooltip override is not used. The install support page `configinfo.php` also builds links to the `desc_` fragments.

Examples of anchors that must remain valid in the final generated HTML:

<a id="desc_site_url" name="desc_site_url"></a>

### site_url

The site's base URL. For required formatting and default values, use the currently shipped configuration reference for your Geeklog release.

<a id="desc_site_name" name="desc_site_name"></a>

### site_name

The site's display name. See the released configuration reference for details.

## Compatibility contract

- Preserve the URL `public_html/docs/english/config.html`, and every existing named fragment identifier before any replacement.
- Retain plugin-local help documents and language fallback behavior where relevant.
- Source documentation contains **450 anchor occurrences (449 unique names)**. Preserving only the two examples above is insufficient.
- Duplicate historical anchor name `users_comments` requires a deliberate migration decision.
- Do not republish incomplete settings descriptions as complete documentation.

See the current [Core config.html](https://github.com/Geeklog-Core/geeklog/blob/master/public_html/docs/english/config.html) and [configuration code](https://github.com/Geeklog-Core/geeklog/blob/master/system/classes/config.class.php).
