from json import dumps
from os import getenv
from pathlib import Path

from packaging.version import parse

INPUT_PRODUCT = getenv("INPUT_PRODUCT")
INPUT_NEW_VERSION = getenv("INPUT_NEW_VERSION")
INPUT_CHANGELOG_URL = getenv("INPUT_CHANGELOG_URL")
INPUT_REASON = getenv("INPUT_REASON")
ROOT = Path(getenv("ROOT"))

def write_output(key: str, value: str):
    with open(getenv("GITHUB_OUTPUT"), "a") as _o:
        _o.write(f"{key}={value}\n")

parsed_new_version = parse(INPUT_NEW_VERSION)
version_family = f"{parsed_new_version.major}.{parsed_new_version.minor}"

# goauthentik.io/docs only has release note pages for authentik itself; other
# products (e.g. platform) don't have one to link to yet.
if not INPUT_CHANGELOG_URL and INPUT_PRODUCT == "authentik":
    version_slug = INPUT_NEW_VERSION.replace(".", "")
    INPUT_CHANGELOG_URL = (
        f"https://docs.goauthentik.io/releases/{version_family}/#fixed-in-{version_slug}"
    )

data = {
    "$schema": "https://version.goauthentik.io/schema.json",
    "stable": {
        "version": INPUT_NEW_VERSION,
        "changelog": f"See {INPUT_CHANGELOG_URL}" if INPUT_CHANGELOG_URL else "",
        "changelog_url": INPUT_CHANGELOG_URL or "",
        "reason": INPUT_REASON,
    },
}

version_root = ROOT / "versions" / INPUT_PRODUCT / str(parsed_new_version.major)
version_root.mkdir(parents=True, exist_ok=True)
version_file = version_root / f"{version_family}.json"
version_file.write_text(dumps(data))
version_file.copy(ROOT / "versions" / INPUT_PRODUCT / "latest.json")
# Legacy version file
if INPUT_PRODUCT == "authentik":
    (ROOT / "version.json").write_text(dumps(data))

write_output("changelog_url", INPUT_CHANGELOG_URL)
