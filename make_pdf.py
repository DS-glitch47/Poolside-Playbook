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
CONTACT = "https://drinkpoolside.com/pages/contact"
CONTACT_BOX = [0.795, 0.470, 0.985, 0.765]

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
    if i == PAGES:
        links.append((CONTACT, CONTACT_BOX))

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
