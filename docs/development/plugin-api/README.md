# Geeklog plugin API — developer guide

> **Modernization draft for Geeklog 2.2.2.** This guide consolidates the recovered Wiki articles `Plugin_API`, `Functions.inc_-_Listing_of_the_Plugin_Functions`, `Plugin_Autoinstall`, `Adding_Moderation_Capability` and `Integrating_the_Comment_Engine`. The historic names and callbacks below are leads for inspection; verify declarations and signatures in the **target version's** `system/lib-plugins.php`, each plugin's `functions.inc`, and the installation routines before publishing this as an API contract.

## How plugins integrate

Geeklog exposes core-level `PLG_*` dispatch functions. A plugin commonly implements optional callbacks named `plugin_<event>_<pluginname>` to participate in an operation. **Do not assume a one-to-one mapping**: a core dispatcher can choose more than one callback, and some events do not propagate to every plugin.

Start with [Geeklog's source](https://github.com/Geeklog-Core/geeklog). Examine the source for your **specific release**; this page is an overview, not a substitute for release-specific signatures.

## Plugin lifecycle

Historically documented callback families include:

| Area | Example callback | What to inspect |
| --- | --- | --- |
| Installation and upgrades | `plugin_autoinstall_<name>` | Required metadata and installation steps for the selected release |
| Upgrade | `plugin_upgrade_<name>` | Upgrade/version comparison and database migrations |
| Uninstallation | `plugin_uninstall_<name>` or `plugin_autouninstall_<name>` | Data cleanup semantics and administrator confirmation |
| Plugin search | `plugin_dopluginsearch_<name>` | Current search interface and access filtering |
| Moderation | `plugin_submissioncount_<name>`, `plugin_moderationapprove_<name>` | Submission queue and permissions |
| Comments | `plugin_displaycomment_<name>` | Current comment lifecycle |
| Statistics | `plugin_showstats_<name>` | Which statistics are exposed |

This table identifies **documented historical callbacks**, not confirmation that every one remains supported unchanged in Geeklog 2.2.2.

## Files and organization

Historically, plugin files reside under `plugins/<pluginname>/`, including `functions.inc`. The auto-install integration described in the old Wiki uses `autoinstall.php` in the same plugin directory. Review the plugin skeleton actually distributed with your Geeklog release before creating files.

## Installation metadata and permissions

The recovered `Plugin_Autoinstall` article describes installation metadata for plugin name, version, compatible Geeklog version and homepage, alongside optional groups, features, mappings and table registrations. If you are implementing this interface:

1. Review an actively maintained core plugin at the same release version.
2. Choose a stable internal plugin name and version.
3. Use the framework's supported setup and upgrade hooks instead of running untrusted SQL directly.
4. Declare only required permissions and groups.
5. Test installation, upgrades, enable/disable and uninstallation in a disposable environment.
6. Document whether removal preserves or deletes plugin-specific data.

**Security:** Never copy historical code samples directly into production without reviewing database permissions, input validation, output escaping, CSRF protection and access checks.

## Moderation, comments, search and templates

The Wiki describes callback families for submitted content, comments, search, and statistics. Implement only callbacks used by your chosen release. Check that each operation enforces permissions at the server, not only through hidden interface elements.

See the future dedicated guides for plugin installation, moderation and comment integration. They should reuse this page rather than duplicating API lists.

## Compatibility checklist

- [ ] API and parameters checked against the target Geeklog release
- [ ] Installation and upgrade rehearsed in staging
- [ ] All code examples tested with the target PHP/runtime
- [ ] Permission/CSRF checks reviewed
- [ ] Legacy Wiki links mapped to final anchors
- [ ] Attribution and reuse license approved

**Source provenance:** recovered 2024-11-02 Geeklog Wiki backup (titles above); actual editing and code validation remain pending.
