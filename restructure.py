#!/usr/bin/env python3
"""
One-off: insert the "Made For Every Occasion" slide as page 6 and renumber.

The page numbers are baked into the artwork, so they cannot just be relabelled.
Each badge is a different size and sits in a slightly different spot (cap heights
run 23-35px) because every slide was generated separately. So for each page we:

  1. locate its two digit glyphs as connected components,
  2. inpaint them out (TELEA -- the backgrounds are blurred foliage, which is
     forgiving),
  3. stamp the new digits, lifted from the deck's own artwork and scaled to that
     page's measured cap height, at its measured origin and letter gap.

Using glyphs cut from the deck means the typeface matches exactly; there is no
font to source or approximate.

    python3 restructure.py
"""
import json, os
import numpy as np
import cv2
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(HERE, "..", "Raw graphics", "NEW")
PAGES_DIR = os.path.join(HERE, "pages")
W, H = 1448, 1086

OCCASION = os.path.join(RAW, "ChatGPT Image Aug 10, 2026, 10_51_57 PM.png")

# old page index -> new page index. 6 is the newly inserted occasion slide.
SHIFT = {1:1, 2:2, 3:3, 4:4, 5:5, 6:7, 7:8, 8:9, 9:10, 10:11,
         11:12, 12:13, 13:14, 14:15, 15:16, 16:17, 17:18}
REPLACE = {2: "Page 2.png", 4: "Page 4.png", 7: "Page 7.png"}

# badge for the inserted slide, matched to its neighbours (old p6 was cap 30)
OCC_BADGE = dict(x0=38, y0=36, cap=30, gap=5)


def load(path):
    im = Image.open(path).convert("RGB")
    return im if im.size == (W, H) else im.resize((W, H), Image.LANCZOS)


def find_digits(img):
    """two digit glyphs of the page-number badge, left to right"""
    a = np.asarray(img).astype(int)
    sub = a[18:110, 18:150]
    lum = sub.mean(axis=2); sat = sub.max(axis=2) - sub.min(axis=2)
    lab, n = ndimage.label((lum > 195) & (sat < 45))
    g = []
    for k in range(1, n + 1):
        ys, xs = np.where(lab == k)
        w, h = xs.max()-xs.min()+1, ys.max()-ys.min()+1
        if not (8 <= w <= 34 and 19 <= h <= 40):      # a single digit
            continue
        if len(ys) < 0.28 * w * h:
            continue
        g.append((int(xs.min()+18), int(ys.min()+18), int(xs.max()+18), int(ys.max()+18)))
    g.sort()
    if len(g) > 2:
        keep = [g[0]]
        for x in g[1:]:
            if abs(x[1]-keep[0][1]) <= 7 and x[0]-keep[-1][2] <= 24:
                keep.append(x)
        g = keep[:2]
    return g


def build_glyph_library(staged):
    """cut one clean alpha mask per digit out of the deck's own artwork"""
    src = {"0":(2,0), "1":(11,0), "2":(2,1), "3":(3,1), "4":(4,1),
           "5":(5,1), "6":(6,1), "7":(7,1), "8":(8,1), "9":(9,1)}
    lib, pad = {}, 6
    for dig, (pg, gi) in src.items():
        g = find_digits(staged[pg])
        x0, y0, x1, y1 = g[gi]
        im = np.asarray(staged[pg]).astype(float)
        p = im[y0-pad:y1+1+pad, x0-pad:x1+1+pad]
        lum = p.mean(axis=2)
        ring = np.concatenate([lum[:pad].ravel(), lum[-pad:].ravel(),
                               lum[:, :pad].ravel(), lum[:, -pad:].ravel()])
        bg, fg = np.median(ring), np.percentile(lum, 99.5)
        lib[dig] = np.clip((lum-bg)/max(fg-bg, 1e-6), 0, 1)[pad:-pad, pad:-pad]
    return lib


def stamp(im, lib, text, x0, y0, cap, gap):
    x = x0
    for ch in text:
        a = lib[ch]
        nw = max(1, int(round(a.shape[1] * cap / a.shape[0])))
        gl = np.asarray(Image.fromarray((a*255).astype(np.uint8))
                        .resize((nw, cap), Image.LANCZOS)).astype(float)/255.
        reg = im[y0:y0+cap, x:x+nw].astype(float)
        im[y0:y0+cap, x:x+nw] = (reg*(1-gl[...,None]) + 255*gl[...,None]).astype(np.uint8)
        x += nw + gap
    return im


def renumber(img, new_text, lib):
    im = np.asarray(img).astype(np.uint8).copy()
    g = find_digits(img)
    if len(g) != 2:
        raise SystemExit(f"expected 2 digits, found {len(g)} — refusing to guess")
    x0 = min(b[0] for b in g); y0 = min(b[1] for b in g); y1 = max(b[3] for b in g)
    cap = y1 - y0 + 1
    gap = g[1][0] - g[0][2] - 1
    mask = np.zeros((H, W), np.uint8)
    for (a0, b0, a1, b1) in g:
        s = im[b0-3:b1+4, a0-3:a1+4].astype(float)
        lum = s.mean(axis=2); sat = s.max(axis=2)-s.min(axis=2)
        mask[b0-3:b1+4, a0-3:a1+4] |= ((lum > 145) & (sat < 65)).astype(np.uint8)
    mask = cv2.dilate(mask, np.ones((9, 9), np.uint8), 1)
    im = cv2.inpaint(im, mask, 9, cv2.INPAINT_TELEA)
    im = stamp(im, lib, new_text, x0, y0, cap, gap)
    return Image.fromarray(im), cap, gap


def emit(img, idx):
    img.save(f"{PAGES_DIR}/page-{idx:02d}.webp", "WEBP", quality=84, method=6)
    img.save(f"{PAGES_DIR}/page-{idx:02d}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    t = img.copy(); t.thumbnail((300, 300), Image.LANCZOS)
    t.save(f"{PAGES_DIR}/thumb-{idx:02d}.webp", "WEBP", quality=72, method=6)


# ---- stage every old page at its current artwork (with the three replacements)
staged = {}
for old in range(1, 18):
    if old in REPLACE:
        staged[old] = load(os.path.join(RAW, REPLACE[old]))
    else:
        staged[old] = load(f"{PAGES_DIR}/page-{old:02d}.jpg")
print(f"staged 17 pages (replaced artwork on {sorted(REPLACE)})")

lib = build_glyph_library(staged)
print(f"glyph library: {''.join(sorted(lib))}")

# ---- emit the new 18-page sequence
print(f"\n{'old':>4} -> {'new':<4} {'badge':<10} note")
for old in range(1, 18):
    new = SHIFT[old]
    img = staged[old]
    if old == 17:
        note = "closing page, no badge"
    elif new == old:
        note = "number already correct"
    else:
        img, cap, gap = renumber(img, f"{new:02d}", lib)
        note = f"renumbered (cap {cap}px, gap {gap}px)"
    emit(img, new)
    print(f"{old:>4} -> {new:<4} {f'{new:02d}':<10} {note}")

# ---- the inserted slide
occ = np.asarray(load(OCCASION)).astype(np.uint8).copy()
occ = stamp(occ, lib, "06", OCC_BADGE["x0"], OCC_BADGE["y0"], OCC_BADGE["cap"], OCC_BADGE["gap"])
emit(Image.fromarray(occ), 6)
print(f"{'new':>4} -> {6:<4} {'06':<10} occasion slide, badge stamped")
print("\ndone — 18 pages written")
