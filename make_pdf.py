#!/usr/bin/env python3
"""
Builds PoolSide-Brand-Playbook.pdf — the version you attach to an email.

Uses the same hotspots.json as the web flipbook, so the product regions are
clickable in the PDF too (Acrobat, Preview, Chrome's viewer, Gmail's viewer).
Page 17 carries the contact link.

    python3 make_pdf.py
"""

import json, os
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "pages")
CFG = json.load(open(os.path.join(HERE, "hotspots.json")))
OUT = os.path.join(HERE, "PoolSide-Brand-Playbook.pdf")

PAGES = 17
# Read from hotspots.json (same file build.py uses) so the PDF and the web
# flipbook can never drift apart. This used to be duplicated here by hand.
CONTACT = CFG["contact"]["url"]
CONTACT_BOX = CFG["contact"]["box"]
CONTACT_PAGE = CFG["contact"].get("page", PAGES)
CTAS = CFG.get("ctas", {})

# 1448 x 1086 px at 150 dpi -> a comfortable landscape page
DPI = 150.0
W = 1448 / DPI * 72.0      # 694.9 pt
H = 1086 / DPI * 72.0      # 521.3 pt

PRODUCTS = CFG["products"]
SPOTS = CFG["pages"]

c = canvas.Canvas(OUT, pagesize=(W, H))
c.setTitle("PoolSide — Brand Playbook")
c.setAuthor("PoolSide")
c.setSubject("PoolSide 10mg THC Drink Mix — company overview, product, compliance and FAQ")
c.setKeywords("PoolSide, THC drink mix, hemp-derived Delta-9, brand playbook")

for i in range(1, PAGES + 1):
    c.drawImage(ImageReader(os.path.join(SRC, f"page-{i:02d}.jpg")),
                0, 0, width=W, height=H)

    spots = list(SPOTS.get(str(i), []))
    links = [(PRODUCTS[s["p"]]["url"], s["box"]) for s in spots]
    if i == CONTACT_PAGE:
        links.append((CONTACT, CONTACT_BOX))

    # Labelled CTAs are HTML in the flipbook, so they are not baked into the page
    # images. Draw them as vector here, otherwise the PDF would show a link with
    # nothing to click on.
    for cta in CTAS.get(str(i), []):
        x0, y0, x1, y1 = cta["box"]
        bx, by = x0 * W, (1 - y1) * H
        bw, bh = (x1 - x0) * W, (y1 - y0) * H
        c.saveState()
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(0.043, 0.145, 0.271)
        c.setLineWidth(0.7)
        c.roundRect(bx, by, bw, bh, bh / 2.0, stroke=1, fill=1)
        label = cta["label"]
        fs = bh * 0.40
        c.setFillColorRGB(0.043, 0.145, 0.271)
        c.setFont("Helvetica-Bold", fs)
        arrow = "  \u2192"
        tw = c.stringWidth(label + arrow, "Helvetica-Bold", fs)
        c.drawString(bx + (bw - tw) / 2.0, by + (bh - fs) / 2.0 + fs * 0.22, label + arrow)
        c.restoreState()
        links.append((cta["url"], cta["box"]))

    for url, (x0, y0, x1, y1) in links:
        # hotspots.json uses a top-left origin; PDF uses bottom-left
        rect = (x0 * W, (1 - y1) * H, x1 * W, (1 - y0) * H)
        c.linkURL(url, rect, relative=0, thickness=0)

    c.showPage()

c.save()
size = os.path.getsize(OUT)
print(f"wrote {OUT}  ({size/1024/1024:.2f} MB, {PAGES} pages)")
if size > 20 * 1024 * 1024:
    print("  WARNING: over 20MB — most mail servers will bounce this as an attachment.")
