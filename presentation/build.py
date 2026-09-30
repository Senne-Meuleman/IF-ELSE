"""Build the pitch deck: src/* -> index.html (one file, screenshots inlined).

    py -3.12 build.py

Edit src/slides.html (content), src/theme.css (look), src/deck.js (phone wall).
src/base.css and src/engine.js are the epic-pitch-deck engine; leave them alone.
"""
import base64
import pathlib
import re

HERE = pathlib.Path(__file__).parent
SRC = HERE / "src"


def read(name: str) -> str:
    return (SRC / name).read_text(encoding="utf-8")


def inline_assets(html: str) -> str:
    def data_uri(m: re.Match) -> str:
        path = SRC / "assets" / m.group(1)
        mime = "image/jpeg" if path.suffix == ".jpg" else "image/png"
        return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"
    return re.sub(r"assets/([\w-]+\.(?:jpg|png))", data_uri, html)


html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KBC Adaptive Home · Pitch</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{read("base.css")}
{read("theme.css")}
</style>
</head>
<body>
<div class="stage" id="stage">
  <div class="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="grid-lines"></div><div class="grain"></div></div>
{read("slides.html")}
</div>
<div class="progress" id="progress"></div>
<div class="counter" id="counter"></div>
<script>
{read("engine.js")}
{read("deck.js")}
</script>
</body>
</html>
"""
out = HERE / "index.html"
out.write_text(inline_assets(html), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
