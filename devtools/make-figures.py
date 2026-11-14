#!/usr/bin/env python3
"""Draws the deck's schematic figures as SVG (text as text, sans-serif): figures/pipeline.svg, three-domain.svg,
escalation.svg, braid.svg and its dated snapshots, setup.svg, tdoa-map.svg, inference-ladder.svg and the rest the loop
at the end names; figures no slide shows any more are not drawn (round 56).
The masters are a dark chalkboard, so the drawings use chalk-like light ink. Re-run: python3 devtools/make-figures.py"""
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
INK, NAVY, BLUE, ORANGE, GREEN, RED, GREY, LIGHT = "#f2f2f2", "#9ecbff", "#7cc4ff", "#ffd866", "#8fe3a8", "#ff8a8a", "#c4c4c4", "#2e2e2e"   # chalk on a blackboard
FONT = 'font-family="Liberation Sans, Arial, sans-serif"'


class SVG:
    def __init__(self, w, h, title):
        self.w, self.h, self.parts = w, h, [f'<?xml version="1.0" encoding="utf-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>',
            f'  <title>{title}</title>',
            '  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker>'
            '<marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{BLUE}"/></marker></defs>']

    def add(self, s):
        self.parts.append("  " + s)

    def text(self, x, y, s, size=22, anchor="middle", colour=INK, weight="normal", style="normal"):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{colour}" font-weight="{weight}" font-style="{style}">{s}</text>')

    def lines(self, x, y, items, size=22, anchor="middle", colour=INK, lh=1.25, weight="normal"):
        for i, s in enumerate(items):
            self.text(x, y + i * size * lh, s, size, anchor, colour, weight)

    def box(self, x, y, w, h, fill=LIGHT, stroke=NAVY, rx=10, sw=2.5):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def arrow(self, x1, y1, x2, y2, colour=INK, sw=3, both=False, dash=None):
        extra = ' marker-start="url(#arrow)"' if both else ""
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = "arrow-blue" if colour == BLUE else "arrow"
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{colour}" stroke-width="{sw}" marker-end="url(#{m})"{extra}{d}/>')

    def path(self, d, stroke=INK, sw=3, fill="none", marker=False, dash=None):
        m = ' marker-end="url(#arrow)"' if marker else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"{m}{da}/>')

    def circle(self, x, y, r, fill=BLUE, stroke=INK, sw=2):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def write(self, name, crop=None):
        """crop = (x, y, w, h): publish only that part of the canvas (a figure drawn on a generous canvas, shown large)"""
        if crop:
            x, y, w, h = crop
            self.parts[1] = self.parts[1].replace(f'viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}"',
                                                  f'viewBox="{x} {y} {w} {h}" width="{w}" height="{h}"')
        (OUT / name).write_text("\n".join(self.parts + ["</svg>", ""]), encoding="utf-8")
        print(name)


def pipeline():
    """excite → propagate → interact → observe → infer → control, with what each stage meant historically."""
    s = SVG(1500, 330, "the recurring measurement and control chain")
    stages = [("excite", "spark, gun, carrier,", "RF pulse, bunch"), ("propagate", "air, ether, cable,", "waveguide, beam pipe"),
              ("interact", "target, receiver,", "cavity, particle"), ("observe", "coherer, microphone,", "antenna, pickup, ADC"),
              ("infer", "position, range,", "spectrum, state"), ("control", "steer, jam, tune,", "feed back")]
    w, h, gap, x0, y0 = 216, 125, 37, 20, 60
    for i, (name, a, b) in enumerate(stages):
        x = x0 + i * (w + gap)
        s.box(x, y0, w, h, fill=LIGHT if i < 5 else "#4a3f1f", stroke=NAVY if i < 5 else ORANGE)
        s.text(x + w / 2, y0 + 46, name, 32, weight="bold", colour=NAVY)
        s.lines(x + w / 2, y0 + 82, [a, b], 19, colour=GREY)
        if i < 5:
            s.arrow(x + w + 6, y0 + h / 2, x + w + gap - 6, y0 + h / 2)
    # the feedback return from control to excite, its label above the dashed line (not on it)
    xc, xe, yl = x0 + 5 * (w + gap) + w / 2, x0 + w / 2, y0 + h + 85
    s.path(f"M {xc} {y0 + h + 2} L {xc} {yl} L {xe} {yl} L {xe} {y0 + h + 8}", stroke=ORANGE, marker=True, dash="10 8")
    s.text((xc + xe) / 2, yl - 14, "measure → estimate → decide → actuate → measure again", 24, colour=ORANGE, style="italic")
    s.write("pipeline.svg", crop=(18, 50, 1486, 230))


def three_domain():
    """The triangle: accelerators, radar/SIGINT, radio/telecom around RF/DSP; none of the arrows one-way."""
    s = SVG(1200, 760, "three domains around one RF and DSP core")
    P = {"acc": (600, 95), "radar": (170, 600), "radio": (1030, 600), "core": (600, 430)}
    labels = {"acc": ("PHYSICS /", "ACCELERATORS"), "radar": ("RADAR /", "SIGINT · EW"), "radio": ("RADIO /", "TELECOM"), "core": ("RF · DSP ·", "SOFTWARE")}
    for k, (x, y) in P.items():
        w, h = (300, 100) if k != "core" else (260, 110)
        s.box(x - w / 2, y - h / 2, w, h, fill="#4a3f1f" if k == "core" else LIGHT, stroke=ORANGE if k == "core" else NAVY, rx=16)
        s.lines(x, y - 8, labels[k], 30, weight="bold", colour=NAVY if k != "core" else ORANGE)
    def edge(a, b, t1, t2, off):
        (x1, y1), (x2, y2) = P[a], P[b]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        def sh(k):
            w, h = (150, 50) if k != "core" else (130, 55)
            return min(w / max(abs(ux), 1e-6), h / max(abs(uy), 1e-6)) + 12
        s.arrow(x1 + ux * sh(a) + off[0], y1 + uy * sh(a) + off[1], x2 - ux * sh(b) + off[0], y2 - uy * sh(b) + off[1], both=True, colour=BLUE)
        mx, my = (x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1]
        s.lines(mx + off[2], my + off[3], [t1, t2], 20, colour=GREY)
    edge("acc", "radar", "RF sources, pulsed power,", "klystron ↔ magnetron", (-10, 0, -135, -10))
    edge("acc", "radio", "oscillators, resonators,", "Schottky, superhet", (10, 0, 135, -10))
    edge("radar", "radio", "mixers, IF, timing,", "navigation beams", (0, 10, 0, 50))
    edge("core", "acc", "LLRF, diagnostics,", "feedback", (0, 0, 120, 0))
    edge("core", "radar", "ranging, matched", "filter, arrays", (0, 0, 20, 60))
    edge("core", "radio", "modulation, filtering,", "SDR", (0, 0, -20, 60))
    s.text(600, 740, "none of the arrows is one-way", 26, colour=RED, style="italic")
    s.write("three-domain.svg")


def escalation():
    """The War of the Beams as an escalation ladder."""
    s = SVG(1500, 420, "the escalation of the Battle of the Beams")
    steps = [("navigation", "transmission"), ("intercept", "listen, DF"), ("analyse", "modulation, timing"),
             ("understand the", "receiver / operator"), ("jam · imitate", "· spoof"), ("counter-", "countermeasure")]
    w, gap, x0, y0 = 210, 42, 30, 60
    for i, (a, b) in enumerate(steps):
        x = x0 + i * (w + gap)
        col = [BLUE, NAVY, NAVY, ORANGE, RED, GREY][i]
        s.box(x, y0, w, 110, stroke=col)
        s.lines(x + w / 2, y0 + 48, [a, b], 24, weight="bold", colour=col)
        if i < 5:
            s.arrow(x + w + 6, y0 + 55, x + w + gap - 6, y0 + 55)
    s.lines(750, 230, ["Knickebein (1940) → X-Gerät → Y-Gerät: equisignal beams → precise timing/filtering → ranging",
                       "the decisive problem is not transmitter power: it is what the receiver and its operator will do with the waveform"], 23, colour=INK)
    s.path("M 1300 180 L 1300 330 L 240 330 L 240 180", stroke=RED, marker=True, dash="10 8")
    s.text(750, 365, "… and the cycle restarts with the next waveform", 22, colour=RED, style="italic")
    s.write("escalation.svg")


def braid():
    """The braid, 1865-2026: five threads (waves, acoustics, radio/radar, accelerators, signal processing), the documented
    crossings between them (solid arrows: transfer), independent convergence (dashed: co-evolution), the same maths
    without a claimed link (dotted: parallel), and two forks (a strand that splits and rejoins: one goal, two routes,
    both surviving). The time axis is stretched over 1915-1950, where most crossings happen."""
    s = SVG(1720, 745, "the braid: five threads, their crossings and two forks, 1865-2026")   # 1720: room for "software" and the GNU Radio 4.0 logo
    xa, xb = 300, 1450
    knots = [(1860, 0.0), (1915, 0.17), (1950, 0.74), (2026, 1.0)]
    def X(year):
        for (y0, f0), (y1, f1) in zip(knots, knots[1:]):
            if year <= y1:
                return xa + (xb - xa) * (f0 + (f1 - f0) * (year - y0) / (y1 - y0))
        return xb
    VIOLET = "#c9a0ff"
    Y = {"W": 70, "A": 165, "R": 290, "P": 500, "S": 640}
    COL = {"W": VIOLET, "A": "#ffa94d", "R": RED, "P": GREEN, "S": "url(#spg)"}   # S as in the snapshots: cyan (hardware) → gold (software)
    s.add(f'<defs><linearGradient id="spg" gradientUnits="userSpaceOnUse" x1="{X(1945):.1f}" y1="0" x2="{X(2001):.1f}" y2="0">'
          f'<stop offset="0" stop-color="{SP_CYAN}"/><stop offset="0.5" stop-color="{SP_MID}"/><stop offset="1" stop-color="{SP_GOLD}"/></linearGradient></defs>')
    names = {"W": "waves as instruments", "A": "acoustics, arrays", "R": "radio, navigation, radar",
             "P": "accelerators", "S": "signal processing, software"}
    start = {"W": 1865, "A": 1914, "R": 1896, "P": 1923, "S": 1917}
    for k in Y:
        s.add(f'<line x1="{X(start[k]):.1f}" y1="{Y[k]}" x2="{xb}" y2="{Y[k]}" stroke="{COL[k]}" stroke-width="7" stroke-linecap="round"/>')
        s.text(xa - 16, Y[k] + 7, names[k], 19, anchor="end", colour=SP_CYAN if k == "S" else COL[k], weight="bold")
    def fork(lane, y0, y1, dy):
        y, col, xs, xe = Y[lane], COL[lane], X(y0), X(y1)
        s.path(f"M {xs:.1f} {y} C {xs + 30:.1f} {y} {xs + 20:.1f} {y + dy} {xs + 55:.1f} {y + dy} "
               f"L {xe - 55:.1f} {y + dy} C {xe - 20:.1f} {y + dy} {xe - 30:.1f} {y} {xe:.1f} {y}", stroke=col, sw=5)
    fork("R", 1941, 2008, 56)
    fork("P", 1929, 1959, 56)
    def dot(year, lane, off=0):
        s.circle(X(year), Y[lane] + off, 7, fill=INK)
    def label(x, y, text, anchor="middle", colour=INK, size=16, style="normal"):
        s.text(x, y, text, size, anchor=anchor, colour=colour, style=style)
    # waves
    for yr, txt in ((1865, "Maxwell"), (1887, "Hertz"), (1912, "Laue, the Braggs")):
        dot(yr, "W"); label(X(yr), Y["W"] - 16, txt)
    # acoustics
    dot(1916, "A"); label(X(1916) + 12, Y["A"] - 16, "sound ranging: Nordmann, Bull, Tucker, Bragg", anchor="start")
    # radio, navigation, radar
    dot(1898, "R"); label(X(1898), Y["R"] + 28, "Marconi")
    dot(1918, "R"); label(X(1918), Y["R"] - 16, "superhet ×3")
    dot(1932, "R"); dot(1940, "R"); label(X(1940) - 16, Y["R"] + 28, "Lorenz beam → Knickebein, magnetron", anchor="end")
    dot(1945, "R"); label(X(1945) + 8, Y["R"] + 28, "Rad Lab", anchor="start")
    dot(1985, "R"); label(X(1985) + 10, Y["R"] - 16, "TEMPEST", anchor="start")
    label(X(2008) - 6, Y["R"] - 40, "both on approach: ILS + GNSS", anchor="end", colour=COL["R"], style="italic")
    dot(1943, "R", 56); label(X(1950) + 8, Y["R"] + 82, "delays: Gee, LORAN → GNSS", anchor="start", colour=COL["R"])
    # accelerators
    dot(1924, "P"); label(X(1924), Y["P"] - 16, "Ising")
    dot(1928, "P"); label(X(1928) - 6, Y["P"] + 26, "Widerøe", anchor="end")
    dot(1931, "P"); label(X(1931), Y["P"] - 16, "cyclotron")
    dot(1937, "P"); label(X(1937), Y["P"] + 26, "klystron")
    dot(1940, "P"); label(X(1940) + 10, Y["P"] - 16, "Kerst: betatron", anchor="start")
    dot(1947, "P"); label(X(1947), Y["P"] + 26, "Alvarez linac")
    dot(1971, "P"); label(X(1971), Y["P"] + 26, "ISR")
    dot(1981, "P"); label(X(1981) + 2, Y["P"] + 26, "Sp\u0304pS", anchor="start")
    dot(1991, "P"); label(X(1991), Y["P"] - 16, "LEP, LLRF")
    dot(2008, "P"); label(X(2008), Y["P"] - 16, "LHC")
    dot(2013, "P"); label(X(2013) + 4, Y["P"] + 26, "MIM", anchor="start")
    dot(1932, "P", 56); label(X(1932) + 12, Y["P"] + 82, "one big push: Cockcroft–Walton, p + Li 1932", anchor="start", colour=COL["P"])
    label(X(1959), Y["P"] + 104, "rejoined: DC injectors feed RF linacs", anchor="end", colour=COL["P"], style="italic")
    # signal processing
    dot(1918, "S"); label(X(1918), Y["S"] + 28, "Schottky: noise is information")
    dot(1965, "S"); label(X(1965), Y["S"] + 28, "FFT")
    dot(2008, "S"); label(X(2008), Y["S"] + 28, "White Rabbit")
    dot(2026, "S"); label(X(2026) + 12, Y["S"] + 6, "software", anchor="start")
    import base64, io   # the GNU Radio 4.0 logo right of it (author, round 55)
    from PIL import Image
    png = io.BytesIO()
    Image.open(OUT.parent / "media" / "gnuradio-4.0-logo.webp").save(png, "PNG", optimize=True)
    lw = 190; lh = lw * 70 / 364
    s.add(f'<image x="{X(2026) + 92:.1f}" y="{Y["S"] - lh / 2 - 2:.1f}" width="{lw}" height="{lh:.1f}" href="data:image/png;base64,{base64.b64encode(png.getvalue()).decode()}"/>')
    # the crossings
    def link(x0, y0, x1, y1, kind):
        ym = (y0 + y1) / 2
        dash = {"T": "", "C": ' stroke-dasharray="9 6" stroke-linecap="round"', "P": ' stroke-dasharray="2 7" stroke-linecap="round"'}[kind]
        marker = ' marker-end="url(#arrow)"' if kind == "T" else ""
        s.add(f'<path d="M {x0:.1f} {y0:.1f} C {x0:.1f} {ym:.1f} {x1:.1f} {ym:.1f} {x1:.1f} {y1:.1f}" stroke="{INK}" '
              f'stroke-width="3" fill="none"{dash}{marker}/>')
    def note(x, y, text, anchor="middle"):
        s.text(x, y, text, 15, anchor=anchor, colour=GREY, style="italic")
    link(X(1887), Y["W"] + 8, X(1898), Y["R"] - 10, "T"); note(X(1887) - 6, 190, "radio", "end")
    link(X(1912), Y["W"] + 8, X(1916), Y["A"] - 10, "T"); note(X(1912) - 4, 122, "Bragg", "end")
    link(X(1922), Y["R"] + 8, X(1928), Y["P"] - 10, "T"); note(X(1924) - 4, 400, "RF hands energy to ions", "end")
    link(X(1928), Y["P"] + 8, X(1930), Y["P"] + 50, "C"); note(X(1929) - 8, Y["P"] + 82, "Widerøe ‖ Walton", "end")
    link(X(1937), Y["P"] - 8, X(1940), Y["R"] + 10, "T")
    link(X(1945), Y["R"] + 8, X(1947), Y["P"] - 10, "T"); note(X(1947) + 8, 432, "radar's tubes,", "start"); note(X(1947) + 8, 450, "pulsers, receivers", "start")
    link(X(1917), Y["A"] + 8, X(1943), Y["R"] + 46, "P"); note(X(1926), 204, "the same hyperbolae")
    link(X(2013), Y["P"] - 8, X(2010), Y["R"] + 10, "C"); note(X(2010) - 10, 420, "MIM ‖ cochlea", "end")
    # into and out of acoustics (author, round 54; scratchpad braid-r54.md): Fessenden's radio man's sonar (1914), sonar
    # quartz → the crystal oscillator and clock (Cady 1921), Gold's ear as a regenerative receiver (1948), the test-ban
    # seismic arrays → the FFT (1964), proton beams heard in water (1979)
    link(X(1913), Y["R"] - 8, X(1914.2), Y["A"] + 10, "T"); note(X(1913) + 6, Y["R"] + 28, "Fessenden", "start")
    link(X(1920.5), Y["A"] + 8, X(1923.5), Y["R"] - 10, "T"); note(X(1923.5) + 8, Y["R"] - 16, "quartz clocks", "start")
    link(X(1948), Y["R"] - 8, X(1948), Y["A"] + 10, "T"); note(X(1948) - 8, 205, "Gold: the ear, a receiver", "end")
    link(X(1963), Y["A"] + 8, X(1965), Y["S"] - 10, "T"); note(X(1963) - 8, 335, "seismic arrays", "end")
    link(X(1979), Y["P"] - 8, X(1979), Y["A"] + 10, "T"); note(X(1979) + 8, 222, "beams heard in water", "start")
    link(X(2004), Y["P"] + 8, X(2008), Y["S"] - 10, "T")
    link(X(1971), Y["S"] - 8, X(1971), Y["P"] + 36, "T"); note(X(1971) + 8, Y["S"] - 44, "Schottky's noise", "start")
    xg = X(2023)
    s.add(f'<line x1="{xg:.1f}" y1="{Y["A"]}" x2="{xg:.1f}" y2="{Y["S"] - 10}" stroke="{INK}" stroke-width="3" marker-end="url(#arrow)"/>')
    for lane in ("A", "R", "P"):
        s.circle(xg, Y[lane], 6, fill=INK)
    # the legend
    yl, xl = 722, 60
    for kind, txt in (("T", "transfer, documented"), ("C", "co-evolution: found independently"),
                      ("P", "parallel: the same maths"), ("F", "a fork: one goal, two routes")):
        if kind == "F":
            s.add(f'<line x1="{xl}" y1="{yl - 6}" x2="{xl + 66}" y2="{yl - 6}" stroke="{GREY}" stroke-width="4"/>')
            s.path(f"M {xl} {yl - 6} C {xl + 14} {yl - 6} {xl + 10} {yl + 8} {xl + 26} {yl + 8} L {xl + 40} {yl + 8} "
                   f"C {xl + 56} {yl + 8} {xl + 52} {yl - 6} {xl + 66} {yl - 6}", stroke=GREY, sw=4)
        else:
            dash = {"T": "", "C": ' stroke-dasharray="9 6"', "P": ' stroke-dasharray="2 7" stroke-linecap="round"'}[kind]
            marker = ' marker-end="url(#arrow)"' if kind == "T" else ""
            s.add(f'<line x1="{xl}" y1="{yl - 6}" x2="{xl + 66}" y2="{yl - 6}" stroke="{INK}" stroke-width="3"{dash}{marker}/>')
        s.text(xl + 80, yl, txt, 16, anchor="start", colour=GREY)
        xl += 80 + int(8.2 * len(txt)) + 36
    s.write("braid.svg")   # shown whole (round 55); its two click states, braid-0/braid-links, are no longer made (round 56)

def crossing_tags():
    """One small tag per kind of crossing, in the braid's own line styles and legend words, for the slides where a
    crossing happens (widero, betatron, navigation, mim, loop), so that the braid's legend is known before the braid."""
    for kind, txt, name in (("T", "transfer, documented", "crossing-transfer.svg"),
                            ("C", "co-evolution: found independently", "crossing-coevolution.svg"),
                            ("P", "parallel: the same maths", "crossing-parallel.svg")):
        w = 80 + int(8.6 * len(txt)) + 6
        s = SVG(w, 30, f"the braid's {txt}")
        dash = {"T": "", "C": ' stroke-dasharray="9 6"', "P": ' stroke-dasharray="2 7" stroke-linecap="round"'}[kind]
        marker = ' marker-end="url(#arrow)"' if kind == "T" else ""
        s.add(f'<line x1="3" y1="15" x2="66" y2="15" stroke="{INK}" stroke-width="3"{dash}{marker}/>')
        s.text(80, 21, txt, 16, anchor="start", colour=GREY)
        s.write(name)


SP_CYAN, SP_MID, SP_GOLD, RADIO = "#45e3f0", "#eef2e4", "#ffc94d", "#8f9cff"   # the instruments strand: hardware (cyan) → software (gold)
LABEL_FONT = "/usr/share/fonts/truetype/LiberationSans-Regular.ttf"   # only to measure label widths for the placement


def strands(now, act, name, compact=False, here=True, custom=None, recall=()):
    """The simple braid (3+1), shown again at the act boundaries: physics/accelerators, radio/telecom, radar/navigation/EW
    and the instruments strand, twisted as a rope (the strand in front hides the one behind at every crossing). The
    instruments strand turns from cyan (hardware: wire, brass, film, valves) to gold (software) between 1945 and 2001.
    `now` dims the future and draws the "you are here" line; labels are shown for act `act` only, dots for all acts up
    to it. Echo arcs join an old hardware function to the same function as a block today (the GR4 box: the live
    demos). The twist is periodic and illustrative — a crossing here is no claim; the detailed braid (braid.svg) is.
    Labels are placed automatically: the nearest free row above or below, centred on its leader if it fits.
    `recall`: years of older acts' milestones shown again by their short name, in grey (author, 2026-11-13: concise
    labels, older milestones by name only — there will be more and more)."""
    import base64
    from PIL import ImageFont
    font = {sz: ImageFont.truetype(LABEL_FONT, sz) for sz in (16, 18)}
    W, H = (1500, 290) if compact else (1500, 640)   # compact: a strip for the bottom of a slide
    s = SVG(W, H, f"the braid so far: physics and accelerators, radio, radar and the instruments, to {now}")
    xa, xb = 235, 1295
    knots = [(1865, 0.0), (1887, 0.07), (1912, 0.20), (1919, 0.34), (1950, 0.64), (2026, 1.0)]
    def X(year):
        for (y0, f0), (y1, f1) in zip(knots, knots[1:]):
            if year <= y1:
                return xa + (xb - xa) * (f0 + (f1 - f0) * (year - y0) / (y1 - y0))
        return xb
    yc, A = (135, 52) if compact else (285, 88)
    turns, th0 = 3.5, -3 * math.pi / 8
    def th(i, x):
        return th0 + 2 * math.pi * turns * (x - xa) / (xb - xa) + i * math.pi / 2
    def Ys(i, x):
        return yc + A * math.sin(th(i, x))
    def mix(c1, c2, f):
        a, b = [int(c1[k:k + 2], 16) for k in (1, 3, 5)], [int(c2[k:k + 2], 16) for k in (1, 3, 5)]
        return "#" + "".join(f"{round(u + (v - u) * f):02x}" for u, v in zip(a, b))
    g0, g1 = X(1945), X(2001)
    def sp_colour(x):
        f = min(max((x - g0) / (g1 - g0), 0), 1)
        return mix(SP_CYAN, SP_MID, 2 * f) if f < 0.5 else mix(SP_MID, SP_GOLD, 2 * f - 1)
    names = [("physics, accelerators", GREEN), ("radio, telecom", RADIO), ("radar, navigation, EW", RED),
             ("instruments → software", "url(#spg)")]
    xnow = X(min(now, 2026))
    top, bottom = (20, 252) if compact else (40, 585)
    s.add(f'<defs><linearGradient id="spg" gradientUnits="userSpaceOnUse" x1="{g0:.1f}" y1="0" x2="{g1:.1f}" y2="0">'
          f'<stop offset="0" stop-color="{SP_CYAN}"/><stop offset="0.5" stop-color="{SP_MID}"/><stop offset="1" stop-color="{SP_GOLD}"/>'
          f'</linearGradient><clipPath id="past"><rect x="0" y="0" width="{xnow:.1f}" height="{H}"/></clipPath>'
          f'<marker id="arrow-gold" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
          f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{SP_GOLD}"/></marker></defs>')
    # the two world wars, faint: most of the documented crossings fall into them
    for y0, y1, txt in ((1914, 1918.9, "WWI"), (1939, 1945, "WWII")):
        s.add(f'<rect x="{X(y0):.1f}" y="{top}" width="{X(y1) - X(y0):.1f}" height="{bottom - top}" fill="#ffffff" opacity="0.05"/>')
        s.text((X(y0) + X(y1)) / 2, 14 if compact else bottom - 8, txt, 15, colour=GREY, style="italic")
    # the strands as runs, split where they pass from behind to in front: behind first, then in front (no outline)
    runs = []
    for i, (_, col) in enumerate(names):
        pts, cur, x = [], None, xa
        while x <= xb + 0.01:
            front = math.cos(th(i, x)) >= 0
            if cur is not None and front != cur:
                runs.append((cur, col, pts)); pts = pts[-1:]
            cur = front
            pts.append((x, Ys(i, x)))
            x += 3
        runs.append((cur, col, pts))
    def draw(group_attr):
        s.add(f"<g {group_attr}>")
        for front in (False, True):
            for f, col, pts in runs:
                if f == front:
                    d = "M " + " L ".join(f"{u:.1f} {v:.1f}" for u, v in pts)
                    s.add(f'<path d="{d}" stroke="{col}" stroke-width="6" fill="none" stroke-linecap="round"/>')
        s.add("</g>")
    if now < 2026:
        draw('opacity="0.16"')
    draw('clip-path="url(#past)"' if now < 2026 else "")
    for i, (txt, col) in enumerate(names):
        s.text(xa - 16, Ys(i, xa) + 7, txt, 19, anchor="end", colour=col if i < 3 else SP_CYAN, weight="bold")
    # milestones: (year, strand, label, short label (when an older act's echo source), act)
    M = [(1865, 0, "1865 Maxwell", "Maxwell", 1), (1887, 1, "1887 Hertz", "Hertz", 1), (1893, 3, "1890s coherer", "", 1),
         (1895.5, 0, "1895 Röntgen: X-rays", "Röntgen", 1), (1898, 1, "1895–1901 Marconi, Tesla: wireless", "Marconi", 1),
         (1904, 2, "1904 Hülsmeyer: radio echoes", "Hülsmeyer", 1), (1912.5, 0, "1912–13 Laue, the Braggs", "Laue", 1),
         (1915, 2, "1915 sound ranging", "sound ranging", 2),
         (1915.5, 3, "1915 Bull's film", "Bull", 2),
         (1916.5, 3, "1916 Tucker's hot wire", "Tucker", 2),
         (1918, 0, "1918 Schottky noise", "Schottky", 3), (1918.5, 3, "1918 superhet ×3", "superhet", 3),
         (1923, 0, "1922 ray-transformer", "ray-transformer", 3), (1924.5, 0, "1924 Ising", "Ising", 3),
         (1928, 0, "1928 Widerøe linac", "Widerøe", 3), (1929.3, 0, "1929 Walton", "Walton", 3),
         (1932, 0, "1932 Cockcroft–Walton", "Cockcroft–Walton", 3), (1932.5, 2, "1932 Lorenz beam", "Lorenz", 3),
         (1937, 0, "1937 klystron", "klystron", 3), (1940, 2, "1940 magnetron", "magnetron", 3), (1940.5, 0, "1940 betatron", "betatron", 3),
         (1942.5, 2, "1942 Gee, LORAN", "LORAN", 3), (1947, 0, "1947 Alvarez linac", "Alvarez", 3),
         (1943, 3, "1943 matched filter", "matched filter", 4), (1965, 3, "1965 FFT", "FFT", 4), (1985, 2, "1985 TEMPEST", "TEMPEST", 4),
         (1992, 3, "1990s SDR", "SDR", 4), (1995, 2, "1995 GNSS", "GNSS", 4), (2001, 3, "2001 GNU Radio", "GNU Radio", 4),
         (2008, 3, "2008 White Rabbit", "White Rabbit", 4), (2009, 1, "", "", 4), (2013, 0, "2013 MIM", "MIM", 4),
         (1971, 0, "1971 ISR", "ISR", 4), (1981, 0, "1981 Sp\u0304pS", "Sp\u0304pS", 4), (1989, 0, "1989 LEP", "LEP", 4),
         (2008.5, 0, "2008 LHC", "LHC", 4), (2024, 0, "FAIR, FCC? ;-)", "FAIR", 4)]
    # echo arcs: (source year, act, the same function as a block today)
    E = [(1915.5, 2, "ADC + trigger · exp. 1"), (1916.5, 2, "low-pass · exp. 2"),
         (1918.5, 3, "mixer + filter · SDR"), (1943, 4, "correlator · exp. 6")]
    echoes = []   # no echo arcs (author, 2026-11-12): the logo alone closes the last snapshot; E stays for the notes
    sources = {e[0] for e in echoes}
    # label placement: rows above and below the braid, nearest first; obstacles: placed labels, leaders, the GR4 box
    above, below = ([60, 36], [214, 240]) if compact else ([178, 148, 118, 88, 58], [407, 437, 467, 497])
    gw, gh = 186, 186 * 70 / 364                       # the GNU Radio 4.0 logo at the strands' end
    gx, gy = 1310, yc - gh / 2
    rects = [(0, yc - A - 15, 232, yc + A + 15)] + ([(gx - 8, gy - 8, 1500, gy + gh + 8)] if now >= 2026 else [])
    if now < 2026 and here:
        rects.append((xnow - 110, 10, xnow + 110, 38))   # its label; the line itself breaks where a label crosses it
    todo = []
    if custom:   # (year, strand, label, colour): a slide's own selection, instead of the act's milestones
        M = [(year, i, txt, "", act) for year, i, txt, _ in custom]
        todo = [(0, year, i, txt, 18, col) for year, i, txt, col in custom]
    for year, i, txt, short, a in ([] if custom else M):
        if a > act or not txt:
            continue
        if a == act:
            todo.append((0, year, i, txt, 18, INK))
        elif year in sources or (year in recall and short):
            todo.append((1, year, i, short or txt, 16, GREY))
    todo.sort()
    # a depth-first search over (row, anchor) per label, in order of year: the first layout where no label, leader or
    # obstacle overlaps another; nearest row first, the strand's own side first, centred before left or right
    items = []
    for _, year, i, txt, size, col in sorted(todo, key=lambda t: t[1]):
        x, y = X(year), Ys(i, X(year))
        w = font[size].getlength(txt)
        prefer = (above, below) if y < yc else (below, above)
        opts = []
        for rows in prefer:
            for ry in rows:
                for anchor, x0 in (("middle", x - w / 2), ("start", x - 6), ("end", x + 6 - w)):
                    r = (x0 - 4, ry - size + 2, x0 + w + 4, ry + 5)
                    lead = (x, ry + 6, y - 10) if ry < yc else (x, y + 10, ry - size)
                    opts.append((anchor, ry, r, lead))
        items.append((x, txt, size, col, opts))
    fixed = list(rects)
    arcs = []
    for k, (year, a, txt) in enumerate(echoes):   # they rise into the logo from below
        x0 = X(year); y0 = Ys(3, x0); xe = gx + 30 + 36 * k; c = 560 + 12 * k
        P = [(x0, y0 + 9), (x0, c), (xe, c), (xe, gy + gh + 4)]
        arcs.append((P, txt))
    arc_pts = [tuple(sum(w * q[j] for w, q in zip(((1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3), P)) for j in (0, 1))
               for P, _ in arcs for t in [n / 120 for n in range(121)]]
    def static_ok(r, lead):
        x0, y0, x1, y1 = r
        if x0 < 4 or x1 > W - 4:
            return False
        if any(x0 < q[2] and q[0] < x1 and y0 < q[3] and q[1] < y1 for q in fixed):
            return False
        if any(x0 - 2 < px < x1 + 2 and y0 - 2 < py < y1 + 2 for px, py in arc_pts):
            return False
        lx, la, lb = lead
        return not any(q[0] - 3 < lx < q[2] + 3 and la < q[3] and q[1] < lb for q in fixed)
    items = [(x, txt, size, col, [o for o in opts if static_ok(o[2], o[3])]) for x, txt, size, col, opts in items]
    def ok(r, lead, chosen):
        x0, y0, x1, y1 = r
        lx, la, lb = lead
        for c in chosen:
            q, (cx, ca, cb) = c[2], c[3]
            if x0 < q[2] and q[0] < x1 and y0 < q[3] and q[1] < y1:
                return False
            if x0 - 3 < cx < x1 + 3 and y0 < cb and ca < y1:      # their leader through my label
                return False
            if q[0] - 3 < lx < q[2] + 3 and la < q[3] and q[1] < lb:  # my leader through their label
                return False
        return True
    budget, deepest = [100000], [0]
    def search(k, chosen):
        deepest[0] = max(deepest[0], k)
        if k == len(items):
            return chosen
        budget[0] -= 1
        if budget[0] < 0:
            return None
        for opt in items[k][4]:
            if ok(opt[2], opt[3], chosen):
                res = search(k + 1, chosen + [opt])
                if res is not None:
                    return res
        return None
    layout = search(0, [])
    if layout is None:
        empty = [t for _, t, _, _, o in items if not o]
        raise SystemExit(f"{name}: no layout for the labels; no free spot at all for {empty}; "
                         f"stuck at {items[min(deepest[0], len(items) - 1)][1]!r} (order: {[t for _, t, _, _, _ in items]})")
    for (x, txt, size, col, _), (anchor, ry, r, (lx, la, lb)) in zip(items, layout):
        s.add(f'<line x1="{lx:.1f}" y1="{la:.1f}" x2="{lx:.1f}" y2="{lb:.1f}" stroke="{GREY}" stroke-width="1.5" stroke-dasharray="2 4"/>')
        s.text({"middle": x, "start": x - 6, "end": x + 6}[anchor], ry, txt, size, anchor=anchor, colour=col)
    for year, i, txt, short, a in M:
        if a <= act:
            x = X(year)
            s.circle(x, Ys(i, x), 7 if a == act else 5.5, fill=sp_colour(x) if i == 3 else names[i][1], stroke="#1d1d1d", sw=1.5)
    if now >= 2026:
        import io
        from PIL import Image
        png = io.BytesIO()
        Image.open(OUT.parent / "media" / "gnuradio-4.0-logo.webp").save(png, "PNG", optimize=True)   # lunasvg: PNG/JPEG, not WebP
        s.add(f'<image x="{gx}" y="{gy:.1f}" width="{gw}" height="{gh:.1f}" href="data:image/png;base64,{base64.b64encode(png.getvalue()).decode()}"/>')
        for P, txt in arcs:
            (x0, y0), (_, c1), (x2, c2), (x3, y3) = P
            s.add(f'<path d="M {x0:.1f} {y0:.1f} C {x0:.1f} {c1:.1f} {x2:.1f} {c2:.1f} {x3:.1f} {y3:.1f}" '
                  f'stroke="url(#spg)" stroke-width="2.5" fill="none" stroke-dasharray="2 7" stroke-linecap="round" marker-end="url(#arrow-gold)"/>')
    if now < 2026 and here:
        gaps = sorted((r[1] - 3, r[3] + 3) for _, _, r, _ in layout if r[0] < xnow < r[2])
        y = top
        for g0_, g1_ in gaps + [(bottom, bottom)]:
            if g0_ > y:
                s.add(f'<line x1="{xnow:.1f}" y1="{y:.1f}" x2="{xnow:.1f}" y2="{g0_:.1f}" stroke="{ORANGE}" stroke-width="2.5"/>')
            y = max(y, g1_)
        s.text(xnow, 30, f"you are here: {now}", 19, colour=ORANGE, weight="bold")
    # the time axis: stretched where the story is dense
    ya = 264 if compact else 602
    s.add(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{ya}" stroke="{GREY}" stroke-width="2"/>')
    for year in (1865, 1887, 1900, 1914, 1918, 1930, 1939, 1945, 1960, 1980, 2000, 2026):
        s.add(f'<line x1="{X(year):.1f}" y1="{ya - 6}" x2="{X(year):.1f}" y2="{ya + 6}" stroke="{GREY}" stroke-width="2"/>')
        s.text(X(year), ya + (22 if compact else 28), str(year), 15 if compact else 16, colour=GREY)
    s.write(name)


def split_band():
    """Why the MIM beats covering the band: both rows show the same bunch spectrum (head-tail, schematic) shaded behind.
    OFDM (digital) covers it back to back — drawn as Butterworth-like bands in rainbow order, dark red to bright blue —
    for one fast ADC and an FFT. The MIM (cyan, analogue) samples it only at the baseband and at multiples of the RF
    frequency: a bunch shorter than the RF bucket 1/f_RF is fully determined by its spectrum at k·f_RF (sampling, in
    frequency), so the gaps carry nothing new and the bunch is rebuilt in software. Axis in units of f_RF."""
    W, H = 1000, 500
    s = SVG(W, H, "OFDM covers the band back to back; the MIM samples it at multiples of the RF frequency")
    x0, x1, fmax = 130, 985, 8.6
    X = lambda f: x0 + (x1 - x0) * f / fmax
    def spectrum(f):   # a bunch shorter than the RF bucket: |sinc|, its dominant lobe at DC (the ~100 kHz high-pass is invisible here)
        u = 0.55 * f
        return 1.0 if u == 0 else abs(math.sin(math.pi * u) / (math.pi * u))
    smax = max(spectrum(i / 500) for i in range(int(fmax * 500) + 1))
    def area(fn, base, h, n=900):
        pts = [(X(fmax * i / n), base - h * fn(fmax * i / n)) for i in range(n + 1)]
        return f"M {x0} {base} " + " ".join(f"L {u:.1f} {v:.1f}" for u, v in pts) + f" L {x1} {base} Z"
    def shaded(base, h):
        s.add(f'<path d="{area(lambda f: spectrum(f) / smax, base, h)}" fill="{INK}" fill-opacity="0.13" stroke="{INK}" stroke-opacity="0.45" stroke-width="1.8"/>')
    def mix(c1, c2, f):
        a, b = [int(c1[k:k + 2], 16) for k in (1, 3, 5)], [int(c2[k:k + 2], 16) for k in (1, 3, 5)]
        return "#" + "".join(f"{round(u + (v - u) * f):02x}" for u, v in zip(a, b))
    rainbow = [(0.0, "#8b1414"), (0.16, "#e8352f"), (0.33, "#ff9f1c"), (0.5, "#ffe14d"), (0.66, "#5ed36a"), (0.83, "#3fd4e0"), (1.0, "#4d8dff")]
    def colour(t):
        for (t0, c0), (t1, c1) in zip(rainbow, rainbow[1:]):
            if t <= t1:
                return mix(c0, c1, (t - t0) / (t1 - t0))
        return rainbow[-1][1]
    rows = (("OFDM", ("digital",), INK, 200), ("MIM", ("analogue", "revival"), SP_CYAN, 425))
    for name, subs, col, base in rows:
        s.text(x0 - 18, base - 74, name, 34, anchor="end", colour=col, weight="bold")
        for j, sub in enumerate(subs):
            s.text(x0 - 18, base - 44 + 26 * j, sub, 22, anchor="end", colour=col)
        s.add(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{GREY}" stroke-width="1.5"/>')
    # OFDM: back to back, Butterworth-like bands (4th order), rainbow from low to high
    base, h, N = 200, 125, 18
    shaded(base, h)
    d = fmax / N
    for k in range(N):
        fc = d * (k + 0.5)
        band = lambda f, fc=fc: 0.92 / math.sqrt(1 + ((f - fc) / (d / 2)) ** 8)
        col = colour(k / (N - 1))
        s.add(f'<path d="{area(band, base, h, 1800)}" fill="{col}" fill-opacity="0.22" stroke="{col}" stroke-width="2"/>')
    s.text(x1, 30, "covered back to back — every frequency:", 24, anchor="end", colour=GREY, style="italic")
    s.text(x1, 58, "one fast ADC, then an FFT", 24, anchor="end", colour=GREY, style="italic")
    # MIM: only the baseband and k·f_RF
    base, h, half = 425, 125, 0.14
    shaded(base, h)
    for k in range(int(fmax) + 1):
        band = lambda f, k=k: math.exp(-((f - k) / half) ** 8)
        s.add(f'<path d="{area(lambda f: band(f) * spectrum(f) / smax, base, h, 1800)}" fill="{SP_CYAN}" fill-opacity="0.7" stroke="none"/>')
        s.add(f'<path d="{area(lambda f: band(f) * 0.95, base, h, 1800)}" fill="none" stroke="{SP_CYAN}" stroke-width="2"/>')
        s.circle(X(k), base - h * spectrum(k) / smax, 6, fill=INK, stroke="#1d1d1d", sw=1.5)
        s.text(X(k), base + 28, f"{k}", 22, colour=SP_CYAN)
    s.text(x1, 258, "only the baseband and multiples of the RF —", 24, anchor="end", colour=GREY, style="italic")
    s.text(x1, 286, "enough to rebuild a short bunch in software", 24, anchor="end", colour=GREY, style="italic")
    s.text(x1, base + 62, "× the RF frequency: 200 MHz (SPS), 400 MHz (LHC)", 21, anchor="end", colour=GREY)
    s.write("split-band.svg")


def cochlea():
    """The ear as a filter bank: sound → eardrum → ossicles → the cochlea, uncurling from the base (20 kHz) to the apex
    (20 Hz); along it the hair cells, each tuned to its own frequency (coloured from cyan, high, to red, low). Schematic:
    the spiral is 2.6 turns, the frequency map exponential along it (Greenwood, roughly); not to scale."""
    W, H = 640, 330
    s = SVG(W, H, "the cochlea: a filter bank of hair cells, each tuned to its own frequency")
    cy = 172
    for k, r in enumerate((14, 26, 38)):   # the sound arriving
        s.path(f"M {38 + r * 0.35:.1f} {cy - r} A {r} {r} 0 0 1 {38 + r * 0.35:.1f} {cy + r}", stroke=GREY, sw=2.5)
    s.add(f'<line x1="70" y1="{cy - 34}" x2="112" y2="{cy - 34}" stroke="{GREY}" stroke-width="2"/>')
    s.add(f'<line x1="70" y1="{cy + 34}" x2="112" y2="{cy + 34}" stroke="{GREY}" stroke-width="2"/>')
    s.add(f'<ellipse cx="118" cy="{cy}" rx="7" ry="44" fill="{LIGHT}" stroke="{INK}" stroke-width="3"/>')
    s.text(118, cy + 74, "eardrum", 20, colour=INK)
    s.path(f"M 126 {cy - 18} Q 142 {cy - 34} 152 {cy - 8} L 172 {cy + 2} Q 186 {cy - 16} 204 {cy - 2}", stroke=INK, sw=6)
    s.text(165, cy - 46, "ossicles", 18, colour=GREY)
    # the spiral duct, tapering towards the apex
    cx, R0, turns = 405, 128, 2.6
    T = 2 * math.pi * turns
    b = math.log(R0 / 16) / T
    def at(t, off=0.0):   # t: 0 base … 1 apex; off: across the duct, + outwards
        th = t * T
        r = R0 * math.exp(-b * th) + off
        return cx + r * math.cos(math.pi + th), cy + r * math.sin(math.pi + th)
    width = lambda t: 22 * (1 - t) + 7 * t
    n = 400
    outer = [at(i / n, width(i / n) / 2) for i in range(n + 1)]
    inner = [at(i / n, -width(i / n) / 2) for i in range(n + 1)]
    sx0, sy0 = at(0)
    s.add(f'<path d="M 204 {cy - 9} L {sx0:.1f} {sy0 - 9:.1f} L {sx0:.1f} {sy0 + 9:.1f} L 204 {cy + 9} Z" fill="#3a3a3a" stroke="{GREY}" stroke-width="1.5"/>')
    d = "M " + " L ".join(f"{u:.1f} {v:.1f}" for u, v in outer) + " L " + " L ".join(f"{u:.1f} {v:.1f}" for u, v in reversed(inner)) + " Z"
    s.add(f'<path d="{d}" fill="#3a3a3a" stroke="{GREY}" stroke-width="1.5"/>')
    # the hair cells: little bundles on the duct's inner side, coloured by their characteristic frequency
    stops = [(0.0, "#45e3f0"), (0.35, "#8fe3a8"), (0.65, "#ffd866"), (1.0, "#ff8a8a")]
    def colour(t):
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t <= t1:
                f = (t - t0) / (t1 - t0)
                a, bb = [int(c0[k:k + 2], 16) for k in (1, 3, 5)], [int(c1[k:k + 2], 16) for k in (1, 3, 5)]
                return "#" + "".join(f"{round(u + (v - u) * f):02x}" for u, v in zip(a, bb))
        return stops[-1][1]
    m = 64
    for j in range(m):
        t = 0.02 + 0.95 * j / (m - 1)
        x0, y0 = at(t, -width(t) / 2 + 2)
        x1, y1 = at(t, width(t) / 2 - 2)
        ux, uy = (x0 - x1), (y0 - y1)
        L = math.hypot(ux, uy) or 1.0
        ux, uy = ux / L, uy / L
        hl = 9 - 4 * t
        for ang in (-0.35, 0.0, 0.35):   # three stereocilia, fanned
            ca, sa = math.cos(ang), math.sin(ang)
            vx, vy = ux * ca - uy * sa, ux * sa + uy * ca
            s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x1 + vx * hl:.1f}" y2="{y1 + vy * hl:.1f}" stroke="{colour(t)}" stroke-width="2" stroke-linecap="round"/>')
    # the frequency map along the duct: f = 20 kHz · 1000^(-t)
    # labels led out of the spiral: 20 kHz to the left of the base, the others to the right margin
    for f, txt, lx, ly, anchor in ((20000, "20 kHz", 266, 222, "end"), (1000, "1 kHz", 562, 112, "start"),
                                   (100, "100 Hz", 562, 182, "start"), (20, "20 Hz", 562, 252, "start")):
        t = math.log(20000 / f) / math.log(1000)
        x, y = at(min(t, 0.985))
        s.add(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{lx:.1f}" y2="{ly - 6:.1f}" stroke="{GREY}" stroke-width="1.5" stroke-dasharray="2 3"/>')
        s.circle(x, y, 3.5, fill=colour(min(t, 1.0)), stroke="none", sw=0)
        s.text(lx + (4 if anchor == "start" else -4), ly, txt, 20, anchor=anchor, colour=colour(min(t, 1.0)))
    hx, hy = at(0.04, -width(0.04) / 2 - 6)   # a hair bundle on the outer turn, for the note top left
    s.add(f'<line x1="150" y1="66" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{GREY}" stroke-width="1.5" stroke-dasharray="2 3"/>')
    s.text(8, 30, "hair cells: each one tuned", 20, anchor="start", colour=INK)
    s.text(8, 56, "to its own frequency", 20, anchor="start", colour=INK)
    s.text(W - 8, H - 36, "≈ 3,500 channels · 120 dB", 19, anchor="end", colour=GREY, style="italic")
    s.text(W - 8, H - 12, "20 Hz – 20 kHz", 19, anchor="end", colour=GREY, style="italic")
    s.write("cochlea.svg")


def pulse_compression():
    """Experiment 6 in one picture: the known chirp (1 → 8 kHz in 20 ms, coloured from low to high), correlated with
    itself, becomes one sharp peak at the delay — the energy of the whole chirp in ~1/B: T·B = 140, +21 dB."""
    W, H = 560, 230
    s = SVG(W, H, "pulse compression: the known chirp in, one sharp peak out")
    s.add(f'<defs><linearGradient id="chirpg" gradientUnits="userSpaceOnUse" x1="20" y1="0" x2="250" y2="0">'
          f'<stop offset="0" stop-color="{SP_CYAN}"/><stop offset="1" stop-color="{SP_GOLD}"/></linearGradient></defs>')
    base = 120
    pts = []
    for i in range(1201):
        t = i / 1200
        env = math.sin(math.pi * t) ** 0.3
        ph = 2 * math.pi * (3 * t + 0.5 * 21 * t * t)   # schematic: 3 → 24 cycles per window
        pts.append((20 + 230 * t, base - 62 * env * math.sin(ph)))
    s.add(f'<path d="M ' + " L ".join(f"{u:.1f} {v:.1f}" for u, v in pts) + f'" fill="none" stroke="url(#chirpg)" stroke-width="2"/>')
    s.text(135, 30, "the chirp s(t): 1 → 8 kHz, 20 ms", 18, colour=INK)
    s.text(135, 214, "T = 20 ms", 16, colour=GREY, style="italic")
    s.arrow(266, base, 312, base, colour=INK, sw=3)
    s.text(289, base - 16, "s*", 18, colour=INK)
    pts = []
    for i in range(801):
        u = (i / 800 - 0.5) * 16
        y = 1.0 if u == 0 else math.sin(math.pi * u) / (math.pi * u)
        pts.append((330 + 220 * i / 800, base + 50 - 112 * abs(y)))
    s.add(f'<path d="M ' + " L ".join(f"{u:.1f} {v:.1f}" for u, v in pts) + f'" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    s.add(f'<line x1="330" y1="{base + 50}" x2="550" y2="{base + 50}" stroke="{GREY}" stroke-width="1.5"/>')
    s.text(440, 30, "one sharp peak: the delay τ", 18, colour=INK)
    s.text(440, 214, "T·B = 140 → +21 dB", 16, colour=SP_GOLD, style="italic")
    s.write("pulse-compression.svg")


def hayrake_sectors():
    """YE-ZB 'Hayrake' in one picture: the carrier's YE beacon turns at about 2 rpm and keys a different Morse letter into
    each 30° sector (the letters changed daily); the pilot's ZB receiver hears the letter of the sector the aircraft is in,
    and flies the reciprocal bearing home — to a moving airfield. Schematic letters."""
    W = H = 360
    s = SVG(W, H, "YE-ZB 'Hayrake': a Morse letter per 30-degree sector, the pilot flies the reciprocal home")
    cx, cy, R = 180, 186, 140
    letters = "ANDUKGRMWOSI"
    for k in range(12):
        a0, a1 = math.radians(-90 + 30 * k), math.radians(-90 + 30 * (k + 1))
        x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0)
        x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        op = 0.20 if k % 2 == 0 else 0.08
        s.add(f'<path d="M {cx} {cy} L {x0:.1f} {y0:.1f} A {R} {R} 0 0 1 {x1:.1f} {y1:.1f} Z" fill="{GREEN}" fill-opacity="{op}" stroke="{GREY}" stroke-width="1.2"/>')
        am = math.radians(-90 + 30 * k + 15)
        s.text(cx + 108 * math.cos(am), cy + 108 * math.sin(am) + 10, letters[k], 28, colour=GREEN, weight="bold")
    s.text(cx, cy - R - 10, "N", 20, colour=GREY)
    # the 2 rpm rotation, outside the ring
    a0, a1, r = math.radians(-60), math.radians(-20), R + 14
    s.add(f'<path d="M {cx + r * math.cos(a0):.1f} {cy + r * math.sin(a0):.1f} A {r} {r} 0 0 1 {cx + r * math.cos(a1):.1f} {cy + r * math.sin(a1):.1f}" '
          f'stroke="{INK}" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>')
    s.text(W - 6, 34, "2 rpm", 19, anchor="end", colour=INK)
    # the carrier (a flight deck) and its beacon
    s.add(f'<rect x="{cx - 26}" y="{cy - 7}" width="52" height="14" rx="3" fill="{GREY}" transform="rotate(-25 {cx} {cy})"/>')
    s.circle(cx + 6, cy - 4, 4, fill=INK, stroke="none", sw=0)
    # an aircraft in the 'K' sector flies the reciprocal home
    am = math.radians(-90 + 30 * 4 + 15)
    px, py = cx + 70 * math.cos(am), cy + 70 * math.sin(am)
    ang = math.degrees(am) + 180
    s.add(f'<g transform="translate({px:.1f} {py:.1f}) rotate({ang:.1f})"><path d="M 12 0 L -8 -3 L -10 -12 L -14 -12 L -12 -2 L -16 -1 L -16 1 L -12 2 L -14 12 L -10 12 L -8 3 Z" fill="{INK}"/></g>')
    s.add(f'<line x1="{px - 16 * math.cos(am):.1f}" y1="{py - 16 * math.sin(am):.1f}" x2="{cx + 22 * math.cos(am):.1f}" y2="{cy + 22 * math.sin(am):.1f}" stroke="{INK}" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrow)"/>')
    s.write("hayrake-sectors.svg")


def race_clock():
    """The war of the beams as a race clock: a vertical time line, June 1940 → February 1941, one row per click — the
    German guidance in green, the British counter in red (the brief's colours). Written as overlays on one canvas
    (race-clock-0 … -3), so the slide reveals them in identical boxes and the rows line up."""
    W, H, ax = 760, 560, 150
    rows = [("Jun 1940", [("Knickebein: fly the equisignal, drop at the crossing", GREEN), ("found by R. V. Jones's team", GREY)]),
            ("Aug–Oct", [("ASPIRIN: find the modulation, add the dots", RED), ("the beam is not bent — it is misread", GREY)]),
            ("Nov 1940", [("X-Gerät: its receivers filter at 2000 Hz", GREEN), ("BROMIDE jammed at 1500 Hz — then at 2000", RED)]),
            ("Feb 1941", [("Y-Gerät: ranging by an echo", GREEN), ("DOMINO: the BBC's TV transmitter answers, phase-shifted", RED)])]
    ys = [52, 182, 312, 442]
    for k, (date, lines) in enumerate(rows):
        s = SVG(W, H, f"the war of the beams, step {k + 1}: {date}")
        if k == 0:   # the axis, with its end arrow
            s.add(f'<line x1="{ax}" y1="20" x2="{ax}" y2="{H - 30}" stroke="{GREY}" stroke-width="3" marker-end="url(#arrow)"/>')
            s.text(ax, H - 6, "weeks, not years", 18, colour=GREY, style="italic")
        y = ys[k]
        s.circle(ax, y, 9, fill=INK, stroke="#1d1d1d", sw=2)
        s.text(ax - 20, y + 8, date, 24, anchor="end", colour=INK, weight="bold")
        for j, (txt, col) in enumerate(lines):
            s.text(ax + 24, y + 8 + 34 * j, txt, 25 if j == 0 else 22, anchor="start", colour=col)
        s.write(f"race-clock-{k}.svg")


def beams_map_overlays():
    """Transparent overlays on the Knickebein map (media/knickebein-map-dahnielson.svg), one per click of `beams`, in the
    map's own coordinates (its viewBox) so that boxes of the same size line up: 0 a bomber on the Kleve beam towards the
    crossing over Derby; 1 ASPIRIN — a British jammer and the extra dots on the beam; 2 X-Gerät — a director beam from the
    Cherbourg peninsula to Coventry with three timed cross-beams, and BROMIDE's jammer; 3 Y-Gerät — one beam and the
    two-way ranging to the aircraft, DOMINO answering from Alexandra Palace. Green: guidance; red: the counter.
    Positions are approximate (from the map's labels and beams; Coventry, Cassel and Alexandra Palace scaled from
    Derby and London) — schematic, no text."""
    VB = (2550, 5300, 8200, 5600)          # the map cropped to England, the Channel and the Low Countries
    W, H = 820, 560
    def svg(k, body):
        head = (f'<?xml version="1.0" encoding="utf-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB[0]} {VB[1]} {VB[2]} {VB[3]}" '
                f'width="{W}" height="{H}">\n  <title>the war of the beams on the map, step {k}</title>\n'
                f'  <defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
                f'<path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker>'
                f'<marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
                f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{GREEN}"/></marker>'
                f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
                f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{RED}"/></marker></defs>\n')
        (OUT / f"beams-map-{k}.svg").write_text(head + "\n".join("  " + b for b in body) + "\n</svg>\n", encoding="utf-8")
        print(f"beams-map-{k}.svg")
    # the two Knickebein beams, from the map's paths (group translate 2402.64, 2857.6; the Kleve one also scaled 15.2788)
    T = (2402.64, 2857.6)
    kleve = (503.81359 * 15.2788 - 867.01 + T[0], 554.37164 * 15.2788 - 2696.6 + T[1])
    kleve_end = (kleve[0] - 270.76734 * 15.2788, kleve[1] - 100.08379 * 15.2788)
    stoll = (8014.088 + T[0], 3552.8278 + T[1])
    stoll_end = (stoll[0] - 5338.0058, stoll[1] + 990.8159)
    def cross(p1, p2, p3, p4):
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
        return x1 + t * (x2 - x1), y1 + t * (y2 - y1)
    derby = cross(kleve, kleve_end, stoll, stoll_end)
    london = (6311, 8456)
    ky, kx = (london[1] - derby[1]) / 157.0, (london[0] - derby[0]) / 91.0   # map units per km, south and east
    coventry = (derby[0] - 2 * kx, derby[1] + 57 * ky)
    ally = (london[0] - 1 * kx, london[1] - 9 * ky)          # Alexandra Palace, north London
    cherbourg = (5399, 9598)                                  # the Beaumont-Hague dot, the X-Gerät transmitters' peninsula
    cassel = (london[0] + 183 * kx, london[1] + 79 * ky)     # the Y-Gerät station near Cassel
    U = 13.0                                                  # map units per slide pixel (≈ 8000 / 600)
    def plane(x, y, ang, col=INK, size=1.0):
        sc = 0.6 * U * size
        return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({ang:.1f}) scale({sc:.1f})">'
                f'<path d="M 12 0 L -8 -3 L -10 -12 L -14 -12 L -12 -2 L -16 -1 L -16 1 L -12 2 L -14 12 L -10 12 L -8 3 Z" fill="{col}"/></g>')
    def jammer(x, y):
        out = [f'<path d="M {x:.0f} {y:.0f} l {-6 * U:.0f} {14 * U:.0f} l {12 * U:.0f} 0 z" fill="{RED}"/>']
        for r in (10, 17, 24):
            out.append(f'<path d="M {x - r * U * 0.8:.0f} {y - r * U * 0.55:.0f} A {r * U:.0f} {r * U:.0f} 0 0 1 {x + r * U * 0.8:.0f} {y - r * U * 0.55:.0f}" '
                       f'stroke="{RED}" stroke-width="{2.2 * U:.0f}" fill="none" stroke-linecap="round"/>')
        return out
    def heading(a, b):
        return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    def lerp(a, b, t):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    # 0: a bomber rides the Kleve beam towards the crossing
    pk = lerp(kleve, derby, 0.55)
    svg(0, [plane(*pk, heading(kleve, derby), size=1.6), f'<circle cx="{derby[0]:.0f}" cy="{derby[1]:.0f}" r="{4 * U:.0f}" fill="none" stroke="{GREEN}" stroke-width="{2 * U:.0f}"/>'])
    # 1: ASPIRIN — a jammer in England, and the extra dots it lays on the beam
    body = jammer(derby[0] - 55 * kx, derby[1] + 22 * ky)   # one of the Aspirin sites, west of the crossing
    for t in [0.66 + 0.035 * i for i in range(8)]:
        x, y = lerp(kleve, derby, t)
        body.append(f'<circle cx="{x:.0f}" cy="{y + 9 * U:.0f}" r="{1.7 * U:.0f}" fill="{RED}"/>')
    svg(1, body)
    # 2: X-Gerät — a director beam to Coventry and three timed cross-beams; BROMIDE's jammer near the target
    body = [f'<line x1="{cherbourg[0]:.0f}" y1="{cherbourg[1]:.0f}" x2="{coventry[0]:.0f}" y2="{coventry[1]:.0f}" stroke="{GREEN}" stroke-width="{2.5 * U:.0f}" stroke-opacity="0.9"/>']
    for t in (0.55, 0.78, 0.92):
        cx_, cy_ = lerp(cherbourg, coventry, t)
        dx, dy = coventry[0] - cherbourg[0], coventry[1] - cherbourg[1]
        L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
        body.append(f'<line x1="{cx_ - nx * 38 * U:.0f}" y1="{cy_ - ny * 38 * U:.0f}" x2="{cx_ + nx * 38 * U:.0f}" y2="{cy_ + ny * 38 * U:.0f}" '
                    f'stroke="{GREEN}" stroke-width="{1.6 * U:.0f}" stroke-opacity="0.9"/>')
    body.append(f'<circle cx="{coventry[0]:.0f}" cy="{coventry[1]:.0f}" r="{4 * U:.0f}" fill="none" stroke="{GREEN}" stroke-width="{2 * U:.0f}"/>')
    body.append(plane(*lerp(cherbourg, coventry, 0.7), heading(cherbourg, coventry), size=1.6))
    body += jammer(coventry[0] - 32 * kx, coventry[1] + 12 * ky)
    svg(2, body)
    # 3: Y-Gerät — one beam, two-way ranging to the aircraft; DOMINO answers from Alexandra Palace
    tgt = lerp(cassel, derby, 0.62)
    body = [f'<line x1="{cassel[0]:.0f}" y1="{cassel[1]:.0f}" x2="{tgt[0]:.0f}" y2="{tgt[1]:.0f}" stroke="{GREEN}" stroke-width="{2.5 * U:.0f}" stroke-opacity="0.9"/>']
    pa = lerp(cassel, tgt, 0.8)
    off = (0, -12 * U)
    body.append(f'<line x1="{cassel[0] + off[0]:.0f}" y1="{cassel[1] + off[1]:.0f}" x2="{pa[0] + off[0]:.0f}" y2="{pa[1] + off[1]:.0f}" '
                f'stroke="{GREEN}" stroke-width="{1.8 * U:.0f}" stroke-dasharray="{5 * U:.0f} {4 * U:.0f}" marker-start="url(#ag)" marker-end="url(#ag)"/>')
    body.append(plane(*pa, heading(cassel, tgt), size=1.6))
    body += jammer(*ally)
    body.append(f'<line x1="{ally[0]:.0f}" y1="{ally[1] - 26 * U:.0f}" x2="{pa[0] + 10 * U:.0f}" y2="{pa[1] + 6 * U:.0f}" stroke="{RED}" stroke-width="{1.8 * U:.0f}" '
                f'stroke-dasharray="{5 * U:.0f} {4 * U:.0f}" marker-end="url(#arr)"/>')
    svg(3, body)


def time_frequency():
    """Pulses or spectra, in one picture: the same three signals seen in time (left, white) and in frequency (right,
    gold) — a click is a flat wide spectrum, a steady tone one sharp line, a train of bunches a comb of lines under the
    bunch's envelope. The arrows between the halves are the Fourier transform. Few words: the column questions and,
    under each column, who lives there."""
    W, H = 1400, 470
    s = SVG(W, H, "pulses or spectra: the same signals in time and in frequency")
    L0, L1, R0, R1 = 40, 600, 800, 1360
    s.text((L0 + L1) / 2, 34, "time-domain: when?", 30, colour=INK, weight="bold")
    s.text((R0 + R1) / 2, 34, "frequency-domain: which tone?", 30, colour=SP_GOLD, weight="bold")
    rows = [125, 245, 365]
    def poly(pts, col, sw=2.5):
        return f'<path d="M ' + " L ".join(f"{u:.1f} {v:.1f}" for u, v in pts) + f'" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>'
    for y in rows:
        s.add(f'<line x1="{L0}" y1="{y}" x2="{L1}" y2="{y}" stroke="{GREY}" stroke-width="1.2"/>')
        s.add(f'<line x1="{R0}" y1="{y}" x2="{R1}" y2="{y}" stroke="{GREY}" stroke-width="1.2"/>')
        s.arrow(640, y - 30, 760, y - 30, colour=GREY, sw=2.5, both=True)
    s.text(700, rows[0] - 46, "Fourier", 20, colour=GREY, style="italic")
    n = 600
    # 1: a click ↔ a flat, wide spectrum
    y = rows[0]
    s.add(poly([(L0 + (L1 - L0) * i / n, y - 70 * math.exp(-((i / n - 0.3) / 0.008) ** 2)) for i in range(n + 1)], INK))
    s.add(poly([(R0 + (R1 - R0) * i / n, y - 52 * math.exp(-((i / n) / 1.6) ** 2)) for i in range(n + 1)], SP_GOLD))
    # 2: a steady tone ↔ one line
    y = rows[1]
    s.add(poly([(L0 + (L1 - L0) * i / n, y - 35 - 30 * math.sin(2 * math.pi * 14 * i / n)) for i in range(n + 1)], INK, 2))
    xl = R0 + (R1 - R0) * 0.35
    s.add(f'<line x1="{xl:.1f}" y1="{y}" x2="{xl:.1f}" y2="{y - 78}" stroke="{SP_GOLD}" stroke-width="4"/>')
    # 3: a train of bunches ↔ a comb under the bunch's envelope
    y = rows[2]
    pts = []
    for i in range(n + 1):
        t = i / n
        v = sum(math.exp(-((t - c) / 0.012) ** 2) for c in (0.1, 0.3, 0.5, 0.7, 0.9))
        pts.append((L0 + (L1 - L0) * t, y - 70 * v))
    s.add(poly(pts, INK))
    for k in range(1, 15):
        f = k / 15
        h = 70 * math.exp(-(f / 0.55) ** 2)
        x = R0 + (R1 - R0) * f
        s.add(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y - h:.1f}" stroke="{SP_GOLD}" stroke-width="3"/>')
    s.add(poly([(R0 + (R1 - R0) * i / n, y - 70 * math.exp(-((i / n) / 0.55) ** 2)) for i in range(n + 1)], SP_GOLD, 1.2))
    s.text((L0 + L1) / 2, 420, "arrival times, range, timing:", 20, colour=GREY, style="italic")
    s.text((L0 + L1) / 2, 446, "sound ranging, radar pulses, Gee and LORAN, White Rabbit", 20, colour=GREY, style="italic")
    s.text((R0 + R1) / 2, 420, "tuning, Doppler, sidebands:", 20, colour=GREY, style="italic")
    s.text((R0 + R1) / 2, 446, "the superheterodyne, Lorenz and Hayrake, Schottky, the FFT", 20, colour=GREY, style="italic")
    s.write("time-frequency.svg")


def setup():
    """The demo apparatus: four microphones, a sound source, a 4-channel USB interface and a laptop running GR4."""
    s = SVG(1500, 640, "the demonstration set-up")
    # the stage: four microphones on a line, 0.6 m apart (a sound-ranging base in miniature), the source in front of it
    sx, sy, sc = 420, 390, 210   # 1 m = 210 px
    mics = [(-0.9, 0.0), (-0.3, 0.0), (0.3, 0.0), (0.9, 0.0)]
    src = (1.5 * math.cos(math.radians(60)), 1.5 * math.sin(math.radians(60)))
    def P(x, y):
        return sx + x * sc, sy - y * sc
    s.add(f'<rect x="{sx - 1.1 * sc}" y="{sy - 0.25 * sc}" width="{2.2 * sc}" height="{0.5 * sc}" fill="{LIGHT}" stroke="none" rx="20"/>')
    for i, (mx, my) in enumerate(mics):
        x, y = P(mx, my)
        s.circle(x, y, 14, fill=BLUE)
        s.text(x, y + 42, f"mic {i + 1}", 20, colour=BLUE)
        # the acoustic path and its delay
        qx, qy = P(*src)
        s.path(f"M {qx:.1f} {qy:.1f} L {x:.1f} {y:.1f}", stroke=ORANGE, sw=2, dash="6 6")
    qx, qy = P(*src)
    s.add(f'<polygon points="{qx - 18},{qy - 22} {qx + 18},{qy - 22} {qx},{qy + 18}" fill="{RED}" stroke="{INK}" stroke-width="2"/>')
    s.text(qx - 28, qy + 6, "source: drum · tuning fork · speaker (chirp)", 20, anchor="end", colour=RED)
    s.text(sx, sy + 0.25 * sc + 40, "four microphones on a line, 0.6 m apart: a 1.8 m base", 19, colour=GREY)
    # the chain: 4 cables → USB interface → laptop (GR4 flow-graph) → screen
    s.box(940, 150, 220, 110, stroke=NAVY)
    s.lines(1050, 195, ["4-channel USB", "audio interface"], 22, weight="bold", colour=NAVY)
    s.text(1050, 245, "48 kS/s, coherent", 17, colour=GREY)
    jx, jy = sx + 1.1 * sc, sy   # the cable run leaves the stage on the right, like a sound-ranging base's lines to Central
    s.path(f"M {jx:.1f} {jy:.1f} C {jx + 120:.1f} {jy:.1f} 860 205 940 205", stroke=GREY, sw=4, marker=True)
    s.text(jx + 62, jy + 30, "4 cables", 17, colour=GREY)
    s.arrow(1050, 262, 1050, 318)
    s.box(900, 320, 300, 150, stroke=ORANGE, fill="#4a3f1f")
    s.lines(1050, 365, ["laptop: one flow-graph", "running in the slide"], 22, weight="bold", colour=ORANGE)
    s.lines(1050, 420, ["trigger · filter · FFT · phase ·", "correlation · localise"], 17, colour=GREY)
    s.path("M 900 440 C 800 440 760 560 700 580", stroke=GREY, sw=2, marker=True, dash="6 6")
    s.box(520, 560, 180, 70, stroke=RED)
    s.lines(610, 590, ["speaker", "chirp · tone"], 18, colour=RED)
    s.write("setup.svg", crop=(95, 80, 1120, 560))   # the drawing spans x ~110-1200, y 95-630; the slide's subtitle carries the motto


def tdoa_map():
    """Hyperbolae of constant time difference for three microphone pairs crossing at the source."""
    s = SVG(900, 760, "time differences of arrival locate the source where the hyperbolae cross")
    sx, sy, sc = 450, 560, 190
    c = 343.0
    mics = np.array([[-0.9, 0.0], [-0.3, 0.0], [0.3, 0.0], [0.9, 0.0]])   # a line, the source in front of it (y > 0)
    src = 1.5 * np.array([math.cos(math.radians(60)), math.sin(math.radians(60))])
    d = np.linalg.norm(mics - src, axis=1)
    def P(x, y):
        return sx + x * sc, sy - y * sc
    xs, ys = np.meshgrid(np.linspace(-2.2, 2.2, 441), np.linspace(0.02, 2.6, 259))   # the half-plane in front of the base
    # as OpenDigitizer's LocalisationChart draws them live on the same slides: neighbouring pairs in the deck's first
    # three series colours; the microphones in the colours of their live traces (make-workflows.py MIC_COLOURS)
    cols = ["#fdb342", "#268bd2", "#859900"]
    mic_cols = [INK] + cols
    for (i, j), col in zip([(0, 1), (1, 2), (2, 3)], cols):
        dd = np.hypot(xs - mics[i, 0], ys - mics[i, 1]) - np.hypot(xs - mics[j, 0], ys - mics[j, 1]) - (d[i] - d[j])
        # trace the zero contour cheaply: sign changes along rows and columns
        pts = []
        sgn = np.sign(dd)
        rows, colsx = np.where(sgn[:, :-1] * sgn[:, 1:] < 0)
        for r, cc in zip(rows, colsx):
            pts.append((xs[r, cc], ys[r, cc]))
        rows, colsx = np.where(sgn[:-1, :] * sgn[1:, :] < 0)
        for r, cc in zip(rows, colsx):
            pts.append((xs[r, cc], ys[r, cc]))
        for x, y in pts[::1]:
            px, py = P(x, y)
            s.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{col}"/>')
        s.text(60, 70 + 40 * cols.index(col), f"Δt(mic {i + 1}, mic {j + 1}) = {(d[i] - d[j]) / c * 1e3:+.2f} ms", 30, anchor="start", colour=col)
    for i, (mx, my) in enumerate(mics):   # one colour per microphone, as its traces in the live charts (make-workflows.py)
        x, y = P(mx, my)
        s.circle(x, y, 14, fill=mic_cols[i])
        s.text(x, y + 46, f"mic {i + 1}", 28, colour=mic_cols[i])
    qx, qy = P(*src)
    s.add(f'<polygon points="{qx - 14},{qy - 17} {qx + 14},{qy - 17} {qx},{qy + 14}" fill="{RED}" stroke="{INK}" stroke-width="2"/>')
    s.text(qx + 24, qy + 9, "drum", 30, anchor="start", colour=RED)
    s.write("tdoa-map.svg", crop=(40, 25, 760, 600))   # the formula is on the slide; the drawing spans x 60-700, y 40-600


def inference_ladder():
    """Communications → radar → SIGINT → TEMPEST → passive diagnostics: who meant the signal, in a few words each.
    Square, large type: it fills the left column of `unintended` alone (author, 2026-11-13: about twice the size);
    the full sentences are in the notes."""
    s = SVG(690, 660, "who meant the signal: ever less intended")
    rows = [("communications", ["meant for you"], BLUE), ("radar", ["meant to", "come back"], NAVY),
            ("SIGINT", ["meant for", "someone else"], ORANGE), ("TEMPEST", ["never meant", "to leave"], RED),
            ("passive diagnostics", ["nobody meant it:", "a state"], GREEN)]
    for i, (name, what, col) in enumerate(rows):
        y = 8 + i * 130
        s.box(8, y + 22, 300, 72, stroke=col)
        s.text(158, y + 69, name, 29, weight="bold", colour=col)
        y0 = y + 70 - (len(what) - 1) * 21
        for k, line in enumerate(what):
            s.text(330, y0 + 42 * k, line, 37, anchor="start")
    s.path("M 636 24 L 636 640", stroke=GREY, sw=2.5, marker=True)
    s.add(f'<text x="656" y="330" font-size="23" fill="{GREY}" transform="rotate(90 656 330)" text-anchor="middle">ever less intended</text>')
    s.write("inference-ladder.svg")


def bragg_law():
    """Bragg's law, minimal: two lattice planes d apart, two parallel waves from one wavefront (the source), reflected
    to one wavefront (the detector). With d sin θ = λ the lower wave travels exactly 2λ further, so both arrive in
    phase, visible by eye. Only d, λ and θ are marked."""
    s = SVG(900, 480, "Bragg's law: two reflections, in phase")
    lam, th = 36.0, math.radians(30)
    d = lam / math.sin(th)          # 2 λ: the path difference 2 d sin θ is 2 λ
    hx, y1 = 450, 215
    y2 = y1 + d
    ux, uy = math.cos(th), math.sin(th)     # the incoming direction, down-right; the outgoing one is (ux, -uy)
    for y in (y1, y2):
        for c in range(7):
            s.add(f'<circle cx="{210 + c * 80}" cy="{y:.1f}" r="6" fill="{INK}" fill-opacity="0.85"/>')
        s.add(f'<line x1="170" y1="{y:.1f}" x2="730" y2="{y:.1f}" stroke="{GREY}" stroke-width="1" stroke-dasharray="5 7" stroke-opacity="0.6"/>')
    def wave(x1, y1_, x2, y2_, amp=8):
        L = math.hypot(x2 - x1, y2_ - y1_)
        vx, vy = (x2 - x1) / L, (y2_ - y1_) / L
        n = int(L / 2)
        pts = [(x1 + vx * (L * i / n) - vy * amp * math.sin(2 * math.pi * (L * i / n) / lam),
                y1_ + vy * (L * i / n) + vx * amp * math.sin(2 * math.pi * (L * i / n) / lam)) for i in range(n + 1)]
        s.path("M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts), stroke=RED, sw=3)
    L1 = 250
    L2 = L1 + d * math.sin(th)      # the lower wave's legs are longer by λ each: same wavefronts at both ends
    wave(hx - L1 * ux, y1 - L1 * uy, hx, y1); wave(hx, y1, hx + L1 * ux, y1 - L1 * uy)
    wave(hx - L2 * ux, y2 - L2 * uy, hx, y2); wave(hx, y2, hx + L2 * ux, y2 - L2 * uy)
    # the wavefronts: a short line through both start points (source) and both end points (detector)
    for (px, py), label, sign in (((hx - L1 * ux, y1 - L1 * uy), "source", -1), ((hx + L1 * ux, y1 - L1 * uy), "detector", 1)):
        nx, ny = uy * sign, ux           # along the wavefront, from the upper wave's point to the lower wave's: d cos θ away
        span = d * math.cos(th)
        s.add(f'<line x1="{px - nx * 20:.1f}" y1="{py - ny * 20:.1f}" x2="{px + nx * (span + 20):.1f}" y2="{py + ny * (span + 20):.1f}" stroke="{ORANGE}" stroke-width="3"/>')
        s.text(px - nx * 34, py - ny * 34 - 8, label, 20, colour=ORANGE)
    # d, θ, λ
    s.arrow(760, y1, 760, y2, colour=ORANGE, sw=2, both=True)
    s.text(778, (y1 + y2) / 2 + 9, "d", 26, anchor="start", colour=ORANGE)
    s.path(f"M {hx - 50} {y1} A 50 50 0 0 1 {hx - 50 * ux:.1f} {y1 - 50 * uy:.1f}", stroke=ORANGE, sw=2)
    s.text(hx - 76, y1 - 10, "θ", 26, colour=ORANGE)
    ax, ay = hx + 130 * ux, y1 - 130 * uy
    bx, by = hx + (130 + lam) * ux, y1 - (130 + lam) * uy
    s.arrow(ax - 16 * uy, ay - 16 * ux, bx - 16 * uy, by - 16 * ux, colour=ORANGE, sw=2, both=True)
    s.text((ax + bx) / 2 - 28, (ay + by) / 2 - 24, "λ", 26, colour=ORANGE)
    s.text(450, 450, "nλ = 2d sin θ", 30, colour=ORANGE, weight="bold")
    s.write("bragg-law.svg", crop=(150, 15, 670, 455))   # the drawing spans x 170-800, y 38-460: shown as large as its column allows

def embed(rel, width, fmt="JPEG"):
    """A picture from the deck folder as a data URI lunasvg decodes (PNG or JPEG, not WebP), `width` pixels wide;
    returns (uri, height)."""
    import base64, io
    from PIL import Image
    im = Image.open(OUT.parent / rel).convert("RGB")
    h = round(im.size[1] * width / im.size[0])
    buf = io.BytesIO()
    im.resize((width, h), Image.LANCZOS).save(buf, fmt, quality=86)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode(), h


def schottky():
    """Schottky's noise as a spectrum, in the time-frequency figure's idiom: left (white) a pickup's signal as N
    particles pass at random phases — it looks like noise; middle (gold) one particle, a comb at the revolution
    harmonics; right (gold, the click) N particles with a momentum spread: each line a band whose width grows with
    the harmonic h, the betatron sidebands beside it — momentum spread and tune, read off the noise. The slide shows
    the middle and right as one strip, schottky-strip.svg."""
    import random
    W, H = 1400, 400
    P = [(30, 430), (500, 900), (970, 1370)]
    heads = [("time-domain: a pickup, N particles", INK), ("one particle: a comb", SP_GOLD), ("N particles: bands", SP_GOLD)]
    caps = [("random arrival times —", "it looks like noise"), ("a line at every harmonic h", "of the revolution frequency"),
            ("width grows with h · momentum spread,", "the sidebands: the tune")]
    base = 290
    def poly(pts, col, sw=2.5):
        return '<path d="M ' + " L ".join(f"{u:.1f} {v:.1f}" for u, v in pts) + f'" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>'
    def panel(s, k):
        x0, x1 = P[k]
        s.text((x0 + x1) / 2, 34, heads[k][0], 28, colour=heads[k][1], weight="bold")
        s.add(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{GREY}" stroke-width="1.2"/>')
        s.text((x0 + x1) / 2, base + 62, caps[k][0], 21, colour=GREY, style="italic")
        s.text((x0 + x1) / 2, base + 89, caps[k][1], 21, colour=GREY, style="italic")
    s0, s1 = SVG(W, H, "Schottky noise: N particles on a pickup, one particle's comb"), SVG(W, H, "Schottky bands: momentum spread and tune")
    panel(s0, 0); panel(s0, 1); panel(s1, 2)
    rnd = random.Random(1918)
    x0, x1 = P[0]
    for _ in range(140):   # each particle passing: a short pulse at a random time
        x = rnd.uniform(x0 + 4, x1 - 4)
        s0.add(f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base - rnd.uniform(190, 220):.1f}" stroke="{INK}" stroke-width="1.6" opacity="0.85"/>')
    x0, x1 = P[1]
    F = lambda x0, x1, h: x0 + 20 + (x1 - x0 - 40) * h / 8.6
    for h in range(1, 9):
        x = F(x0, x1, h)
        s0.add(f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base - 210}" stroke="{SP_GOLD}" stroke-width="3.5"/>')
        s0.text(x, base + 24, str(h), 18, colour=GREY)
    s0.text(x1 - 6, base + 24, "h", 18, colour=GREY, anchor="end", style="italic")
    x0, x1 = P[2]
    n, sig0, q = 900, 0.022, 0.3
    pts, side = [], []
    for i in range(n + 1):
        f = 0.05 + 8.55 * i / n
        main = sum(math.exp(-0.5 * ((f - h) / (sig0 * h)) ** 2) / (h ** 0.5) for h in range(1, 9))
        sb = sum(0.28 * math.exp(-0.5 * ((f - h - d) / (sig0 * h)) ** 2) / (h ** 0.5) for h in range(1, 9) for d in (-q, q))
        x = x0 + 20 + (x1 - x0 - 40) * f / 8.6
        pts.append((x, base - 210 * main)); side.append((x, base - 210 * sb))
    s1.add(poly(side, NAVY, 1.8))
    s1.add(poly(pts, SP_GOLD, 2.6))
    for h in range(1, 9):
        s1.text(F(x0, x1, h), base + 24, str(h), 18, colour=GREY)
    s1.text(x1 - 6, base + 24, "h", 18, colour=GREY, anchor="end", style="italic")
    hx = F(x0, x1, 7); wd = (x1 - x0 - 40) / 8.6 * sig0 * 7 * 2.4
    s1.add(f'<line x1="{hx - wd:.1f}" y1="{base - 112}" x2="{hx + wd:.1f}" y2="{base - 112}" stroke="{INK}" stroke-width="2" marker-end="url(#arrow)" marker-start="url(#arrow)"/>')
    s1.text(hx, base - 124, "Δp/p", 18, colour=INK)
    sx = F(x0, x1, 3 + q)
    s1.path(f"M {sx + 4:.1f} {base - 70} Q {sx + 40:.1f} {base - 140} {sx + 70:.1f} {base - 165}", stroke=NAVY, sw=1.8)
    s1.text(sx + 74, base - 170, "the tune", 18, colour=NAVY, anchor="start")
    s2 = SVG(W, H, "Schottky noise: one particle's comb, N particles' bands")   # `schottky`'s strip (round 52): middle and right
    s2.parts = s0.parts + s1.parts[4:]
    s2.write("schottky-strip.svg", crop=(480, 0, 910, 400))


AXIS_YEARS = (1885, 1895, 1905, 1915, 1925, 1930, 1935, 1940, 1945, 1950, 1960)
MEDALLION = {"fessenden": (-4, -34), "barkhausen": (6, 34), "whbragg": (-4, -32), "boyle": (0, 30), "nordmann": (-4, -32),
             "reeves": (-6, -34), "jansky": (4, 32), "rocard": (6, 30), "tuve": (0, 34)}   # nudges where two lines start side by side


def portrait(name, fallback=None):
    """the deck's portrait if there is one, else the fallback (None: the initials in a ring)"""
    rel = f"media/portraits/{name}.webp"
    return rel if (OUT.parent / rel).exists() else fallback


# (key, name, nodes [(year, lane)], offset px — unique, so no two lines share a track —, portrait, layer 0/1, end year,
# died early); sources: scratchpad people-r52.md, people-r53.md; W. H. Bragg and the French connection added in round 53
PEOPLE = [   # offsets in 4 px steps, grouped by the lane a career ends on; round 54 adds Hertz, Rutherford and the sonar people
    ("whbragg", "W. H. Bragg", [(1907, "P"), (1912, "W"), (1915.5, "A"), (1919, "W")], -52, "media/portraits/bragg-wh.webp", 1, 1965, False),
    ("wlbragg", "W. L. Bragg", [(1912.5, "W"), (1915.3, "A"), (1919.5, "W")], -48, "media/bragg-wl-nobel-1915.webp", 0, 1965, False),
    ("randall", "Randall", [(1932, "W"), (1940.2, "R"), (1946.5, "W")], -44, "media/portraits/randall.webp", 0, 1965, False),
    ("langevin", "Langevin", [(1915.2, "A")], -40, "langevin", 1, 1925, False),
    ("fessenden", "Fessenden", [(1900, "C"), (1912.5, "A")], -36, "fessenden", 1, 1965, False),
    ("boyle", "Boyle", [(1905, "P"), (1916, "A")], -32, "boyle", 1, 1965, False),
    ("woodab", "A. B. Wood", [(1912, "P"), (1915.6, "A"), (1936, "R"), (1950, "A")], -28, "wood-ab", 1, 1965, False),
    ("piercegw", "G. W. Pierce", [(1904, "C"), (1917, "A"), (1923, "C"), (1927, "A")], -24, "pierce-gw", 1, 1965, False),
    ("barkhausen", "Barkhausen", [(1907, "C"), (1926, "A")], -20, "barkhausen", 1, 1965, False),
    ("hertz", "Hertz", [(1886, "C")], -16, "media/hertz-portrait.webp", 1, 1894, False),
    ("reeves", "Reeves", [(1923, "C"), (1940.5, "R"), (1946, "C")], -12, "reeves", 1, 1965, False),
    ("kompfner", "Kompfner, Pierce", [(1941, "R"), (1951, "C")], -8, "pierce", 1, 1965, False),
    ("blumlein", "Blumlein", [(1924, "C"), (1938.5, "R")], -4, "blumlein", 1, 1942.4, True),
    ("jansky", "Jansky", [(1928, "C"), (1932, "S"), (1935, "C"), (1942, "R")], 0, "jansky", 1, 1950, False),
    ("rutherford", "Rutherford", [(1894.5, "C"), (1896.5, "W"), (1898.5, "P"), (1915.5, "A"), (1919, "P")], 4, "media/portraits/rutherford.webp", 1, 1937, False),
    ("cockcroft", "Cockcroft", [(1924, "P"), (1939.5, "R"), (1946, "P")], 8, "cockcroft", 1, 1965, False),
    ("oliphant", "Oliphant", [(1927, "P"), (1939, "R"), (1943.5, "P")], 12, "oliphant", 1, 1965, False),
    ("mcmillan", "McMillan", [(1932, "P"), (1940.5, "R"), (1941.5, "A"), (1945, "P")], 16, "mcmillan", 1, 1965, False),
    ("touschek", "Touschek", [(1940.5, "R"), (1943.5, "P")], 20, "touschek", 1, 1965, False),
    ("alvarez", "Alvarez", [(1936.5, "P"), (1941, "R"), (1946.5, "P")], 24, "media/portraits/alvarez.webp", 0, 1965, False),
    ("hansen", "Hansen, Varians", [(1934, "P"), (1937.5, "R"), (1947.5, "P")], 28, "media/klystron-1940.webp", 0, 1965, False),
    ("nordmann", "Nordmann", [(1905, "S"), (1914.8, "A"), (1919.5, "S")], 32, "nordmann", 1, 1965, False),
    ("esclangon", "Esclangon", [(1908, "S"), (1914.7, "A"), (1918.5, "S"), (1933, "C"), (1934.5, "S")], 36, "esclangon", 1, 1965, False),
    ("tuve", "Tuve", [(1925, "C"), (1929, "P"), (1941, "R"), (1952, "S")], 40, "tuve", 1, 1965, False),
    ("bowen", "Bowen", [(1930, "W"), (1933.5, "C"), (1936, "R"), (1946, "S")], 44, "bowen", 1, 1965, False),
    ("lovell", "Lovell", [(1936, "P"), (1939.8, "R"), (1945.5, "S")], 48, "lovell", 1, 1965, False),
    ("rocard", "Rocard", [(1928, "C"), (1941.5, "R"), (1946, "S")], 52, "rocard", 1, 1965, False),
]


def people_lines():
    """The people as world-lines between six fields, 1905-1965 (the braid's colours), drawn like a transit map: a
    line runs flat on its lane and hops in a short S-bend at each move; a small portrait at its start, the name at its
    end on the right margin (a cross where a life ends early). Nearly every hop falls in a war band, almost none
    starts there. Two files of one geometry, for a reveal: people-lines-0.svg (lanes, wars, the people of layer 0)
    and people-lines-1.svg (layer 1, drawn over it). Sources: scratchpad people-r52.md, people-r53.md (round 53: the
    French connection, W. H. Bragg; author 2026-11-13: enlarge, clean up, portraits at the start, names at the end)."""
    W, H = 1640, 800
    xa, xb = 330, 1430
    knots = [(1881, xa), (1904, 480), (1925, 700), (1938, 930), (1947, 1200), (1965, xb)]   # stretched where the careers crowd
    def X(year):
        for (y0, x0), (y1, x1) in zip(knots, knots[1:]):
            if year <= y1:
                return x0 + (x1 - x0) * (year - y0) / (y1 - y0)
        return xb
    VIOLET, TEAL = "#c9a0ff", "#66d9c4"
    lanes = {"W": (82, VIOLET, "X-rays, crystals, DNA"), "A": (199, "#ffa94d", "acoustics, sonar"),
             "C": (316, RADIO, "radio, telecom"), "R": (433, RED, "radar, navigation"),
             "P": (552, GREEN, "accelerators, nuclear"), "S": (669, TEAL, "astronomy, radio astronomy")}
    s0, s1 = SVG(W, H, "people as world-lines between the fields, 1905-1965"), SVG(W, H, "people as world-lines, more of them")
    for y0, y1, txt in ((1914, 1918.9, "WWI"), (1939, 1945, "WWII")):
        s0.add(f'<rect x="{X(y0):.1f}" y="8" width="{X(y1) - X(y0):.1f}" height="722" fill="#ffffff" opacity="0.06"/>')
        s0.text((X(y0) + X(y1)) / 2, 746, txt, 17, colour=GREY, style="italic")
    for key, (y, col, name) in lanes.items():
        s0.add(f'<line x1="{xa - 10}" y1="{y}" x2="{xb}" y2="{y}" stroke="{col}" stroke-width="8" opacity="0.45" stroke-linecap="round"/>')
        s0.text(xa - 24, y + 7, name, 21, anchor="end", colour=col, weight="bold")
    s0.add(f'<line x1="{xa}" y1="762" x2="{xb}" y2="762" stroke="{GREY}" stroke-width="2"/>')
    for yr in AXIS_YEARS:
        s0.add(f'<line x1="{X(yr):.1f}" y1="757" x2="{X(yr):.1f}" y2="767" stroke="{GREY}" stroke-width="2"/>')
        s0.text(X(yr), 790, str(yr), 16, colour=GREY)
    hop = 40   # px: the S-bend of a move
    fan = 90   # px: at the right margin the lines fan out to their names (author, round 55: spread the ends)
    tracks = []
    for key, name, nodes, off, pic, layer, end, died in PEOPLE:
        y_end = lanes[nodes[-1][1]][0] + off * 0.85
        tracks.append((round(X(end)), y_end, key))
    label_y = {}
    groups = {}
    for xe, y, key in tracks:
        groups.setdefault(xe, []).append((y, key))
    for xe, group in groups.items():
        group.sort()
        ys = [y for y, _ in group]
        gap = 21 if xe >= xb - 1 else 19
        for _ in range(80):
            for i in range(1, len(ys)):
                if ys[i] - ys[i - 1] < gap:
                    push = (gap - (ys[i] - ys[i - 1])) / 2
                    ys[i - 1] -= push; ys[i] += push
        for (_, key), ty in zip(group, ys):
            label_y[key] = ty
    later = []
    for key, name, nodes, off, pic, layer, end, died in PEOPLE:
        s = s1 if layer else s0
        bold = layer == 0
        colour, sw = (INK, 4) if bold else ("#d8d8d8", 2.6)
        Y = lambda l: lanes[l][0] + off * 0.85
        x, y = X(nodes[0][0]), Y(nodes[0][1])
        d, dots = f"M {x:.1f} {y:.1f}", [(x, y, nodes[0][1])]
        for yr, l in nodes[1:]:
            xn, yn = X(yr), Y(l)
            xs = max(x + 6, xn - hop)
            d += f" L {xs:.1f} {y:.1f} C {(xs + xn) / 2:.1f} {y:.1f} {(xs + xn) / 2:.1f} {yn:.1f} {xn:.1f} {yn:.1f}"
            x, y = xn, yn
            dots.append((x, y, l))
        xe, ty = X(end), label_y[key]
        if xe >= xb - 1 and abs(ty - y) > 0.5:   # fan out to the name
            xf = max(x + 6, xe - fan)
            d += f" L {xf:.1f} {y:.1f} C {xf + fan * 0.5:.1f} {y:.1f} {xf + fan * 0.5:.1f} {ty:.1f} {xe:.1f} {ty:.1f}"
        else:
            d += f" L {xe:.1f} {y:.1f}"
            ty = y if xe >= xb - 1 else ty
        s.add(f'<path d="{d}" stroke="{colour}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>')
        for u, v, l in dots:
            s.circle(u, v, 6 if bold else 5, fill=lanes[l][1], stroke="#1d1d1d", sw=1.8)
        later.append((s, xe, y, ty, name, bold, died, colour))   # the names last, over every line of their layer
        u0, v0 = dots[0][0], dots[0][1]
        r = 22 if bold else 18
        cx = u0 - r - 5
        mdx, mdy = MEDALLION.get(key, (0, 0))
        if mdx or mdy:   # a nudged portrait keeps a thin tie to its line's start
            s.add(f'<line x1="{u0:.1f}" y1="{v0:.1f}" x2="{cx + mdx:.1f}" y2="{v0 + mdy:.1f}" stroke="{colour}" stroke-width="1.2" opacity="0.7"/>')
        cx, v0 = cx + mdx, v0 + mdy
        rel = pic if (pic and "/" in pic) else portrait(pic) if pic else None
        if rel:
            uri, h = embed(rel, 120)
            s.add(f'<clipPath id="m-{key}"><circle cx="{cx:.1f}" cy="{v0:.1f}" r="{r}"/></clipPath>')
            s.add(f'<image x="{cx - r:.1f}" y="{v0 - r * 1.15:.1f}" width="{2 * r}" height="{2 * r * h / 120:.1f}" href="{uri}" clip-path="url(#m-{key})" preserveAspectRatio="none"/>')
        else:
            s.add(f'<circle cx="{cx:.1f}" cy="{v0:.1f}" r="{r}" fill="{LIGHT}"/>')
            s.text(cx, v0 + 5, "".join(w[0] for w in name.replace(",", "").split()[:2]), 13, colour=colour)
        s.add(f'<circle cx="{cx:.1f}" cy="{v0:.1f}" r="{r}" fill="none" stroke="{colour}" stroke-width="1.8"/>')
    for s, xe, y, ty, name, bold, died, colour in later:
        lx = xe + (22 if died else 10)
        if died:
            s.text(xe + 4, y + 7, "†", 20, colour=colour, anchor="start")
        if xe < xb - 20:   # a name inside the picture: a backdrop, so the bundle of lines does not cross it
            if abs(ty - y) > 2:
                s.add(f'<line x1="{xe + 2:.1f}" y1="{y:.1f}" x2="{lx - 2:.1f}" y2="{ty:.1f}" stroke="{colour}" stroke-width="1" opacity="0.6"/>')
            w = 8.6 * len(name) + 6
            s.add(f'<rect x="{lx - 3:.1f}" y="{ty - 11:.1f}" width="{w:.1f}" height="21" rx="4" fill="#262626" opacity="0.92"/>')
        s.text(lx, ty + 6, name, 18 if bold else 16, colour=colour, anchor="start", weight="bold" if bold else "normal")
    s0.write("people-lines-0.svg"); s1.write("people-lines-1.svg")


def radar_loop():
    """The klystron goes to war and comes home (round 52, after the advisor: one loop, one tube): four photographs on a
    circle, clockwise — 1937 the klystron (Stanford: Hansen's cavity, the Varians' tube), radar (the people at the
    tubes, 1945), 1950 the Stanford Mark III linac, 1966 SLAC's klystron gallery — joined by chalk arcs with their
    claim letters; in the centre the second witness, Berkeley's surplus SCR-268s (1947, the Alvarez linac's 200 MHz).
    figures/radar-loop.svg."""
    W, H = 980, 760
    s = SVG(W, H, "the klystron goes to war and comes home")
    def photo(rel, cx, cy, w, cap, cap2="", below=True):
        uri, h = embed(rel, int(w * 1.6))
        h = h / 1.6
        x, y = cx - w / 2, cy - h / 2
        s.add(f'<image x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h:.1f}" href="{uri}"/>')
        ty = y + h + 26 if below else y - 36
        s.text(cx, ty, cap, 21, colour=INK)
        if cap2:
            s.text(cx, ty + 24, cap2, 18, colour=GREY, style="italic")
        return x, y, w, h
    k = photo("media/klystron-1940.webp", 490, 118, 250, "1937 the klystron, Stanford", "Hansen's cavity, the Varians' tube", below=True)
    r = photo("media/radar-operator-1945.webp", 830, 380, 250, "radar, 1940–45", "the people at the tubes")
    m = photo("media/stanford-mark-iii.webp", 490, 590, 130, "1950 Mark III linac", "")
    g = photo("media/slac-klystron-gallery.webp", 150, 380, 250, "1966 SLAC", "245 klystrons, one phase")
    c = photo("media/scr-268-radar.webp", 490, 372, 170, "Berkeley 1947: surplus SCR-268s", "set the Alvarez linac's 200 MHz (T)")
    def arc(x1, y1, x2, y2, bend, label, lx, ly, anchor="middle"):
        mx, my = (x1 + x2) / 2 + bend[0], (y1 + y2) / 2 + bend[1]
        s.add(f'<path d="M {x1} {y1} Q {mx:.1f} {my:.1f} {x2} {y2}" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round" marker-end="url(#arrow)"/>')
        s.text(lx, ly, label, 21, colour=ORANGE, anchor=anchor, style="italic")
    arc(625, 80, 800, 270, (70, -60), "into radar (T)", 835, 120, "start")
    arc(830, 520, 570, 640, (90, 70), "home: the linacs (T)", 850, 690, "middle")
    arc(420, 650, 165, 548, (-60, 80), "more power than radar asked for", 160, 712, "middle")
    arc(150, 255, 355, 80, (-90, -70), "the klystron, out-driven", 20, 70, "start")
    s.write("radar-loop.svg")


def radar_trades():
    """What radar (and space) and the accelerators traded besides the klystron's loop (author, 2026-11-13: superhets in
    BPMs, the other radar crossings, and what went back — the klystron is an accelerator turned RF source; pixel
    detectors in space; sources: scratchpad radar-acc-r52.md, acc-to-radar-r53.md — Shafer AIP 249 1992, Jachim et al.
    IEEE TNS 28 1981, the SLAC Blue Book, Walkinshaw/Fry, Miller Proc. IEE 1954, Borer et al. 1974, JINST 6 T11005;
    Caryotakis SLAC-PUB-7731, Siegman's Ginzton memoir, Fermi LAT, the ISS Timepix monitors 2012, the EISCAT_3D
    tender 2022). Top: radar → accelerators (white); bottom: accelerators → radar and space (gold); claim letters on the
    arrows. figures/radar-trades.svg."""
    W, H = 880, 700
    s = SVG(W, H, "radar and accelerators: what they traded")
    xl, xr = 380, 512   # the left column ends, the right one starts, the arrows run between
    s.text(xl - 6, 34, "radar · space", 29, colour=RED, weight="bold", anchor="end")
    s.text(xr + 6, 34, "accelerators", 29, colour=GREEN, weight="bold", anchor="start")
    rows = [(1918, "1918 superhet receiver", "BPM and LLRF receivers", "C", 1),
            (1938, "1938 radar oscillator", "Hansen's accelerator cavity", "T", -1),
            (1940, "1940 cavity magnetron", "Oliphant's cyclotron lab", "T", -1),
            (1940.1, "1940 the Rad Lab", "Lawrence's cyclotroneers", "T", -1),
            (1943, "1943 monopulse Σ/Δ", "1981 BPM Σ/Δ processors", "T", 1),
            (1946, "wartime magnetron", "1946 S-band · 1953 medical linac", "T", 1),
            (1946.5, "1946 surplus SCR-268s", "1947 Alvarez linac", "T", 1),
            (1948, "1948 Rad Lab pulsers, thyratrons", "1963 SLAC modulators", "T", 1),
            (1959, "1959 BMEWS, Goldstone radars", "linac klystrons", "T", -1),
            (1972, "radar test-set analyser", "1972 ISR: Schottky noise", "C", 1),
            (2003, "2003 radar receiver boards", "Tevatron BPMs", "T", 1),
            (2008, "2008 Fermi gamma-ray telescope", "collider trackers", "T", -1),
            (2012, "2012 ISS radiation monitors", "CERN pixel chips", "T", -1),
            (2022, "2022 EISCAT_3D radar sync", "White Rabbit timing", "T", -1)]   # by year (author, round 54)
    s.add(f'<defs><marker id="arrow-gold" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
          f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{SP_GOLD}"/></marker></defs>')
    y = 84
    for _, left, right, kind, way in sorted(rows):
        col = INK if way > 0 else SP_GOLD
        s.text(xl - 10, y, left, 20, colour=col, anchor="end")
        s.text(xr + 10, y, right, 20, colour=col, anchor="start")
        ya = y - 7
        x0, x1 = (xl, xr) if way > 0 else (xr, xl)
        dash = '' if kind == "T" else ' stroke-dasharray="8 6"'
        s.add(f'<line x1="{x0}" y1="{ya}" x2="{x1}" y2="{ya}" stroke="{col}" stroke-width="2.5"{dash} marker-end="url(#{"arrow" if way > 0 else "arrow-gold"})"/>')
        s.text((xl + xr) / 2, ya - 6, kind, 14, colour=GREY, style="italic")
        y += 46
    s.write("radar-trades.svg")


def stochastic_cooling():
    """van der Meer's stochastic cooling, drawn for `schottky`: a ring of particles, a pickup that hears the beam's
    Schottky noise, an amplifier, and a kicker on the far side reached by the signal's short cut across the ring
    (it arrives with the very particles it measured); beneath, the road to the W and Z (dates: CERN Courier 2011,
    Bramham et al. 1975, the Nobel Prize 1984)."""
    s = SVG(760, 620, "stochastic cooling: hear the noise here, kick it away there")
    cx, cy, r = 380, 262, 190
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GREY}" stroke-width="16" opacity="0.35"/>')
    rng = np.random.default_rng(1968)
    for a in np.linspace(0, 2 * np.pi, 46, endpoint=False):
        rr = r + rng.normal(0, 5)
        s.circle(cx + rr * math.cos(a + rng.normal(0, 0.02)), cy + rr * math.sin(a), 4.5, fill=SP_CYAN, stroke="none", sw=0)
    s.add(f'<path d="M {cx - 60} {cy - r - 30} A {r + 30} {r + 30} 0 0 1 {cx + 60} {cy - r - 30}" fill="none" stroke="{INK}" '
          f'stroke-width="2.5" marker-end="url(#arrow)"/>')
    s.text(cx, cy - r - 44, "the beam", 22, colour=GREY, style="italic")
    pa, ka = math.radians(200), math.radians(-20)   # pickup on the left, kicker on the right, the chord between
    px, py = cx + r * math.cos(pa), cy - r * math.sin(pa)
    kx, ky = cx + r * math.cos(ka), cy - r * math.sin(ka)
    for x, y, txt, ttx, anchor in ((px, py, "pickup", px - 22, "end"), (kx, ky, "kicker", kx + 22, "start")):
        s.box(x - 16, y - 26, 32, 52, fill=LIGHT, stroke=ORANGE, rx=4, sw=3)
        s.text(ttx, y + 8, txt, 26, anchor=anchor, colour=ORANGE, weight="bold")
    mx, my = cx, py + 28
    s.path(f"M {px + 16} {py} L {mx - 34} {my}", stroke=ORANGE, sw=3)
    s.add(f'<path d="M {mx - 34} {my - 26} L {mx + 30} {my} L {mx - 34} {my + 26} z" fill="{LIGHT}" stroke="{ORANGE}" stroke-width="3"/>')
    s.path(f"M {mx + 30} {my} L {kx - 18} {ky}", stroke=ORANGE, sw=3, marker=True)
    s.text(cx, cy - 34, "the signal takes the short cut", 22, colour=ORANGE, style="italic")
    s.text(cx, cy - 6, "and meets the particles it heard", 22, colour=ORANGE, style="italic")
    s.text(px - 22, py + 40, "hear the noise", 21, anchor="end", colour=INK)
    s.text(kx + 22, ky + 40, "kick it away", 21, anchor="start", colour=INK)
    road = [("1968", "the idea"), ("1974", "ISR test"), ("1980", "p\u0304 accumulator"), ("1983", "W, Z"), ("1984", "Nobel")]
    y0, x0, dx = 534, 70, 155
    s.add(f'<line x1="{x0}" y1="{y0}" x2="{x0 + dx * 4}" y2="{y0}" stroke="{GREY}" stroke-width="2.5"/>')
    for k, (yr, what) in enumerate(road):
        x = x0 + dx * k
        s.circle(x, y0, 8, fill=SP_GOLD if k >= 3 else INK, stroke="none", sw=0)
        s.text(x, y0 - 20, yr, 22, colour=INK, weight="bold")
        s.text(x, y0 + 36, what, 21, colour=SP_GOLD if k >= 3 else GREY)
    s.write("stochastic-cooling.svg")


def tempest_spikes():
    """TEMPEST, 1943, in three rows: the plain text into the Bell 131-B2 mixer as teletype (Baudot) code; on the line,
    mixed with the one-time key tape — unreadable; on an oscilloscope across the laboratory, a spike at every step of
    the plain-text relays — readable again. The cipher held; the equipment talked."""
    import random
    W, H = 1400, 430
    s = SVG(W, H, "TEMPEST 1943: the cipher held, the relays radiated the plain text")
    ita2 = {"A": "11000", "T": "00001", "C": "01110", "K": "11110"}
    word = "ATTACK"
    x0, x1 = 330, 1370
    nbits = len(word) * 7                     # start bit, five data bits, stop bit
    bw = (x1 - x0) / nbits
    plain = []
    for ch in word:
        plain += [0] + [int(b) for b in ita2[ch]] + [1]
    rnd = random.Random(131)
    key = []
    for ch in word:
        key += [0] + [rnd.randint(0, 1) for _ in range(5)] + [1]
    cipher = [p_ ^ k if 0 < i % 7 < 6 else p_ for i, (p_, k) in enumerate(zip(plain, key))]
    def wave(bits, ybase, amp, col, sw=3):
        pts, y = [], None
        for i, b in enumerate(bits):
            yy = ybase - amp * b
            if y is not None and yy != y:
                pts.append((x0 + i * bw, y))
            pts.append((x0 + i * bw, yy)); pts.append((x0 + (i + 1) * bw, yy)); y = yy
        s.add('<path d="M ' + " L ".join(f"{u:.1f} {v:.1f}" for u, v in pts) + f'" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>')
    rows = [(110, "plain text in", INK), (245, "on the line", GREY), (390, "a scope, across the lab", RED)]
    for y, label, col in rows:
        s.text(x0 - 18, y - 10, label, 28, anchor="end", colour=col, weight="bold")
    for k, ch in enumerate(word):
        s.text(x0 + (k * 7 + 3.5) * bw, 42, ch, 36, colour=INK, weight="bold")
        s.add(f'<line x1="{x0 + k * 7 * bw:.1f}" y1="52" x2="{x0 + k * 7 * bw:.1f}" y2="400" stroke="{GREY}" stroke-width="1" stroke-dasharray="2 6"/>')
    wave(plain, 110, 46, INK)
    wave(cipher, 245, 46, GREY, 2.5)
    s.text(x1, 290, "mixed with a one-time key: unreadable", 25, anchor="end", colour=GREY, style="italic")
    rng = random.Random(1943)
    trace = []
    n = 4000                                  # fine enough that every spike reaches the same height
    edges = [i for i in range(1, len(plain)) if plain[i] != plain[i - 1]]
    for j in range(n + 1):
        xx = x0 + (x1 - x0) * j / n
        bit = (xx - x0) / bw
        v = rng.gauss(0, 1.6) if j % 3 == 0 else None
        for e in edges:
            d = bit - e
            if 0 <= d < 0.6:
                v = (v or 0) + 58 * math.exp(-d / 0.1) * math.cos(2 * math.pi * d / 0.14)
        if v is not None:
            trace.append((xx, 390 - v))
    s.add('<path d="M ' + " L ".join(f"{u:.1f} {v:.1f}" for u, v in trace) + f'" fill="none" stroke="{RED}" stroke-width="2"/>')
    s.text(x1, 328, "a spike at every step of the plain text: readable", 25, anchor="end", colour=RED, style="italic")
    s.write("tempest-spikes.svg")


for fn in (pipeline, three_domain, escalation, braid, setup, tdoa_map, inference_ladder, bragg_law, split_band, cochlea, pulse_compression, hayrake_sectors, race_clock, beams_map_overlays, time_frequency, schottky, people_lines, radar_loop, tempest_spikes, stochastic_cooling, radar_trades, crossing_tags):
    fn()
strands(1918, 2, "braid-1918.svg", compact=True, here=False,  # a strip under the chain (author, 2026-11-12)
        recall=(1887, 1895.5, 1912.5))                         # Hertz, Röntgen, Laue by name (author, 2026-11-13)
strands(1950, 3, "braid-1950.svg", here=False, recall=(1887, 1895.5, 1912.5, 1915))
strands(2026, 4, "braid-2026.svg")
# under "Pulses or Spectra?": the same braid to 1950, its milestones sorted by view — time (white), frequency (gold)
strands(1950, 3, "braid-duality.svg", compact=True, here=False, custom=[
    (1915.5, 2, "1915 sound ranging: arrival times", INK), (1936, 2, "1936 radar: pulse ranging", INK),
    (1942.5, 2, "1942 Gee, LORAN: delays", INK), (1918.5, 3, "1918 superheterodyne: tuned IF", SP_GOLD),
    (1932.5, 2, "1932 Lorenz beam: modulation", SP_GOLD), (1937, 0, "1937 klystron: resonance", SP_GOLD)])
