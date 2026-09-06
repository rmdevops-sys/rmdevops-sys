"""
render_github_banner.py

Render the working animated SVG banner to animated GIFs for GitHub README use.

Recommended:
  1. Install Inkscape and make sure `inkscape` is available in PATH.
  2. Run:
       python render_github_banner.py

The script renders frames with Inkscape, then assembles them with Pillow.
The original SVG files remain untouched as the animation source of truth.
"""

from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parent
FPS = 20
DURATION_SECONDS = 14.2
FRAME_COUNT = int(FPS * DURATION_SECONDS)

def require(cmd):
    if shutil.which(cmd) is None:
        raise SystemExit(
            f"'{cmd}' was not found in PATH. Install Inkscape and reopen your terminal."
        )

def render_svg(svg_name, gif_name):
    svg = ROOT / svg_name
    out = ROOT / gif_name

    if not svg.exists():
        raise SystemExit(f"Missing {svg}")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # Inkscape CLI exports a selected animation time with --export-id-only
        # only for static objects, so for SMIL timing use its frame sequence.
        # We create a tiny HTML wrapper and use Playwright/Chromium if available.
        # This preserves SMIL animation much better than CairoSVG.
        if shutil.which("node"):
            pass

        # Preferred path: use Playwright if installed in Python.
        try:
            import asyncio
            from playwright.async_api import async_playwright
        except Exception:
            raise SystemExit(
                "Playwright is required for accurate animated-SVG rendering. "
                "Install with: pip install playwright pillow && playwright install chromium"
            )

        async def capture():
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page(viewport={"width": 1180, "height": 610}, device_scale_factor=1)
                url = svg.resolve().as_uri()
                await page.goto(url, wait_until="load")
                await page.wait_for_timeout(100)

                frames = []
                for i in range(FRAME_COUNT):
                    path = td / f"frame_{i:04d}.png"
                    await page.screenshot(path=str(path), animations="allow")
                    frames.append(path)
                    await page.wait_for_timeout(round(1000 / FPS))
                await browser.close()
                return frames

        frames = asyncio.run(capture())

        images = [Image.open(p).convert("P", palette=Image.Palette.ADAPTIVE, colors=256) for p in frames]
        # 50ms/frame = 20fps
        images[0].save(
            out,
            save_all=True,
            append_images=images[1:],
            duration=50,
            loop=0,
            optimize=False,
            disposal=2,
        )

    print(f"Created {out} ({out.stat().st_size / 1024:.1f} KB)")

for svg, gif in [
    ("dark.svg", "profile-banner-dark.gif"),
    ("light.svg", "profile-banner-light.gif"),
]:
    render_svg(svg, gif)
