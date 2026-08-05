# PoolSide Brand Playbook — interactive flipbook

A 17-page, page-turning brand playbook. No frameworks, no subscriptions, no
third-party player — one HTML file plus an images folder. It works as a
standalone page, inside a pop-up on Shopify, and as a link you email.

---

## What's in here

| File / folder | What it is |
|---|---|
| `index.html` | **The flipbook.** Self-contained (CSS + JS inline). Open it anywhere. |
| `pages/` | 17 page images as WebP (2.8 MB total) + JPEG fallbacks + thumbnails. |
| `PoolSide-Brand-Playbook.pdf` | 5.6 MB, 17 pages, **product links clickable inside the PDF**. This is the email attachment. |
| `hotspots.json` | Source of truth for every clickable region. Edit this, not the HTML. |
| `build.py` | Regenerates `index.html` from `hotspots.json`. |
| `make_pdf.py` | Regenerates the PDF from the same hotspot data. |
| `shopify/popup-button.html` | Button + modal. Paste into Shopify for the pop-up route. |
| `shopify/brand-playbook-page.html` | Full-page embed. Paste into a Shopify page. |
| `_demo-popup.html` | Local-only test harness for the pop-up. Do not deploy. |

---

## What it does

- **Page-turn animation** — real CSS 3D, turns on its left edge with a shading pass.
- **Click the page** to go forward; arrows, `←` `→`, swipe, and a scrubber all work.
- **17 clickable product regions** — every pouch and the 12-pack carton link to the
  right product page. A pulsing pin marks each one so people know to tap.
- **Page 17** links to `/pages/contact` (the "Let's Connect" block), and a
  "Get in touch with our team" button appears when you reach the last page.
- **Page picker** — grid of all 17 pages.
- **Deep links** — `…/#p=7` opens straight to page 7. Handy in emails and DMs.
- Fullscreen, PDF download, keyboard and screen-reader support, and a
  `prefers-reduced-motion` path that skips the animation.

---

## Deploying it — pick one

### Route A — host the flipbook, embed it on Shopify *(recommended)*

Shopify can't host a standalone HTML page (Content → Files only accepts assets,
not pages), so the flipbook lives on a static host and Shopify frames it. Free,
takes about ten minutes, and gives you one URL that serves the website *and* your
emails.

1. **Upload this folder** to any static host. [Cloudflare Pages](https://pages.cloudflare.com)
   and [Netlify](https://app.netlify.com/drop) both take a drag-and-drop of the
   whole folder, free, no build step.
2. **Point a subdomain at it** — e.g. `playbook.drinkpoolside.com`. Both hosts
   walk you through the CNAME. Using your own subdomain (rather than
   `something.netlify.app`) is worth it: it looks right in an email and keeps
   the brand consistent.
3. **Pop-up:** paste `shopify/popup-button.html` into a Custom Liquid section
   (Customize → Add section → Custom Liquid), change `PLAYBOOK_URL` at the
   bottom to your subdomain, and put the button wherever you want it. You can
   also add `class="ps-playbook-open"` to any button you already have.
4. **Its own page:** Online Store → Pages → Add page → title it *Brand Playbook*,
   click the `<>` button in the editor, and paste
   `shopify/brand-playbook-page.html` (again, change `PLAYBOOK_URL`).

You can do both — the same hosted flipbook powers the pop-up and the page.

### Route B — pop-up only, no separate page

Just steps 1–3 above. Skip the Shopify page entirely and put the button on your
homepage, your product pages, or in the footer.

### Route C — email only

You don't need any of the website work. Host it (step 1) and send the link, or
just attach the PDF. See below.

---

## Emailing it

**An interactive flipbook cannot run inside an email.** Every mail client
(Gmail, Outlook, Apple Mail) strips JavaScript and iframes — this is a hard limit
of email, not of this build. So there are exactly two things that work, and
you have both:

1. **Send the link** — best option. Recipients get the real flipbook with working
   product links. Deep-link if useful: `playbook.drinkpoolside.com/#p=15` drops a
   retailer straight onto "Why Retailers Love PoolSide".
2. **Attach `PoolSide-Brand-Playbook.pdf`** — 5.6 MB, comfortably under the 20–25 MB
   limit most mail servers enforce. The product links and the contact link are
   live inside the PDF too.

Best practice is both: link in the body, PDF attached for whoever wants to keep it.

> Sample copy:
>
> Hi Sam — here's the PoolSide brand playbook: everything on the product, our
> nano-soluble tech, compliance and margins in 17 pages.
> **Flip through it here:** https://playbook.drinkpoolside.com
> I've attached a PDF as well if that's easier. Any questions, just reply.

---

## Updating a page

Say page 6 gets redesigned:

1. Drop the new artwork in `../Raw graphics/NEW/Page 6.png` (**1448 × 1086**, exactly —
   the pages must all match or the flipbook will letterbox one of them).
2. Regenerate that page's assets:
   ```bash
   cd "/Users/davinspurrier/Desktop/Poolside/Brand Playbook"
   python3 -c "
   from PIL import Image
   i=6
   im=Image.open(f'Raw graphics/NEW/Page {i}.png').convert('RGB').resize((1448,1086), Image.LANCZOS)
   im.save(f'flipbook/pages/page-{i:02d}.webp','WEBP',quality=84,method=6)
   im.save(f'flipbook/pages/page-{i:02d}.jpg','JPEG',quality=86,optimize=True,progressive=True)
   t=im.copy(); t.thumbnail((300,300), Image.LANCZOS)
   t.save(f'flipbook/pages/thumb-{i:02d}.webp','WEBP',quality=72,method=6)
   "
   ```
3. If the product moved on that page, update its box in `hotspots.json`.
4. Rebuild and re-upload:
   ```bash
   cd flipbook && python3 build.py && python3 make_pdf.py
   ```

### Moving a hotspot

`hotspots.json` boxes are `[x0, y0, x1, y1]` as **fractions of the page** (0–1),
measured from the top-left. So `[0.5, 0.25, 0.75, 0.8]` starts halfway across,
a quarter down, and covers a quarter of the width. Change the numbers, run
`python3 build.py`, reload. Nothing else to touch.

---

## One thing worth fixing on the store

The Mango product URL is:

```
/products/poolside-flavorless-thc-drink-mix-10mg-copy
```

It was duplicated from the Flavorless listing and the `-copy` handle stuck. It
works fine and every link here points at it correctly — but it reads as a
mistake to anyone who looks at the address bar, and it's poor SEO for the word
"mango". If you change the handle in Shopify to
`poolside-mango-thc-drink-mix-10mg`, Shopify will offer to create a redirect —
accept it, then update the two `mango` URLs in `hotspots.json` and re-run
`build.py` and `make_pdf.py`.
