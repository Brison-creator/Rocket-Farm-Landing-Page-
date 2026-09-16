#!/usr/bin/env python3
"""
Generates the Rocket Farm logo family as SVG.

All lettering is converted to outlines, so the finished SVGs have no font
dependency — a printer can open them anywhere. Requires `fonttools` and the
Space Grotesk Bold TTF (see brand/README.md for the one-line download).

    python3 brand/generate.py

Writes into the directory this script lives in.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FONT_ENV = os.environ.get("RF_FONT")

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

FONT = FONT_ENV or os.path.join(HERE, "sg-bold.ttf")
FONT_LIGHT = os.environ.get("RF_FONT_LIGHT") or os.path.join(HERE, "sg-light.ttf")
_f = TTFont(FONT)
_gs, _cmap = _f.getGlyphSet(), _f.getBestCmap()
_upem, _hmtx = _f["head"].unitsPerEm, _f["hmtx"]

# The light face is loaded lazily so the rest of the kit still builds without it.
_LIGHT = {}
def _use_light(on):
    """Swap the active glyph source between the bold and light faces."""
    global _gs, _cmap, _upem, _hmtx
    if on:
        if not _LIGHT:
            lf = TTFont(FONT_LIGHT)
            _LIGHT.update(gs=lf.getGlyphSet(), cmap=lf.getBestCmap(),
                          upem=lf["head"].unitsPerEm, hmtx=lf["hmtx"])
        _gs, _cmap, _upem, _hmtx = _LIGHT["gs"], _LIGHT["cmap"], _LIGHT["upem"], _LIGHT["hmtx"]
    else:
        _gs, _cmap = _f.getGlyphSet(), _f.getBestCmap()
        _upem, _hmtx = _f["head"].unitsPerEm, _f["hmtx"]

# ---------------------------------------------------------------- type helpers
def _g(ch):  return _cmap[ord(ch)]
def _adv(ch): return _hmtx[_g(ch)][0]

def _draw(ch, t):
    sp = SVGPathPen(_gs)
    _gs[_g(ch)].draw(TransformPen(sp, t))
    return sp.getCommands()

def tw(s, size, tracking=0.0):
    sc = size / _upem
    return sum(_adv(c) for c in s) * sc + tracking * size * max(0, len(s) - 1)

def fit(s, target_w, tracking=0.0):
    """Point size at which `s` sets to exactly target_w wide."""
    per_em = sum(_adv(c) for c in s) / _upem + tracking * max(0, len(s) - 1)
    return target_w / per_em

def tp(s, size, x=0, y=0, tracking=0.0, anchor="start"):
    """Upright text outlines; y is the baseline."""
    sc = size / _upem
    w = tw(s, size, tracking)
    if anchor == "middle": x -= w / 2
    elif anchor == "end":  x -= w
    out, cx = [], x
    for ch in s:
        if ch != " ":
            out.append(_draw(ch, Transform().translate(cx, y).scale(sc, -sc)))
        cx += _adv(ch) * sc + tracking * size
    return " ".join(p for p in out if p)

def arc(s, size, cx, cy, r, tracking=0.0, top=True, center_deg=None):
    """Text set around a circle. top=True rides the upper arc, letters upright
    outward; top=False rides the lower arc, letters upright toward the centre."""
    sc = size / _upem
    steps = [(_adv(ch) * sc + (tracking * size if i < len(s) - 1 else 0)) / r
             for i, ch in enumerate(s)]
    theta = -sum(steps) / 2.0 + math.radians(center_deg or 0)
    out = []
    for ch, a in zip(s, steps):
        mid = theta + a / 2.0
        if top:
            t = (Transform().translate(cx, cy).rotate(mid).translate(0, -r)
                 .scale(sc, -sc).translate(-_adv(ch) / 2, 0))
        else:
            t = (Transform().translate(cx, cy).rotate(-mid).translate(0, r)
                 .scale(sc, -sc).translate(-_adv(ch) / 2, 0))
        if ch != " ":
            out.append(_draw(ch, t))
        theta += a
    return " ".join(p for p in out if p)

# ------------------------------------------------------------- shape helpers
def circ(cx, cy, r):
    """Circle as a path subpath (so it can punch holes under fill-rule=evenodd)."""
    return (f"M{cx - r:.2f},{cy:.2f} a{r:.2f},{r:.2f} 0 1,0 {2 * r:.2f},0 "
            f"a{r:.2f},{r:.2f} 0 1,0 {-2 * r:.2f},0 Z")

def wedge(x, y, ang_deg, near, far, w_near, w_far):
    """Tapered ray from (x,y) along ang_deg (0 = straight down)."""
    a = math.radians(ang_deg)
    dx, dy = math.sin(a), math.cos(a)
    px, py = math.cos(a), -math.sin(a)      # perpendicular
    pts = [(x + dx * near + px * w_near, y + dy * near + py * w_near),
           (x + dx * far  + px * w_far,  y + dy * far  + py * w_far),
           (x + dx * far  - px * w_far,  y + dy * far  - py * w_far),
           (x + dx * near - px * w_near, y + dy * near - py * w_near)]
    return "M" + " L".join(f"{a_:.2f},{b_:.2f}" for a_, b_ in pts) + " Z"

def ray(cx, cy, a_center, a_half, r0, r1):
    """Radial band between two angles and two radii (0 deg = straight down).
    Defined by ANGLE, so the gap between neighbouring rays never closes up
    near the origin the way fixed pixel widths do."""
    pts = []
    for a, r in ((a_center - a_half, r0), (a_center + a_half, r0),
                 (a_center + a_half, r1), (a_center - a_half, r1)):
        t = math.radians(a)
        pts.append((cx + math.sin(t) * r, cy + math.cos(t) * r))
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"

def star4(cx, cy, r, inner=0.34):
    pts = []
    for i in range(8):
        a = math.radians(i * 45 - 90)
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"

def qbez(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
    dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    return x, y, math.degrees(math.atan2(dy, dx))

def stalk(p0, p1, p2, grains=7, gl=13, gw=5.2, t0=0.26):
    """Rice stalk: stem plus grains riding the curve."""
    stem = (f"M{p0[0]:.1f},{p0[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} "
            f"{p2[0]:.1f},{p2[1]:.1f}")
    out = [f'<path d="{stem}" fill="none" stroke="INK" stroke-width="5.5" stroke-linecap="round"/>']
    for i in range(grains):
        t = t0 + (1 - t0) * i / max(1, grains - 1)
        x, y, ang = qbez(p0, p1, p2, t)
        for side in (-1, 1):
            out.append(
                f'<ellipse cx="0" cy="0" rx="{gl:.1f}" ry="{gw:.1f}" fill="INK" '
                f'transform="translate({x:.1f},{y:.1f}) rotate({ang + side * 38:.1f}) '
                f'translate({gl * 0.78:.1f},0)"/>')
    return "\n    ".join(out)

def rocket(scale=1.0, tilt=0.0, ox=0.0, oy=0.0):
    """Rocket as one evenodd compound path: body + fins + nozzle, porthole
    knocked out so it reads on any background and in one colour."""
    body = ("M0,-150 C18,-118 30,-84 30,-52 L30,0 L-30,0 L-30,-52 "
            "C-30,-84 -18,-118 0,-150 Z")
    finL = "M-30,-44 L-62,10 L-30,-2 Z"
    finR = "M30,-44 L62,10 L30,-2 Z"
    nozzle = "M-21,0 L21,0 L15,15 L-15,15 Z"
    port = circ(0, -74, 15)
    d = " ".join([body, finL, finR, nozzle, port])
    t = f"translate({ox},{oy}) rotate({tilt}) scale({scale})"
    return f'<path d="{d}" fill="INK" fill-rule="evenodd" transform="{t}"/>'

def flame(scale=1.0, tilt=0.0, ox=0.0, oy=0.0):
    d = "M-17,12 C-11,46 -6,62 0,84 C6,62 11,46 17,12 Z"
    t = f"translate({ox},{oy}) rotate({tilt}) scale({scale})"
    return f'<path d="{d}" fill="ACCENT" transform="{t}"/>'

def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">\n{b}\n{body}\n</svg>\n')

# ------------------------------------------------------------------- palettes
NAVY, AMBER, SUNSET, CREAM, MARSH = "#0b1226", "#f5a524", "#e8623c", "#f4efe6", "#3f9d7f"

# =============================================================== MISSION PATCH
def patch(mode="color"):
    C, S = 300, 300
    R_OUT, R_RING, R_IN = 288, 268, 212
    one = mode != "color"
    ink = {"color": CREAM, "dark": NAVY, "light": CREAM}[mode]
    acc = AMBER if mode == "color" else ink
    o = []

    if mode == "color":
        o.append(f'<path d="{circ(C, S, R_OUT)}" fill="{NAVY}"/>')
        o.append(f'<path d="{circ(C, S, R_OUT)} {circ(C, S, R_RING)}" '
                 f'fill="{AMBER}" fill-rule="evenodd"/>')
    else:
        o.append(f'<path d="{circ(C, S, R_OUT)} {circ(C, S, R_OUT - 13)}" '
                 f'fill="{ink}" fill-rule="evenodd"/>')
        o.append(f'<path d="{circ(C, S, R_RING)} {circ(C, S, R_RING - 5)}" '
                 f'fill="{ink}" fill-rule="evenodd"/>')

    # ring lettering
    # top text baseline sits just outside the inner disc so the caps stay
    # inside the navy band instead of running over the outer ring
    o.append(f'<path d="{arc("ROCKET FARM", 52, C, S, R_IN + 12, 0.10, top=True)}" fill="{ink}"/>')
    o.append(f'<path d="{arc("STAY · WATCH · EXPLORE", 31, C, S, R_RING - 18, 0.13, top=False)}" fill="{ink}"/>')
    for d in (0, 180):
        a = math.radians(d)
        o.append(f'<path d="{star4(C + (R_RING - 28) * math.cos(a), S + (R_RING - 28) * math.sin(a), 13)}" fill="{acc}"/>')

    # ---- inner scene ----
    sc = []
    if mode == "color":
        sc.append(f'<path d="{circ(C, S, R_IN)}" fill="#111a33"/>')

    HZ = S + 74                                     # horizon
    bw, bh, by = 232, 50, HZ + 40                   # banner box (needed early)
    half = math.sqrt(max(1.0, R_IN ** 2 - (HZ - S) ** 2))
    if mode == "color":
        sc.append(f'<path d="M{C - half:.1f},{HZ} L{C + half:.1f},{HZ} '
                  f'A{R_IN},{R_IN} 0 0,1 {C - half:.1f},{HZ} Z" fill="{MARSH}" opacity=".95"/>')
    # furrows converging on the horizon
    furrows = []
    for ang in (-64, -46, -28, -10, 10, 28, 46, 64):
        furrows.append(f'<path d="{ray(C, HZ - 2, ang, 4.2, 10, 156)}" '
                       f'fill="{NAVY if mode == "color" else ink}" '
                       f'opacity="{0.55 if mode == "color" else 1}"/>')
    if one:
        sc.append(f'<clipPath id="nb"><path d="{circ(C, S, R_IN)} '
                  f'M{C - bw/2 - 6},{by - 6} h{bw + 12} v{bh + 12} h{-(bw + 12)} Z" '
                  f'clip-rule="evenodd"/></clipPath>')
        sc.append('<g clip-path="url(#nb)">' + "".join(furrows) + '</g>')
    else:
        sc.extend(furrows)
    sc.append(f'<path d="M{C - half:.1f},{HZ} L{C + half:.1f},{HZ}" stroke="{ink}" stroke-width="4"/>')

    # stars
    for sx, sy, sr in ((C - 128, S - 122, 9), (C - 74, S - 166, 6.5), (C + 96, S - 150, 8),
                       (C + 150, S - 74, 6), (C - 158, S - 44, 6.5), (C + 128, S - 6, 5.5)):
        sc.append(f'<path d="{star4(sx, sy, sr)}" fill="{ink}" opacity=".9"/>')

    # contrail sweeping in from the lower left
    sc.append(f'<path d="M{C - 150},{HZ - 6} Q{C - 96},{S + 6} {C - 26},{S + 34}" '
              f'fill="none" stroke="{acc}" stroke-width="7" stroke-linecap="round" '
              f'stroke-dasharray="26 17" opacity=".85"/>')

    # rocket
    sc.append(flame(0.82, 17, C - 6, S + 36).replace("ACCENT", SUNSET if mode == "color" else ink))
    sc.append(rocket(0.82, 17, C - 6, S + 36).replace("INK", ink))

    # flanking rice stalks
    # kept inside the inner disc so the stems are not sliced by the clip
    sc.append(stalk((C - 148, HZ), (C - 178, S + 26), (C - 142, S - 58)).replace("INK", ink))
    sc.append(stalk((C + 148, HZ), (C + 178, S + 26), (C + 142, S - 58)).replace("INK", ink))

    # banner
    sc.append(f'<path d="M{C - bw/2},{by} h{bw} v{bh} h{-bw} Z" fill="{NAVY if mode=="color" else ink}"/>')
    if mode == "color":
        sc.append(f'<path d="M{C - bw/2 + 7},{by + 7} h{bw - 14} v{bh - 14} h{-(bw - 14)} Z" '
                  f'fill="none" stroke="{AMBER}" stroke-width="3"/>')
        tcol = CREAM
    else:
        tcol = "#ffffff00"
        sc.append(f'<path d="M{C - bw/2 + 7},{by + 7} h{bw - 14} v{bh - 14} h{-(bw - 14)} Z" fill="none"/>')
    label = tp("KAPLAN, LA", 29, C, by + bh - 16, 0.14, anchor="middle")
    if mode == "color":
        sc.append(f'<path d="{label}" fill="{tcol}"/>')
    else:
        # knock the words out of the solid banner
        sc[-2] = (f'<path d="M{C - bw/2},{by} h{bw} v{bh} h{-bw} Z {label}" '
                  f'fill="{ink}" fill-rule="evenodd"/>')
        sc.pop()

    # clip the scene to the inner circle
    o.append(f'<clipPath id="in"><path d="{circ(C, S, R_IN)}"/></clipPath>')
    o.append('<g clip-path="url(#in)">\n    ' + "\n    ".join(sc) + "\n  </g>")
    if mode != "color":
        o.append(f'<path d="{circ(C, S, R_IN)} {circ(C, S, R_IN - 5)}" fill="{ink}" fill-rule="evenodd"/>')

    bg = None
    return svg(600, 600, "  " + "\n  ".join(o), bg)

# ====================================================================== ICON
def icon(mode="color"):
    """Rocket whose plume becomes planted rows. Reads at 16px and on a cap."""
    W = 512
    ink = {"color": CREAM, "dark": NAVY, "light": CREAM}[mode]
    acc = AMBER if mode == "color" else ink
    o = []
    cx = 256
    o.append(rocket(1.02, 0, cx, 232).replace("INK", ink))
    # the plume reads as planted rows: three bands per ray, constant gaps
    for ang in (-40, -20, 0, 20, 40):
        for r0, r1 in ((26, 96), (110, 172), (186, 242)):
            o.append(f'<path d="{ray(cx, 240, ang, 7.4, r0, r1)}" fill="{acc}"/>')
    return svg(W, W, "  " + "\n  ".join(o))

# ================================================================== WORDMARK
def wordmark(mode="color", stacked=False):
    ink = {"color": CREAM, "dark": NAVY, "light": CREAM}[mode]
    acc = AMBER if mode == "color" else ink
    if stacked:
        W, H = 620, 300
        o = [rocket(0.46, 0, 310, 112).replace("INK", ink),
             flame(0.46, 0, 310, 112).replace("ACCENT", acc),
             f'<path d="{tp("ROCKET FARM", 84, 310, 214, 0.045, anchor="middle")}" fill="{ink}"/>',
             f'<path d="M{310 - 150},234 h300" stroke="{acc}" stroke-width="4"/>',
             f'<path d="{tp("KAPLAN · LOUISIANA", 26, 310, 272, 0.26, anchor="middle")}" fill="{ink}"/>']
        return svg(W, H, "  " + "\n  ".join(o))
    W, H = 1000, 240
    o = [rocket(0.55, 0, 88, 152).replace("INK", ink),
         flame(0.55, 0, 88, 152).replace("ACCENT", acc),
         f'<path d="{tp("ROCKET FARM", 92, 176, 132, 0.03)}" fill="{ink}"/>',
         f'<path d="M176,158 h{tw("ROCKET FARM", 92, 0.03):.0f}" stroke="{acc}" stroke-width="4"/>',
         f'<path d="{tp("STAY · WATCH · EXPLORE", 27, 178, 198, 0.22)}" fill="{ink}"/>']
    return svg(W, H, "  " + "\n  ".join(o))

# ============================================================== BACK-PRINT TEE
def backprint(mode="dark"):
    """Big back-of-shirt design: arched title over the rocket, plus the
    property's legal land description as the small print."""
    W, H = 900, 1000
    ink = CREAM if mode == "dark" else NAVY
    acc = AMBER if mode == "dark" else NAVY
    C = 450
    # arch wraps down beside the rocket instead of floating above it
    o = [f'<path d="{arc("ROCKET FARM", 100, C, 700, 430, 0.03, top=True)}" fill="{ink}"/>']
    # no separate flame here: the rays are the plume
    o.append(rocket(1.7, 0, C, 620).replace("INK", ink))
    for ang in (-40, -20, 0, 20, 40):
        for r0, r1 in ((22, 102), (118, 190), (206, 252)):
            o.append(f'<path d="{ray(C, 632, ang, 7.2, r0, r1)}" fill="{acc}"/>')
    o.append(f'<path d="M{C-330},900 h660" stroke="{ink}" stroke-width="4"/>')
    o.append(f'<path d="{tp("SEC 17 · T12S · R1E · VERMILION PARISH", 34, C, 954, 0.10, anchor="middle")}" fill="{ink}"/>')
    return svg(W, H, "  " + "\n  ".join(o))

