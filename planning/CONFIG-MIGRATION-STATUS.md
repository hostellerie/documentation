# Configuration migration checklist

Source: `Geeklog-Core/geeklog` master `public_html/docs/english/config.html`, blob `b726d717ab45d7232693e0537a45efe74f2a9a88` (checked 2026-10-29).

This branch starts from the documentation repo's `main`, independent of draft foundation PR #1.

- [x] Establish preliminary configuration/reference structure and two example preserved anchor names.
- [x] Flag complete legacy anchor preservation as a mandatory gate.
- [ ] Reuse the 450-anchor inventory from PR #1 after it is reviewed and merged; independently audit anchors in other docs files.
- [ ] Compare all documented settings with installed configuration groups and update paths.
- [ ] Migrate each settings table while retaining help-link compatibility.
- [ ] Test every legacy fragment on generated `config.html`, not just sample anchors.
- [ ] Test Core UI plus plugin help links against a packaged Geeklog release.
- [ ] Review generated output with Tom before replacing any Core docs.

**Non-goal:** replacing existing shipped `config.html` in this branch.
