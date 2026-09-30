<p align="center">
    <img src="https://goauthentik.io/img/icon_top_brand_colour.svg" height="150" alt="authentik logo">
</p>

---

[![](https://img.shields.io/discord/809154715984199690?label=Discord&style=for-the-badge)](https://discord.gg/jg33eMhnj6)

# authentik Version info

This repo holds the version info for the authentik built-in version check. This allows us to publish security-relevant updates without publishing the code which might expose vulnerabilities.

## Bumping a version

This repo is also a composite GitHub Action that bumps a product's version file (`versions/<product>/<major>/<family>.json` and `versions/<product>/latest.json`, plus the legacy `version.json` for `authentik` itself) and opens a pull request with the change. Call it from the product's release workflow:

```yaml
- name: Bump version
  uses: goauthentik/version@main
  with:
    product: authentik # or e.g. authentik-agent
    new-version: "2026.8.4"
    changelog-url: "https://docs.goauthentik.io/releases/2026.8/#fixed-in-202684" # optional
    reason: bugfix # bugfix | feature | security | other
    token: ${{ steps.app-token.outputs.token }} # needs push access to this repo
    commit-author: "my-app[bot] <id+my-app[bot]@users.noreply.github.com>" # optional
```

`changelog-url` is optional: products without a docs release-notes page yet (e.g. `platform`) can omit it and the `changelog`/`changelog_url` fields are left empty.