# ============================================================ LAUNCH-STATUS TEE
def scrubbed(mode="dark"):
    """Leans on launch culture, not on anyone's trademarks. Every launch fan
    knows a scrub — and a scrub is an extra night booked."""
    W, H = 900, 830
    ink = CREAM if mode == "dark" else NAVY
    acc = AMBER if mode == "dark" else NAVY
    C = 450
    o = [flame(0.8, 0, C, 196).replace("ACCENT", acc),
         rocket(0.8, 0, C, 196).replace("INK", ink),
         f'<path d="{tp("LAUNCH STATUS", 34, C, 322, 0.30, anchor="middle")}" fill="{acc}"/>']
    big = fit("SCRUBBED", 780, 0.012)
    o.append(f'<path d="{tp("SCRUBBED", big, C, 470, 0.012, anchor="middle")}" fill="{ink}"/>')
    o.append(f'<path d="M{C-390},516 h780" stroke="{acc}" stroke-width="5"/>')
    mid = fit("STAYED ANOTHER NIGHT", 660, 0.04)
    o.append(f'<path d="{tp("STAYED ANOTHER NIGHT", mid, C, 600, 0.04, anchor="middle")}" fill="{ink}"/>')
    o.append(f'<path d="{tp("ROCKET FARM · KAPLAN, LOUISIANA", 30, C, 706, 0.17, anchor="middle")}" fill="{ink}"/>')
    return svg(W, H, "  " + "\n  ".join(o))

