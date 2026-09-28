"""Render every slide of a deck to PNG using headless Chrome/Edge.

Usage:
    python screenshot_slides.py path/to/index.html [out_dir] [--animated]

By default loads each slide with ?static (final state, no motion) so screenshots
show exactly what the audience sees once animations settle. --animated instead
waits ~3s of virtual time per slide with motion enabled (useful to catch
elements that never animate in).
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chrome") or "",
    shutil.which("msedge") or "",
]


def find_browser():
    for c in CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("No Chrome/Edge found. Set CHROME_PATH to a Chromium-based browser.")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    animated = "--animated" in sys.argv
    if not args:
        sys.exit(__doc__)
    deck = Path(args[0]).resolve()
    out = (Path(args[1]) if len(args) > 1 else deck.parent / "screenshots").resolve()
    out.mkdir(parents=True, exist_ok=True)

    html = deck.read_text(encoding="utf-8")
    n = len(re.findall(r'<section[^>]*class="[^"]*\bslide\b', html))
    browser = find_browser()
    query = "" if animated else "?static"
    for i in range(1, n + 1):
        png = out / f"slide-{i:02d}.png"
        url = deck.as_uri() + f"{query}#{i}"
        subprocess.run(
            [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--window-size=1920,1080", "--force-device-scale-factor=1",
             f"--virtual-time-budget={3500 if animated else 1500}",
             f"--screenshot={png}", url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60,
        )
        print(("ok   " if png.exists() else "FAIL ") + str(png))
    print(f"{n} slides -> {out}")


if __name__ == "__main__":
    main()
