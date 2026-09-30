"""Build pitch.mp4: record the deck (index.html) headlessly via CDP screencast while
stepping slides in sync with the voice clips, then mux the audio with ffmpeg.

    py -3.12 make_video.py            (needs ffmpeg on PATH, playwright + chromium, pillow)

Cue times (seconds into each clip) come from whisper word timestamps of voice/*.mp3.
If a clip is re-recorded, re-check its CUES. Work dir: build_video/ (safe to delete)."""
import asyncio, base64, io, json, pathlib, sys, time
from PIL import Image
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
S = HERE / "build_video"; FR = S / "frames"; FR.mkdir(parents=True, exist_ok=True)
for old in FR.glob("*.jpg"): old.unlink()
DECK = (HERE / "index.html").resolve().as_uri()
LEAD = 0.15      # reveal this much before the word is spoken
GAP = 0.5        # silence between clips
DUR = {"opening":27.167,"vision":49.946,"examples_introduction":2.116,"lena":21.394,
       "marc":17.084,"peeters":25.469,"closing":22.831}
# (clip, [(time_in_clip, action)])  action: ("go", slideIndex0) | ("next",)
CUES = {
 "opening":  [(8.22,("next",)),(11.32,("go",1)),(23.08,("next",))],
 "vision":   [(13.04,("go",3)),(15.52,("next",)),(22.52,("next",)),(25.88,("next",)),
              (28.76,("go",4)),(31.68,("next",)),(33.3,("next",)),(36.28,("go",5)),(43.94,("next",))],
 "examples_introduction": [],
 "lena":     [(8.0,("next",)),(14.04,("next",)),(18.06,("next",))],
 "marc":     [(5.42,("next",)),(6.94,("next",)),(13.9,("next",))],
 "peeters":  [(4.98,("next",)),(10.66,("next",)),(16.8,("next",))],
 "closing":  [(3.22,("next",)),(5.14,("go",10)),(13.56,("next",)),(19.22,("go",11))],
}
# slide to switch to right before a clip starts (None = stay)
PRE = {"opening":None,"vision":2,"examples_introduction":6,"lena":None,"marc":7,"peeters":8,"closing":9}
ORDER = ["opening","vision","examples_introduction","lena","marc","peeters","closing"]
FIRST_AUDIO = 0.7; TAIL = 3.0

# Build global timeline (relative to t0 = first deck frame)
events = []   # (t, action)
starts = {}
t = FIRST_AUDIO
for i, c in enumerate(ORDER):
    if i: t += GAP
    if PRE[c] is not None: events.append((t - 0.35, ("go", PRE[c])))
    starts[c] = t
    for ct, a in CUES[c]: events.append((t + ct - LEAD, a))
    t += DUR[c]
END = t + TAIL
events.sort()

async def main():
    frames = []      # (timestamp, path)
    state = {"t0": None, "n": 0}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--force-device-scale-factor=1"])
        ctx = await browser.new_context(viewport={"width":1920,"height":1080}, device_scale_factor=1)
        warm = await ctx.new_page(); await warm.goto(DECK); await warm.wait_for_timeout(1500)
        await warm.evaluate("document.fonts.ready"); await warm.close()
        page = await ctx.new_page()
        await page.goto("data:text/html,<body style='margin:0;background:%23ff00ff'></body>")
        await page.wait_for_timeout(300)
        cdp = await ctx.new_cdp_session(page)

        def on_frame(ev):
            data = base64.b64decode(ev["data"]); ts = ev["metadata"]["timestamp"]
            asyncio.ensure_future(cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]}))
            if state["t0"] is None:
                im = Image.open(io.BytesIO(data)).convert("RGB"); px = im.getpixel((960, 540))
                if px[0] > 200 and px[1] < 80 and px[2] > 200: return   # still magenta
                state["t0"] = ts; print("first deck frame", ts, file=sys.stderr)
            path = FR / f"f{state['n']:05d}.jpg"; state["n"] += 1
            path.write_bytes(data); frames.append((ts, path.name))
        cdp.on("Page.screencastFrame", on_frame)
        await cdp.send("Page.startScreencast", {"format":"jpeg","quality":92,"maxWidth":1920,"maxHeight":1080,"everyNthFrame":1})
        await page.wait_for_timeout(500)
        t_nav = time.time()
        await page.goto(DECK)
        # wait for the first deck frame
        while state["t0"] is None: await asyncio.sleep(0.005)
        t0 = state["t0"]; print(f"load->frame latency {t0 - t_nav:.3f}s", file=sys.stderr)
        log = []
        for et, a in events:
            while (d := t0 + et - time.time()) > 0: await asyncio.sleep(min(d, 0.01))
            if a[0] == "go": await page.evaluate(f"go({a[1]})")
            else: await page.evaluate("next()")
            log.append((round(time.time() - t0, 3), et, a))
        while time.time() - t0 < END: await asyncio.sleep(0.02)
        # tickle a last frame so hold duration is defined, then stop
        await cdp.send("Page.stopScreencast")
        await browser.close()
    # concat list
    frames.sort()
    lines = ["ffconcat version 1.0"]
    for i, (ts, name) in enumerate(frames):
        nxt = frames[i+1][0] if i+1 < len(frames) else t0 + END
        lines += [f"file 'frames/{name}'", f"duration {max(0.001, nxt - ts):.4f}"]
    lines += [f"file '{frames[-1][1]}'"]
    (S/"frames.txt").write_text("\n".join(lines)+"\n")
    (S/"timeline.json").write_text(json.dumps({"starts":starts,"end":END,"first_frame_offset":frames[0][0]-t0,"log":log}, indent=1))
    late = max(abs(l[0]-l[1]) for l in log)
    print(f"frames={len(frames)} span={frames[-1][0]-frames[0][0]:.1f}s END={END:.1f}s max action lateness={late:.3f}s")
    for l in log: print(l)

asyncio.run(main())

# ---- audio mix + final encode -------------------------------------------------
import subprocess
tl = json.loads((S/"timeline.json").read_text())
V = HERE / "voice"
inputs, fc = [], []
for i, c in enumerate(ORDER):
    inputs += ["-i", str(V / f"{c}.mp3")]
    ms = int(round(tl["starts"][c] * 1000))
    fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={ms}|{ms}[a{i}]")
fc.append("".join(f"[a{i}]" for i in range(len(ORDER))) + f"amix=inputs={len(ORDER)}:normalize=0:dropout_transition=0,apad=whole_dur={tl['end']:.3f}[out]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[out]", "-c:a", "pcm_s16le", str(S/"audio.wav")], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(S/"frames.txt"), "-i", str(S/"audio.wav"),
                "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-profile:v", "high", "-movflags", "+faststart",
                "-c:a", "aac", "-b:a", "192k", "-t", f"{tl['end']:.3f}", "-map", "0:v", "-map", "1:a", str(HERE/"pitch.mp4")], check=True)
print("wrote", HERE/"pitch.mp4")
