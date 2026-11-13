#!/usr/bin/env python3
"""Writes the deck's SVG masters from the area tables below: figures/master-title.svg (and -logo, the same areas for
the full-page navy slides), master-main.svg, master-double.svg, master-figure.svg and master-blank.svg. Derived from
talk-gremlin's generator: the same geometry, without the GREMLIN logo, the iRIS eye, the EU flag and the funding box.

The chalkboard look follows the author's template (template.odp); the geometry is talk-gremlin's: 28 x 15.75 cm; the masters are 1600 x 900 px, so 1 cm = 1600/28 px. Every area is a hidden box the
viewer fills (`data-present`), grouped into the `top`, `middle` and `bottom` bands gr4-present stretches to the
screen; `content` takes the slide's own Markdown. The logos every slide shows are drawn into the master (nested SVG).
index.yml names the masters once (`masters:`); a slide picks another with `{master=double}` on its heading.
Re-run after editing a table: python3 devtools/make-masters.py
"""
import base64
import re
from pathlib import Path

PX = 1600 / 28.0
HERE = Path(__file__).resolve().parent.parent / "figures"


def box(name, x1, y1, x2, y2, kind="markdown"):
    return (name, kind, round(x1 * PX), round(y1 * PX), round((x2 - x1) * PX), round((y2 - y1) * PX))


# ---- title master: navy as in the original, areas in cm (x1 y1 x2 y2) ---------------------------
TITLE_BG = "chalk"   # the template.odp chalkboard texture, one strip per band (figures/chalk-*.jpg)
TITLE_AREAS = [
    box("title",        0.00, 0.00, 0.01, 0.01),              # the heading is empty on the title slides: `headline` holds the title
    box("logo",         19.1, 0.30, 27.60, 4.35, "image"),    # the conference banner (cut out of the organisers' header, 2.1:1), top right: 8.5 cm wide, 80 % of round 11
    box("headline",     1.00, 0.50, 15.80, 3.20),             # `:::headline {size=400%}` — the big title
    box("subtitle",     1.00, 3.90, 18.60, 6.60),             # `:::subtitle {size=180%}`, left of the banner, wraps to two lines
    box("authors",      1.00, 6.70, 18.60, 7.60),             # the name, just beneath, left
    box("emblem",       1.00, 8.00, 26.60, 13.30, "image"),   # the opening panorama (figures/emblem-montage.webp, 5.12:1)
    box("content",      2.52, 1.30, 25.41, 14.6),             # the full-page slides (Questions, GREMLIN)
    box("organisers",   1.00, 10.7, 14.6, 12.7, "image"),     # the organisers' logo card (6.8:1) above the event line; the Questions slide
    box("event",        1.00, 13.3, 23.50, 15.65),            # free on the title slide; the Questions slide uses it
]
TITLE_PICTURES = []
TITLE_DECOR = []
TITLE_BANDS = (200, 810)

# ---- content masters: white, as the original ----------------------------------------------------
CONTENT_BG = "chalk"
HEADER = [
    box("title",        0.60, 0.12, 27.70, 1.95),            # `# Title<br>Sub-header`
    box("icons",        18.2, 0.15, 27.70, 2.25, "image"),   # a picture at the top right, over the title's end
]
FOOTER = [
    # no `footnotes` box: credits and citations show only their number on the slide; the text is on the References
    # slide alone (every box that cites is `{notes=off}`, so the viewer draws nothing at the box's foot either)
    # no `slide_number` box either (author, 2026-11-11): the masters show no slide number
]
MAIN_AREAS = HEADER + [box("content", 1.00, 2.30, 27.00, 13.9)] + FOOTER
DOUBLE_AREAS = HEADER + [box("content", 0.70, 2.30, 13.90, 13.9), box("right", 14.20, 2.30, 27.50, 13.9)] + FOOTER
FIGURE_AREAS = HEADER + [box("figure", 1.00, 2.30, 27.00, 8.30, "image"), box("content", 1.00, 8.50, 27.00, 13.9)] + FOOTER   # a picture above, text below
# the portrait column stands in the top right corner, from the title's height down, exactly above the FAIR/GSI logos
# and as wide as they are (3.2 cm, the deck's portrait width: the portraits are cropped 4:5, so a portrait is
# 3.2 x 4.0 cm everywhere); the title row and the content stop 0.5 cm before it (no `icons` box: the column has the
# corner). Each picture takes the full width, so its caption lines up with its left edge (the viewer centres a picture
# only when the box's height budget caps it)
PEOPLE_HEADER = [box("title", 0.60, 0.12, 23.60, 1.95)]
PEOPLE_AREAS = PEOPLE_HEADER + [box("content", 1.00, 2.30, 23.60, 13.9), box("people", 24.10, 0.30, 27.30, 13.95)] + FOOTER
BLANK_AREAS = [box("title", 0.60, 0.12, 27.70, 1.95), box("content", 0.60, 2.30, 27.40, 14.4)] + FOOTER   # the References slide: a heading row, then a grid over the content
CONTENT_BANDS = (120, 800)   # the FAIR/GSI logos (from 806 px) belong to the bottom band, which clips nothing of them

