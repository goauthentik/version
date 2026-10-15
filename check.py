from json import loads
from pathlib import Path

from packaging.version import parse

ROOT = Path(__file__).parent
errors = []


def load(path: Path) -> dict:
    return loads(path.read_text())


for product in sorted((ROOT / "versions").iterdir()):
    latest = load(product / "latest.json")
    families = {f: load(f) for f in product.glob("*/*.json")}
    newest = max(families, key=lambda f: parse(f.stem))
    if families[newest] != latest:
        errors.append(f"{product / 'latest.json'} does not match newest family file {newest}")
    for file, data in families.items():
        if not data["stable"]["version"].startswith(f"{file.stem}."):
            errors.append(f"{file} contains version {data['stable']['version']}")

# Legacy version file, read by older authentik versions
if load(ROOT / "version.json") != load(ROOT / "versions" / "authentik" / "latest.json"):
    errors.append("version.json does not match versions/authentik/latest.json")

for error in errors:
    print(f"::error::{error}")
raise SystemExit(1 if errors else 0)
