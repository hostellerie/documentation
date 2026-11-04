# Static Pages plugin — creating standalone content

> **Modernization draft.** Based on the recovered 2024 Wiki article `Static_Pages_Plugin`. The historical article covers multiple older releases; confirm the available options and permissions in the Static Pages plugin shipped with your installation.

## Purpose

The Static Pages plugin lets an authorized editor create pages outside the normal story/article publishing flow. Common uses include information pages, contact instructions and other relatively stable content.

The Wiki describes page IDs, placement in topic or index views, page cloning, access permissions, URLs and autotags. These capabilities may vary by plugin version, so consult the installed version's administration screen and bundled documentation.

## Create and maintain a page

1. Sign in with an account authorized to administer Static Pages.
2. Open the installed plugin's administration screen.
3. Set a descriptive page title and an appropriate page ID, if editable.
4. Add the content, review its access permissions, and save.
5. Check the page with a public account or logged out to verify expected visibility.
6. Confirm links, navigation and appearance on mobile devices.

Do not give authors broader plugin or PHP-execution permissions than their tasks require.

## PHP execution is a security-sensitive historical feature

The Wiki notes that PHP execution in static pages was disabled by default in older plugin versions, with separate rights and configuration. **Do not enable execution of arbitrary PHP merely to reproduce a historic tutorial.** Prefer plain content, approved plugins and safe template features. If a current deployment supports PHP in page content, restrict its use to trusted administrators and verify the exact security model with the target plugin release.

## Before publishing or upgrading

- Verify visibility and ownership permissions.
- Review any embedded scripts and external resources.
- Test URL/autotag behavior and navigation.
- Check whether content depends on a legacy plugin configuration key.
- Back up the site before changing plugin versions.

**Source provenance:** recovered `Static_Pages_Plugin` from the 2024-11-02 Geeklog Wiki. Specific interface labels and settings require version verification.