# ============================================================== AEROSPACE MARK
def slender(scale=1.0, ox=0.0, oy=0.0, ink="INK"):
    """Tall, thin launch vehicle — the silhouette the site hero uses."""
    body = ("M0,-152 C7,-120 11,-96 11,-72 L11,0 L-11,0 L-11,-72 "
            "C-11,-96 -7,-120 0,-152 Z")
    fwdL, fwdR = "M-11,-106 L-18,-86 L-11,-90 Z", "M11,-106 L18,-86 L11,-90 Z"
    aftL, aftR = "M-11,-26 L-21,4 L-11,-3 Z",     "M11,-26 L21,4 L11,-3 Z"
    skirt = "M-11,0 L11,0 L9,9 L-9,9 Z"
    d = " ".join([body, fwdL, fwdR, aftL, aftR, skirt])
    return (f'<path d="{d}" fill="{ink}" fill-rule="evenodd" '
            f'transform="translate({ox},{oy}) scale({scale})"/>')

def aero(mode="light", stacked=False):
    """Minimal, wide-tracked, monochrome — the modern aerospace register.
    Light weight and open letterspacing, no gradient, no outline."""
    ink = CREAM if mode == "light" else NAVY
    TRACK, SUB = 0.30, 0.34
    if stacked:
        W, H = 700, 420
        C = 350
        o = [slender(0.92, C, 196).replace("INK", ink)]
        _use_light(True)
        name = tp("ROCKET FARM", 62, C, 300, TRACK, anchor="middle")
        nw = tw("ROCKET FARM", 62, TRACK)
        sub = tp("A FIELD FULL OF PEOPLE LOOKING UP", 17, C, 372, SUB, anchor="middle")
        _use_light(False)
        o += [f'<path d="{name}" fill="{ink}"/>',
              f'<path d="M{C - nw/2:.0f},330 h{nw:.0f}" stroke="{ink}" stroke-width="1.1" opacity=".55"/>',
              f'<path d="{sub}" fill="{ink}" opacity=".72"/>']
        return svg(W, H, "  " + "\n  ".join(o))

    W, H = 1240, 250
    o = [slender(0.72, 72, 186).replace("INK", ink)]
    _use_light(True)
    name = tp("ROCKET FARM", 68, 148, 128, TRACK)
    nw = tw("ROCKET FARM", 68, TRACK)
    sub = tp("A FIELD FULL OF PEOPLE LOOKING UP", 17, 150, 186, SUB)
    _use_light(False)
    o += [f'<path d="{name}" fill="{ink}"/>',
          f'<path d="M148,154 h{nw:.0f}" stroke="{ink}" stroke-width="1.1" opacity=".55"/>',
          f'<path d="{sub}" fill="{ink}" opacity=".72"/>']
    return svg(W, H, "  " + "\n  ".join(o))

