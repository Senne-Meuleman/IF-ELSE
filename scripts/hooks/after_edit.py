"""Claude Code PostToolUse hook for Edit/Write (see .claude/settings.json).

Reads the hook JSON on stdin and:
  1. syntax-checks an edited .py file, so a broken demo entry point is caught the
     second it is written (exit 2 sends the error back to the agent);
  2. re-syncs .agents/skills/ when a file under .claude/skills/ changes.
Anything unexpected exits 0: the hook must never block ordinary work.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    raw = (data.get("tool_input") or {}).get("file_path") or (data.get("tool_response") or {}).get("filePath")
    if not raw:
        return 0
    path = Path(raw)
    if path.suffix == ".py" and path.exists():
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as e:
            print(f"SyntaxError in {path.name} line {e.lineno}: {e.msg}. Fix it before moving on.", file=sys.stderr)
            return 2
    try:
        rel = path.resolve().relative_to(ROOT)
    except ValueError:
        return 0
    if rel.parts[:2] == (".claude", "skills"):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_skills.py")],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode:
            print((r.stdout + r.stderr).strip()[-1500:], file=sys.stderr)
            return 2
        print(r.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
