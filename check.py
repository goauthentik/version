from json import dumps, loads
from pathlib import Path

from packaging.version import parse

ROOT = Path(__file__).parent


def load(path: Path) -> dict:
    return loads(path.read_text())


def build_index(product: Path) -> str:
    families = sorted(product.glob("*/*.json"), key=lambda f: parse(f.stem), reverse=True)
    return dumps({
        "families": [
            {"family": f.stem, "path": str(f.relative_to(product)), "stable": load(f)["stable"]}
            for f in families
        ]
    }) + "\n"


if __name__ == "__main__":
    errors = []
    for product in sorted(p for p in (ROOT / "versions").iterdir() if p.is_dir()):
        latest = load(product / "latest.json")
        families = {f: load(f) for f in product.glob("*/*.json")}
        newest = max(families, key=lambda f: parse(f.stem))
        if families[newest] != latest:
            errors.append(f"{product / 'latest.json'} does not match newest family file {newest}")
        for file, data in families.items():
            if not data["stable"]["version"].startswith(f"{file.stem}."):
                errors.append(f"{file} contains version {data['stable']['version']}")
        index = product / "index.json"
        if not index.exists() or index.read_text() != build_index(product):
            errors.append(f"{index} is out of date, regenerate with build_index")

    # Legacy version file, read by older authentik versions
    if load(ROOT / "version.json") != load(ROOT / "versions" / "authentik" / "latest.json"):
        errors.append("version.json does not match versions/authentik/latest.json")

    for error in errors:
        print(f"::error::{error}")
    raise SystemExit(1 if errors else 0)