# pictures drawn into the content masters (x1 y1 x2 y2 in cm): the white logos, small, lower right
FAIR_GSI     = ("logos-dark.svg", 24.10, 14.35, 27.30, 15.15)   # lower right, visibly 0.7 cm from the right and from the bottom edge


def embed(name, x1, y1, x2, y2):
    """The figure's own SVG nested at that place of the master: its root keeps its viewBox, loses its size."""
    text = (HERE / name).read_text(encoding="utf-8")
    text = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", text)
    root = re.match(r"<svg\b[^>]*>", text, re.S)
    sized = dict(re.findall(r'\s(width|height)="([\d.]+)[a-z]*"', root.group(0)))
    tag = re.sub(r'\s(width|height)="[^"]*"', "", root.group(0))
    if "viewBox" not in tag and {"width", "height"} <= sized.keys():
        tag = tag.replace("<svg", f'<svg viewBox="0 0 {sized["width"]} {sized["height"]}"', 1)   # else its units stay the master's
    tag = tag.replace("<svg", f'<svg x="{round(x1 * PX)}" y="{round(y1 * PX)}" width="{round((x2 - x1) * PX)}" height="{round((y2 - y1) * PX)}"', 1)
    body = text[root.end():]
    # a nested <style> is not applied by the viewer's renderer: its class rules become style attributes
    rules = dict(re.findall(r"\.([\w-]+)\s*\{([^}]*)\}", " ".join(re.findall(r"<style[^>]*>(.*?)</style>", body, re.S))))
    body = re.sub(r"<style[^>]*>.*?</style>\s*", "", body, flags=re.S)
    body = re.sub(r'class="([\w-]+)"', lambda m: f'style="{rules[m.group(1)].strip()}"' if m.group(1) in rules else m.group(0), body)
    # the renderer maps one nested <svg> viewBox but not one inside it: inner ones become transformed groups
    def flatten(m):
        attrs = dict(re.findall(r'([\w:-]+)="([^"]*)"', m.group(0)))
        x, y, w, h = (float(attrs.get(k, 0)) for k in ("x", "y", "width", "height"))
        vx, vy, vw, vh = (float(v) for v in attrs["viewBox"].split())
        scale = min(w / vw, h / vh)   # preserveAspectRatio xMidYMid meet
        tx, ty = x + (w - vw * scale) / 2 - vx * scale, y + (h - vh * scale) / 2 - vy * scale
        return f'<g transform="translate({tx:.4f} {ty:.4f}) scale({scale:.6f})">'
    body = re.sub(r"<svg\b[^>]*>", flatten, body).replace("</svg>", "</g>", body.count("</svg>") - 1)
    return tag + body


def write(path, areas, bands, background, title, decor=(), pictures=()):
    top, bottom = bands
    groups = {"top": [], "middle": [], "bottom": []}
    for name, x1, y1, x2, y2 in pictures:
        band = "top" if y1 * PX < top else "bottom" if y1 * PX >= bottom else "middle"
        groups[band].append(embed(name, x1, y1, x2, y2))
    for name, kind, x, y, w, h in areas:
        band = "top" if y < top else "bottom" if y >= bottom else "middle"
        groups[band].append(f'    <rect id="{name}" data-present="{kind}" x="{x}" y="{y}" width="{w}" height="{h}" fill="none"/>')
    def fill(y0, y1):
        if background == "chalk":   # the texture strip of this band, embedded: the viewer draws a master's raster only as a data URI
            band = {0: "top", top: "middle", bottom: "bottom"}[y0]
            data = base64.b64encode((HERE / f"chalk-{band}.jpg").read_bytes()).decode()
            return (f'    <rect x="0" y="{y0}" width="1600" height="{y1 - y0}" fill="#1f1f1f"/>\n'
                    f'    <image x="0" y="{y0}" width="1600" height="{y1 - y0}" preserveAspectRatio="none" href="data:image/jpeg;base64,{data}"/>')
        return f'    <rect x="0" y="{y0}" width="1600" height="{y1 - y0}" fill="{background}"/>' if background else ""
    lines = ['<?xml version="1.0" encoding="utf-8"?>',
             '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 1600 900" width="1600" height="900">',
             f'  <title>{title}</title>',
             '  <g id="top">', fill(0, top), *groups["top"], '  </g>',
             '  <g id="middle">', fill(top, bottom), *decor, *groups["middle"], '  </g>',
             '  <g id="bottom">', fill(bottom, 900), *groups["bottom"], '  </g>',
             '</svg>', '']
    path.write_text("\n".join(line for line in lines if line != ""), encoding="utf-8")
    print(f"{path.name}: {len(areas)} areas")