# ===================================================================== output
FILES = {
    "rocket-farm-patch.svg":            patch("color"),
    "rocket-farm-patch-1c-light.svg":   patch("light"),
    "rocket-farm-patch-1c-dark.svg":    patch("dark"),
    "rocket-farm-icon.svg":             icon("color"),
    "rocket-farm-icon-1c-light.svg":    icon("light"),
    "rocket-farm-icon-1c-dark.svg":     icon("dark"),
    "rocket-farm-wordmark.svg":         wordmark("color"),
    "rocket-farm-wordmark-1c-light.svg":wordmark("light"),
    "rocket-farm-wordmark-1c-dark.svg": wordmark("dark"),
    "rocket-farm-stacked.svg":          wordmark("color", stacked=True),
    "rocket-farm-backprint-dark.svg":   backprint("dark"),
    "rocket-farm-backprint-light.svg":  backprint("light"),
    "rocket-farm-tee-scrubbed-dark.svg":  scrubbed("dark"),
    "rocket-farm-tee-scrubbed-light.svg": scrubbed("light"),
    "rocket-farm-aero-light.svg":        aero("light"),
    "rocket-farm-aero-dark.svg":         aero("dark"),
    "rocket-farm-aero-stacked.svg":      aero("light", stacked=True),
}

if __name__ == "__main__":
    for name, data in FILES.items():
        with open(os.path.join(HERE, name), "w") as fh:
            fh.write(data)
        print(f"  wrote {name} ({len(data):,} bytes)")
