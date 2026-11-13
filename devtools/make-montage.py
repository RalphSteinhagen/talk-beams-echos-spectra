#!/usr/bin/env python3
"""Composes figures/emblem-montage.webp, the title slide's panorama (the `pano` box, 26.0 x 8.9 cm, the band between
the subtitle and the footer bar): the talk's century, left to right, that turns from black-and-white into colour — the
Laue pattern, the 1917 sound-ranging headquarters, the Armistice film, Lawrence's cyclotron, a radar operator at the
CRT, LEP's cavities, the Effelsberg dish, a satellite, and the Whirlpool galaxy seen by Hubble. Each picture is cut to a
square, and from the square a tall window is cut, cross-faded into its neighbours; the colour comes in along the strip.
Re-run after changing a picture:
python3 devtools/make-montage.py
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent.parent
TW, FADE = 392, 70      # px of each window and of the cross-fade between neighbours
W, H = 9 * TW - 8 * FADE, 1016   # 2968 x 1016: 2 px per slide pixel of the band (1485.8 x 508.6 px)
FRAME, INK = 4, (242, 242, 242, 255)
COLOUR_FROM, COLOUR_TO = 0.30, 0.80   # fraction of the width over which the colour comes in
# (file, crop box as fractions l,t,r,b or None, centring of the square, centre of the window across the square)
TILES = [
    ("media/laue-pattern-1915.webp",            None,                     (0.50, 0.50), 0.50),  # 1912: X-rays through a crystal
    ("media/sound-ranging-hq-1917.webp",        (0.10, 0.00, 0.90, 1.00), (0.45, 0.40), 0.48),  # 1917: sound-ranging headquarters
    ("media/armistice-record-iwm-q47886.webp",  (0.36, 0.26, 0.64, 0.86), (0.50, 0.50), 0.55),  # 1918: the film, guns then silence
    ("media/lawrence-cyclotron.webp",           (0.08, 0.00, 0.64, 1.00), (0.50, 0.50), 0.25),  # 1930s: Livingston and Lawrence, 27-inch cyclotron
    ("media/radar-operator-1945.webp",          None,                     (0.55, 0.40), 0.58),  # 1945: a radar operator at the CRT
    ("media/lep-cavity-cern-1991.webp",         (0.15, 0.00, 0.75, 1.00), (0.50, 0.45), 0.38),  # 1991: LEP's copper cavities
    ("media/effelsberg-radio-telescope.webp",   (0.00, 0.00, 1.00, 0.80), (0.50, 0.20), 0.40),  # the Effelsberg 100 m radio telescope
    ("media/gps-satellite-nasa.webp",           None,                     (0.55, 0.40), 0.50),  # a satellite
    ("media/m51-whirlpool-hubble.webp",         (0.12, 0.00, 0.78, 1.00), (0.50, 0.50), 0.46),  # the Whirlpool galaxy, Hubble
]


def square(name, box, centre, side):
    picture = Image.open(ROOT / name).convert("RGB")
    if box:
        w, h = picture.size
        picture = picture.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    return ImageOps.fit(picture, (side, side), Image.LANCZOS, centering=centre)


n = len(TILES)
canvas = np.zeros((H, W, 3), dtype=np.float32)
weight = np.zeros((H, W), dtype=np.float32)
ramp = np.linspace(0.0, 1.0, FADE, dtype=np.float32)
for k, (name, box, centre, window) in enumerate(TILES):
    left = round((window - TW / H / 2) * H)   # the window's left edge in the square
    arr = np.asarray(square(name, box, centre, H).crop((left, 0, left + TW, H)), dtype=np.float32)
    mask = np.ones(TW, dtype=np.float32)
    if k > 0:
        mask[:FADE] = ramp
    if k < n - 1:
        mask[-FADE:] = ramp[::-1]
    x = k * (TW - FADE)
    canvas[:, x:x + TW] += arr * mask[None, :, None]
    weight[:, x:x + TW] += mask
canvas /= np.maximum(weight, 1e-6)[..., None]

# the colour comes in from left to right: grey until COLOUR_FROM, full colour from COLOUR_TO
grey = canvas @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
t = np.clip((np.arange(W) / W - COLOUR_FROM) / (COLOUR_TO - COLOUR_FROM), 0.0, 1.0)
t = t * t * (3.0 - 2.0 * t)
mixed = grey[..., None] * (1.0 - t[None, :, None]) + canvas * t[None, :, None]
out = Image.fromarray(np.clip(mixed, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
ImageDraw.Draw(out).rectangle((0, 0, W - 1, H - 1), outline=INK, width=FRAME)
target = ROOT / "figures" / "emblem-montage.webp"
out.save(target, "WEBP", quality=88, method=6)
print(f"{target.name}: {W}x{H}, {n} pictures")