write(HERE / "master-title.svg", TITLE_AREAS, TITLE_BANDS, TITLE_BG, "title master: chalkboard, title, subtitle, emblem, authors, logo, event", TITLE_DECOR, TITLE_PICTURES + [FAIR_GSI])
write(HERE / "master-title-logo.svg", TITLE_AREAS, TITLE_BANDS, TITLE_BG, "title master for the full-page slides (Questions, GREMLIN)", pictures=TITLE_PICTURES + [FAIR_GSI])
write(HERE / "master-main.svg", MAIN_AREAS, CONTENT_BANDS, CONTENT_BG, "main master: chalkboard, title with sub-header, content, FAIR/GSI logos, number", pictures=(FAIR_GSI,))
write(HERE / "master-double.svg", DOUBLE_AREAS, CONTENT_BANDS, CONTENT_BG, "double master: as main, the content on the left and a right column", pictures=(FAIR_GSI,))
write(HERE / "master-figure.svg", FIGURE_AREAS, CONTENT_BANDS, CONTENT_BG, "figure master: as main, a picture box above the text", pictures=(FAIR_GSI,))
write(HERE / "master-blank.svg", BLANK_AREAS, CONTENT_BANDS, CONTENT_BG, "blank master: chalkboard, content over the whole page, number")
write(HERE / "master-people.svg", PEOPLE_AREAS, CONTENT_BANDS, CONTENT_BG, "people master: as main, a portrait column at the right", pictures=(FAIR_GSI,))
for stale in ("master-content.svg", "master-content-no-gremlin.svg", "master-content-no-fair-gsi.svg"):
    (HERE / stale).unlink(missing_ok=True)


def chalk_patch(name, x0, y0, x1, y1, bands=CONTENT_BANDS):
    """A piece of a content master's chalkboard, cut at the same place (slide pixels, 1600 x 900): laid under a box
    that arrives on a click, it hides what was there before without a visible frame (the viewer's reveals only add,
    and a `{frame}` box would paint the theme's black). figures/chalk-patch-<name>.webp, lossless."""
    from PIL import Image
    top, bottom = bands
    board = Image.new("RGB", (1600, 900), (0x1f, 0x1f, 0x1f))
    for band, (a, b) in {"top": (0, top), "middle": (top, bottom), "bottom": (bottom, 900)}.items():
        board.paste(Image.open(HERE / f"chalk-{band}.jpg").convert("RGB").resize((1600, b - a)), (0, a))
    board.crop((x0, y0, x1, y1)).save(HERE / f"chalk-patch-{name}.webp", lossless=True)
    print(f"chalk-patch-{name}.webp: {x1 - x0}x{y1 - y0} at ({x0}, {y0})")


# the left column of `exp1` and `lowpass` lies over the live region's placeholder pane (gr4-present 28c5abe: `layer=above`);
# a `{frame}` box would cover it too, but its frame is drawn before its step reveals it — patches instead (2026-11-13)
# The pane spans x 57-560, y 478-765 (slide px); each patch overlaps it by ~10 px (above it the ranging chart's "x [m]",
# right of it the next charts' axis labels from x ~568) and its box in talk.md has exactly its aspect — a `fit` patch of
# another aspect is shrunk and left a strip of the empty chart's frame showing (round 56). gr4-present also insets every
# image box: measured in the online viewer (round 56), an image is drawn top-aligned, its height the box's minus 16 px,
# centred across — so each card box is the patch grown by 8 px left and right and by 16 px at the bottom, and the image
# is drawn 1:1 at the patch's own place, seamless with the board.
chalk_patch("exp1", 48, 468, 564, 884)   # `exp1` card0/card1: 0.0250 0.5200 0.3325 0.4800 — the pane, the 1917 photo and its caption
chalk_patch("left", 48, 468, 564, 776)   # `lowpass`, `exp2`, `exp6` card: 0.0250 0.5200 0.3325 0.3600 (the captions below stay clear)
