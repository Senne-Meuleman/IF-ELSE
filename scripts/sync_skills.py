"""Validate and copy Claude skill sources to Codex/Cursor. Run with --check in CI."""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".claude" / "skills"
TARGET = ROOT / ".agents" / "skills"
IGNORED = {"__pycache__", ".DS_Store"}


def inventory(folder: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(folder): path.read_bytes()
        for path in sorted(folder.rglob("*"))
        if path.is_file() and not any(part in IGNORED for part in path.parts)
        and path.suffix != ".pyc"
    }


def validate(files: dict[Path, bytes]) -> None:
    skills = [path for path in files if path.name == "SKILL.md"]
    if not skills:
        raise ValueError("No skills found")
    for path in skills:
        text = files[path].decode("utf-8").replace("\r\n", "\n")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            raise ValueError(f"{path}: missing YAML frontmatter")
        header, body = text[4:].split("\n---\n", 1)
        fields = dict(line.split(":", 1) for line in header.splitlines() if ":" in line)
        name = fields.get("name", "").strip()
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            raise ValueError(f"{path}: invalid name")
        if name != path.parent.name or len(path.parts) != 2:
            raise ValueError(f"{path}: name must match its top-level skill folder")
        if not fields.get("description", "").strip() or not body.strip():
            raise ValueError(f"{path}: description and body required")
        for ref in re.findall(r"`((?:references|assets|scripts)/[^`\s]+)`", body):
            if path.parent / ref not in files:
                raise ValueError(f"{path}: missing resource {ref}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report drift without writing")
    args = parser.parse_args()
    source = inventory(SOURCE)
    validate(source)
    target = inventory(TARGET)
    stale = sorted(set(target) - set(source))
    changed = [path for path, data in source.items() if target.get(path) != data]
    if stale:
        # Never silently delete a teammate's skill or resource.
        print("Unexpected target files; review and remove or move to the source:")
        for path in stale:
            print(f"  {TARGET / path}")
        return 1
    if args.check and changed:
        print("Skill copies differ. Run: python scripts/sync_skills.py")
        for path in changed:
            print(f"  {path}")
        return 1
    if not args.check:
        for path in changed:
            destination = TARGET / path
            if not destination.resolve().is_relative_to(TARGET.resolve()):
                raise ValueError(f"Destination escapes skill root: {path}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source[path])
    count = sum(path.name == "SKILL.md" for path in source)
    print(f"Validated {count} skills, {len(source)} files; copies are synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
