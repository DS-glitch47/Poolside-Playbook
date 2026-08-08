#!/usr/bin/env python3
"""
Builds index.html for the PoolSide Brand Playbook flipbook.

Source of truth for the clickable product regions is hotspots.json — edit that,
re-run this script, and index.html is regenerated. Hotspot data is INLINED into
the HTML (not fetched) so the flipbook also works when opened directly from
disk with file:// , e.g. straight out of a zip a retailer was emailed.

    python3 build.py
"""

import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "hotspots.json")))
OUT = os.path.join(HERE, "index.html")

PAGES = 17
PW, PH = 1448, 1086

TITLE = "PoolSide — Brand Playbook"
DESC = ("The PoolSide brand playbook: our mission, what PoolSide is, nano-soluble "
        "10mg hemp-derived Delta-9 THC drink mix, flavors, ingredients, compliance and FAQ.")
SITE = "https://drinkpoolside.com"
CONTACT = "https://drinkpoolside.com/pages/contact"

# Per-page alt text — real descriptions matter for SEO and screen readers.
ALT = {
    1:  "Cover — PoolSide Company Overview. Flavorless and Mango 10mg THC drink mix pouches beside a pool at sunset.",
    2:  "Our Mission — a letter from founder and CEO Aaron King on why PoolSide was created: adults want the benefits of THC without smoking, in a low dose, fast acting drink mix.",
    3:  "What is PoolSide? — a premium fast-acting hemp-derived THC beverage enhancer that turns any drink into a THC-infused experience. 10mg Active Delta-9 THC per pouch, 0% alcohol, 0 calories, 0 sugar. Fast acting 15 minute onset, add to any drink, portable and convenient, consistent 10mg dose.",
    4:  "Why Consumers Love PoolSide — six reasons: fast-acting water-soluble nano technology with effects in as little as 10 to 15 minutes; mixes with any beverage; small and portable enough to take anywhere; a smoke-free option with no odor or equipment; a simple, consistent measured serving; and great value.",
    5:  "Why PoolSide Exists — alcohol consumption is declining, more adults want approachable alternatives, growth in THC beverages is accelerating and consumers are moving away from smoking. PoolSide is the future of social experiences.",
    6:  "What is Delta-9 THC? — PoolSide contains 10mg active hemp-derived Delta-9 THC per pouch. Every batch is third-party lab tested with a Certificate of Analysis, covering cannabinoid potency, pesticides, residual solvents, heavy metals, mycotoxins, pathogenic microbiology, diacetyl and vitamin E acetate.",
    7:  "Nano-Soluble Technology — traditional THC versus PoolSide nano technology: mixes evenly in any beverage, smooth clean drinking experience, 10 to 15 minute onset, more efficient absorption and no oily residue.",
    8:  "Why PoolSide is Legal — made with hemp-derived Delta-9 THC under the 2018 Farm Bill, which defines hemp as containing no more than 0.3% Delta-9 THC on a dry weight basis. Federally compliant, tested, state compliant and manufactured to industry standards.",
    9:  "Our Flavors — Flavorless, tasteless and mixes perfectly into any drink, best with juice, soda, coffee or mocktails; and Mango, a tropical refreshing mango flavor that pairs with any drink, best with water, juice, soda or mocktails.",
    10: "Ingredients — purified water, citric acid, sodium benzoate, potassium sorbate, ascorbic acid and hemp-derived Delta-9 THC. Zero alcohol, zero calories, zero sugar.",
    11: "Nutrition Facts — 0 calories per pouch, 10mg hemp-derived Delta-9 THC as the active ingredient.",
    12: "Directions For Use — tear open the pouch, pour into 8 to 16 fl oz of your beverage, stir or shake well, enjoy responsibly. Do not exceed one pouch in 24 hours.",
    13: "Safety Information — 21+ only, keep out of reach of children and pets, do not drive, not for use during pregnancy, may cause a positive drug test, store in a cool dry place.",
    14: "Compliance Statements — FDA disclaimer and hemp compliance statement.",
    15: "Why Retailers Love PoolSide — high margin with strong ROI, fast turns and repeat buys, no refrigeration needed, a small footprint that saves shelf space, versatile fit for liquor, grocery, convenience and smoke shops, and a trending functional beverage category.",
    16: "Frequently Asked Questions on onset time, mixing with alcohol, safety, drug tests and storage, plus suggested MSRP of $4.95 for a single pouch and $51.00 for a box.",
    17: "Mix. Sip. PoolSide. — PoolSide 10mg THC Drink Mix. Visit drinkpoolside.com or @poolside.social.",
}

# Contact region and page CTAs both come from hotspots.json, which make_pdf.py
# also reads — so the web flipbook and the PDF can never drift apart.
CONTACT_HOTSPOT = CFG["contact"]
CONTACT_PAGE = CONTACT_HOTSPOT.get("page", PAGES)
CTAS = CFG.get("ctas", {})

PRODUCTS = CFG["products"]
HOTSPOTS = CFG["pages"]


def page_markup(i):
    spots = []
    for hs in HOTSPOTS.get(str(i), []):
        p = PRODUCTS[hs["p"]]
        x0, y0, x1, y1 = hs["box"]
        spots.append(
            f'<a class="hs hs--{hs["p"]}" href="{p["url"]}" target="_blank" rel="noopener"'
            f' style="left:{x0*100:.3f}%;top:{y0*100:.3f}%;width:{(x1-x0)*100:.3f}%;height:{(y1-y0)*100:.3f}%"'
            f' aria-label="{html.escape(p["label"])}">'
            f'<span class="hs__pin" aria-hidden="true"></span>'
            f'<span class="hs__tip">{html.escape(p["label"])}</span></a>'
        )
    if i == CONTACT_PAGE:
        x0, y0, x1, y1 = CONTACT_HOTSPOT["box"]
        spots.append(
            f'<a class="hs hs--contact" href="{CONTACT_HOTSPOT["url"]}" target="_blank" rel="noopener"'
            f' style="left:{x0*100:.3f}%;top:{y0*100:.3f}%;width:{(x1-x0)*100:.3f}%;height:{(y1-y0)*100:.3f}%"'
            f' aria-label="Contact PoolSide">'
            f'<span class="hs__pin" aria-hidden="true"></span>'
            f'<span class="hs__tip">{CONTACT_HOTSPOT["label"]}</span></a>'
        )
    for cta in CTAS.get(str(i), []):
        x0, y0, x1, y1 = cta["box"]
        spots.append(
            f'<a class="pcta" href="{cta["url"]}" target="_blank" rel="noopener"'
            f' style="left:{x0*100:.3f}%;top:{y0*100:.3f}%;width:{(x1-x0)*100:.3f}%;height:{(y1-y0)*100:.3f}%">'
            f'<span>{html.escape(cta["label"])}</span>'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg></a>'
        )

    # Pages 1-2 load immediately. The rest are hydrated by JS from data-* attrs.
    # Native loading="lazy" is NOT usable here: every page except the current one
    # sits in a visibility:hidden layer, so it never intersects the viewport and
    # never loads — deep-linking straight to page 9 would show an empty frame.
    if i <= 2:
        src = (f'<source srcset="pages/page-{i:02d}.webp" type="image/webp">\n'
               f'          <img src="pages/page-{i:02d}.jpg"')
        extra = ' fetchpriority="high"' if i == 1 else ""
    else:
        src = (f'<source data-srcset="pages/page-{i:02d}.webp" type="image/webp">\n'
               f'          <img data-src="pages/page-{i:02d}.jpg"')
        extra = ""
    return f"""      <figure class="page" data-page="{i}" aria-label="Page {i} of {PAGES}">
        <picture>
          {src} alt="{html.escape(ALT[i])}" width="{PW}" height="{PH}" decoding="async"{extra}>
        </picture>
        <span class="page__shade" aria-hidden="true"></span>
{chr(10).join('        ' + s for s in spots)}
      </figure>"""


thumbs = "\n".join(
    f'        <button class="thumb" data-goto="{i}" aria-label="Go to page {i}">'
    f'<img src="pages/thumb-{i:02d}.webp" alt="" width="300" height="225" loading="lazy" decoding="async">'
    f'<span>{i}</span></button>'
    for i in range(1, PAGES + 1)
)

pages_html = "\n".join(page_markup(i) for i in range(1, PAGES + 1))

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{TITLE}</title>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#0b2545">
<link rel="canonical" href="{SITE}/pages/brand-playbook">
<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{SITE}/cdn/shop/files/poolside-playbook-cover.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%230b2545'/><path d='M4 20c3-3 6-3 8 0s5 3 8 0 5-3 8 0' stroke='%2329a8e0' stroke-width='3.2' fill='none' stroke-linecap='round'/><circle cx='16' cy='10' r='4.2' fill='%23f2c21b'/></svg>">
<style>
:root{{
  --navy:#0b2545; --navy-2:#12345f; --blue:#29a8e0; --blue-dk:#1b7fb8;
  --orange:#e07a24; --gold:#f2c21b; --cream:#f7f3ea;
  --ink:#0e1c2c; --chrome:rgba(255,255,255,.92);
  --ratio: {PW} / {PH};
  --turn: 720ms;
}}
*,*::before,*::after{{box-sizing:border-box}}
html,body{{height:100%}}
body{{
  margin:0; background:
    radial-gradient(1200px 700px at 50% -10%, #17456f 0%, transparent 60%),
    linear-gradient(180deg,#0b2545 0%, #071a33 100%);
  background-attachment:fixed;
  color:#fff; overflow:hidden;
  font:500 15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}}
.app{{height:100dvh;display:flex;flex-direction:column}}

/* ---------- top bar ---------- */
.bar{{
  flex:0 0 auto;display:flex;align-items:center;gap:14px;
  padding:10px clamp(10px,2.4vw,22px);
  padding-top:max(10px,env(safe-area-inset-top));
}}
.brand{{display:flex;align-items:center;gap:10px;min-width:0}}
.brand svg{{width:26px;height:26px;flex:0 0 auto}}
.brand b{{font-size:15px;font-weight:800;letter-spacing:.2px;white-space:nowrap}}
.brand span{{font-size:12px;opacity:.62;white-space:nowrap}}
@media(max-width:640px){{.brand span{{display:none}}}}
.bar__sp{{flex:1 1 auto}}
.btn{{
  appearance:none;border:1px solid rgba(255,255,255,.20);background:rgba(255,255,255,.07);
  color:#fff;border-radius:10px;padding:8px 12px;font:inherit;font-size:13px;font-weight:600;
  display:inline-flex;align-items:center;gap:7px;cursor:pointer;
  transition:background .16s,border-color .16s,transform .1s;
  text-decoration:none;white-space:nowrap;
}}
.btn:hover{{background:rgba(255,255,255,.15);border-color:rgba(255,255,255,.36)}}
.btn:active{{transform:translateY(1px)}}
.btn:focus-visible{{outline:2px solid var(--blue);outline-offset:2px}}
.btn--cta{{background:linear-gradient(180deg,var(--blue),var(--blue-dk));border-color:transparent}}
.btn--cta:hover{{background:linear-gradient(180deg,#3fb8ee,#2189c4)}}
.btn svg{{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.btn--icon{{padding:8px}}
@media(max-width:860px){{.btn__t{{display:none}} .btn{{padding:8px}}}}

/* ---------- stage ---------- */
.stage{{
  flex:1 1 auto;position:relative;display:grid;place-items:center;
  padding:0 clamp(6px,5vw,68px);min-height:0;
}}
.book{{
  position:relative;width:100%;aspect-ratio:var(--ratio);
  max-width:calc((100dvh - 132px) * {PW} / {PH});
  perspective:2400px;
  filter:drop-shadow(0 26px 55px rgba(0,0,0,.55));
  border-radius:6px;
}}
.page{{
  position:absolute;inset:0;margin:0;visibility:hidden;
  transform-origin:left center;transform-style:preserve-3d;backface-visibility:hidden;
  border-radius:6px;overflow:hidden;background:#0b2545;
}}
.page img{{display:block;width:100%;height:100%;object-fit:cover;border-radius:6px;user-select:none;-webkit-user-drag:none}}
.page.is-under{{visibility:visible;z-index:5}}
.page.is-current{{visibility:visible;z-index:10}}
.page__shade{{
  position:absolute;inset:0;pointer-events:none;opacity:0;border-radius:6px;
  background:linear-gradient(90deg,rgba(0,0,0,.62) 0%,rgba(0,0,0,.28) 42%,rgba(0,0,0,0) 78%);
}}
.page.turn-fwd{{visibility:visible;z-index:30;animation:turnFwd var(--turn) cubic-bezier(.42,.02,.28,1) forwards}}
.page.turn-fwd .page__shade{{animation:shadeIn var(--turn) linear forwards}}
.page.turn-back{{visibility:visible;z-index:30;animation:turnBack var(--turn) cubic-bezier(.42,.02,.28,1) forwards}}
.page.turn-back .page__shade{{animation:shadeOut var(--turn) linear forwards}}
@keyframes turnFwd{{from{{transform:rotateY(0)}} to{{transform:rotateY(-180deg)}}}}
@keyframes turnBack{{from{{transform:rotateY(-180deg)}} to{{transform:rotateY(0)}}}}
@keyframes shadeIn{{from{{opacity:0}} to{{opacity:1}}}}
@keyframes shadeOut{{from{{opacity:1}} to{{opacity:0}}}}

/* click-to-advance surface, sits under the hotspots */
.tap{{position:absolute;inset:0;z-index:2;cursor:pointer}}

/* ---------- hotspots ---------- */
.hs{{
  position:absolute;z-index:6;display:block;border-radius:10px;text-decoration:none;
  outline:2px solid transparent;outline-offset:3px;
  transition:background .18s,box-shadow .18s;
}}
.hs::after{{content:"";position:absolute;inset:0;border-radius:10px;
  box-shadow:inset 0 0 0 2px transparent;transition:box-shadow .18s}}
.hs:hover{{background:rgba(41,168,224,.16)}}
.hs:hover::after{{box-shadow:inset 0 0 0 2px rgba(255,255,255,.85)}}
.hs--mango:hover{{background:rgba(224,122,36,.18)}}
.hs:focus-visible{{outline-color:#fff}}
.hs__pin{{
  position:absolute;left:50%;top:50%;width:30px;height:30px;margin:-15px 0 0 -15px;
  border-radius:50%;background:rgba(255,255,255,.95);
  box-shadow:0 3px 14px rgba(0,0,0,.4);
  display:grid;place-items:center;
}}
.hs__pin::before{{content:"";width:11px;height:11px;border-radius:50%;background:var(--blue)}}
.hs--mango .hs__pin::before{{background:var(--orange)}}
.hs--contact .hs__pin::before{{background:var(--gold)}}
.hs__pin::after{{
  content:"";position:absolute;inset:0;border-radius:50%;
  box-shadow:0 0 0 0 rgba(255,255,255,.7);animation:pulse 2.6s ease-out infinite;
}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 rgba(255,255,255,.62)}}70%{{box-shadow:0 0 0 16px rgba(255,255,255,0)}}100%{{box-shadow:0 0 0 0 rgba(255,255,255,0)}}}}
.hs__tip{{
  position:absolute;left:50%;top:50%;transform:translate(-50%,26px);
  background:#fff;color:var(--ink);font-size:12px;font-weight:800;letter-spacing:.2px;
  padding:5px 10px;border-radius:999px;white-space:nowrap;
  box-shadow:0 4px 16px rgba(0,0,0,.32);opacity:0;transition:opacity .18s;pointer-events:none;
}}
.hs:hover .hs__tip,.hs:focus-visible .hs__tip{{opacity:1}}
/* touch devices get no hover, so show the label outright — but only where
   there is room for it. On phones two pills sit side by side and collide, so
   below 700px the pulsing pin carries the affordance on its own. */
@media(hover:none) and (min-width:701px){{.hs__tip{{opacity:1}}}}
@media(max-width:700px){{
  .hs__tip{{display:none}}
  .hs__pin{{width:22px;height:22px;margin:-11px 0 0 -11px}}
  .hs__pin::before{{width:8px;height:8px}}
}}
.no-pins .hs__pin,.no-pins .hs__tip{{display:none}}

/* labelled in-page CTA (e.g. "Full COAs" on page 6). Sized against the book,
   which is capped by both viewport width and height, so min() of vw/vh tracks it. */
.pcta{{
  position:absolute;z-index:8;display:flex;align-items:center;justify-content:center;gap:.5em;
  border-radius:999px;text-decoration:none;white-space:nowrap;
  background:linear-gradient(180deg,#ffffff,#eaf2fb);color:var(--navy);
  font-weight:800;letter-spacing:.015em;font-size:clamp(9px,min(1.12vw,1.5vh),17px);
  box-shadow:0 3px 14px rgba(0,0,0,.34),inset 0 0 0 1px rgba(11,37,69,.12);
  transition:transform .14s,box-shadow .18s,background .18s;
}}
.pcta:hover{{background:linear-gradient(180deg,#ffffff,#d9e8f8);transform:translateY(-1px);
  box-shadow:0 7px 22px rgba(0,0,0,.44),inset 0 0 0 1px rgba(11,37,69,.20)}}
.pcta:active{{transform:translateY(0)}}
.pcta:focus-visible{{outline:2px solid #fff;outline-offset:3px}}
.pcta svg{{width:1.05em;height:1.05em;fill:none;stroke:currentColor;stroke-width:2.4;
  stroke-linecap:round;stroke-linejoin:round;transition:transform .16s}}
.pcta:hover svg{{transform:translateX(2px)}}
@media(prefers-reduced-motion:reduce){{.pcta,.pcta svg{{transition:none}}}}

/* ---------- side arrows ---------- */
.nav{{
  position:absolute;top:50%;transform:translateY(-50%);z-index:40;
  width:46px;height:46px;border-radius:50%;display:grid;place-items:center;
  background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.22);
  color:#fff;cursor:pointer;backdrop-filter:blur(7px);transition:background .16s,opacity .16s;
}}
.nav:hover{{background:rgba(255,255,255,.26)}}
.nav[disabled]{{opacity:.22;cursor:default}}
.nav svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}}
.nav--prev{{left:clamp(2px,1.2vw,18px)}}
.nav--next{{right:clamp(2px,1.2vw,18px)}}
@media(max-width:640px){{.nav{{width:38px;height:38px}}}}

/* ---------- bottom bar ---------- */
.foot{{
  flex:0 0 auto;display:flex;align-items:center;justify-content:center;gap:14px;
  padding:10px 16px;padding-bottom:max(10px,env(safe-area-inset-bottom));
}}
.count{{font-variant-numeric:tabular-nums;font-size:13px;font-weight:700;opacity:.9;min-width:64px;text-align:center}}
.scrub{{
  -webkit-appearance:none;appearance:none;width:min(340px,42vw);height:4px;border-radius:99px;
  background:rgba(255,255,255,.24);outline:none;cursor:pointer;
}}
.scrub::-webkit-slider-thumb{{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.4);cursor:grab}}
.scrub::-moz-range-thumb{{width:16px;height:16px;border:0;border-radius:50%;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.4)}}
@media(max-width:560px){{.scrub{{display:none}}}}

/* ---------- thumbnail drawer ---------- */
.sheet{{
  position:fixed;inset:0;z-index:80;background:rgba(4,14,28,.86);backdrop-filter:blur(10px);
  display:none;flex-direction:column;padding:16px;
}}
.sheet[open]{{display:flex}}
.sheet__hd{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}
.sheet__hd h2{{margin:0;font-size:15px;font-weight:800;letter-spacing:.3px}}
.grid{{
  flex:1 1 auto;overflow:auto;display:grid;gap:12px;align-content:start;
  grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
}}
.thumb{{
  position:relative;padding:0;border:2px solid transparent;background:none;border-radius:7px;
  cursor:pointer;overflow:hidden;line-height:0;transition:border-color .15s,transform .15s;
}}
.thumb img{{width:100%;height:auto;display:block;border-radius:5px}}
.thumb span{{
  position:absolute;left:6px;bottom:6px;background:rgba(4,14,28,.85);color:#fff;
  font-size:11px;font-weight:800;line-height:1;padding:4px 7px;border-radius:5px;
}}
.thumb:hover{{transform:translateY(-2px);border-color:rgba(255,255,255,.55)}}
.thumb.is-on{{border-color:var(--blue)}}

/* ---------- first-run hint ---------- */
.hint{{
  position:absolute;left:50%;bottom:14px;transform:translateX(-50%);z-index:45;
  background:rgba(4,14,28,.82);border:1px solid rgba(255,255,255,.16);
  padding:8px 15px;border-radius:999px;font-size:12.5px;font-weight:600;letter-spacing:.2px;
  pointer-events:none;transition:opacity .5s;white-space:nowrap;
}}
.hint.gone{{opacity:0}}

/* ---------- last-page CTA ---------- */
.endcta{{
  position:absolute;left:50%;bottom:16px;transform:translateX(-50%) translateY(12px);
  z-index:46;opacity:0;pointer-events:none;transition:opacity .35s,transform .35s;
}}
.endcta.on{{opacity:1;transform:translateX(-50%) translateY(0);pointer-events:auto}}

@media (prefers-reduced-motion:reduce){{
  .page.turn-fwd,.page.turn-back{{animation-duration:1ms}}
  .page.turn-fwd .page__shade,.page.turn-back .page__shade{{animation-duration:1ms}}
  .hs__pin::after{{animation:none}}
  *{{transition-duration:.01ms !important}}
}}
</style>
</head>
<body>
<div class="app">

  <header class="bar">
    <div class="brand">
      <svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#0b2545"/><path d="M4 20c3-3 6-3 8 0s5 3 8 0 5-3 8 0" stroke="#29a8e0" stroke-width="3.2" fill="none" stroke-linecap="round"/><circle cx="16" cy="10" r="4.2" fill="#f2c21b"/></svg>
      <b>PoolSide</b><span>Brand Playbook</span>
    </div>
    <div class="bar__sp"></div>
    <button class="btn btn--icon" id="btnGrid" aria-label="All pages" title="All pages">
      <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>
    </button>
    <button class="btn btn--icon" id="btnFull" aria-label="Fullscreen" title="Fullscreen">
      <svg viewBox="0 0 24 24"><path d="M4 9V5a1 1 0 011-1h4M20 9V5a1 1 0 00-1-1h-4M4 15v4a1 1 0 001 1h4M20 15v4a1 1 0 01-1 1h-4"/></svg>
    </button>
    <a class="btn" id="btnPdf" href="PoolSide-Brand-Playbook.pdf" download>
      <svg viewBox="0 0 24 24"><path d="M12 3v12m0 0l-4-4m4 4l4-4M4 19h16"/></svg><span class="btn__t">PDF</span>
    </a>
    <a class="btn btn--cta" href="{CONTACT}" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24"><path d="M4 6h16v12H4z"/><path d="M4 7l8 6 8-6"/></svg><span class="btn__t">Contact us</span>
    </a>
    <button class="btn btn--icon" id="btnClose" aria-label="Close" title="Close" hidden>
      <svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
  </header>

  <main class="stage">
    <button class="nav nav--prev" id="prev" aria-label="Previous page">
      <svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>
    </button>

    <div class="book" id="book" role="region" aria-roledescription="flipbook" aria-label="PoolSide Brand Playbook, {PAGES} pages">
      <div class="tap" id="tap" role="button" tabindex="0" aria-label="Next page"></div>
{pages_html}
    </div>

    <button class="nav nav--next" id="next" aria-label="Next page">
      <svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>
    </button>

    <div class="hint" id="hint">Click the page to turn &nbsp;·&nbsp; tap a product to shop it</div>
    <a class="btn btn--cta endcta" id="endcta" href="{CONTACT}" target="_blank" rel="noopener">
      Get in touch with our team →
    </a>
  </main>

  <footer class="foot">
    <span class="count" id="count">1 / {PAGES}</span>
    <input class="scrub" id="scrub" type="range" min="1" max="{PAGES}" value="1" step="1" aria-label="Jump to page">
  </footer>
</div>

<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="All pages">
  <div class="sheet__hd">
    <h2>All pages</h2><div class="bar__sp"></div>
    <button class="btn btn--icon" id="gridClose" aria-label="Close">
      <svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
  </div>
  <div class="grid" id="grid">
{thumbs}
  </div>
</div>

<script>
(function(){{
  "use strict";
  var TOTAL = {PAGES};
  var book  = document.getElementById('book');
  var pages = Array.prototype.slice.call(book.querySelectorAll('.page'));
  var cur = 1, busy = false;

  // read the turn duration from CSS so the safety net can never cut a turn short
  var TURN = (function(){{
    var v = getComputedStyle(document.documentElement).getPropertyValue('--turn').trim();
    var n = parseFloat(v) || 720;
    return /ms$/.test(v) ? n : n * 1000;
  }})();

  function clamp(n){{ return Math.max(1, Math.min(TOTAL, n)); }}

  // swap data-src -> src so the page actually downloads, even though it is
  // sitting in a hidden layer that the lazy-loader would never trigger on
  function hydrate(n){{
    var p = pages[n-1]; if (!p) return;
    var s = p.querySelector('source[data-srcset]');
    if (s){{ s.srcset = s.dataset.srcset; s.removeAttribute('data-srcset'); }}
    var img = p.querySelector('img[data-src]');
    if (img){{ img.src = img.dataset.src; img.removeAttribute('data-src'); }}
  }}

  function paint(){{
    pages.forEach(function(p, i){{
      p.classList.remove('is-current','is-under','turn-fwd','turn-back');
      p.style.transform = '';
      p.classList.toggle('is-current', i === cur-1);
    }});
    document.getElementById('count').textContent = cur + ' / ' + TOTAL;
    document.getElementById('scrub').value = cur;
    document.getElementById('prev').disabled = (cur === 1);
    document.getElementById('next').disabled = (cur === TOTAL);
    document.getElementById('endcta').classList.toggle('on', cur === TOTAL);
    Array.prototype.forEach.call(document.querySelectorAll('.thumb'), function(t){{
      t.classList.toggle('is-on', +t.dataset.goto === cur);
    }});
    // keep neighbours warm so the next turn never shows a blank page
    [cur, cur-1, cur+1, cur+2].forEach(hydrate);
    try{{ history.replaceState(null,'','#p=' + cur); }}catch(e){{}}
  }}

  function go(to, animate){{
    to = clamp(to);
    if (busy || to === cur) return;
    var from = cur;
    if (animate === false || Math.abs(to - from) > 1){{ cur = to; paint(); return; }}

    busy = true;
    var fwd  = to > from;
    var leaf = pages[(fwd ? from : to) - 1];   // the page that visually turns
    var base = pages[(fwd ? to : from) - 1];   // the page revealed underneath

    base.classList.add('is-under');
    leaf.classList.remove('is-current');
    leaf.classList.add(fwd ? 'turn-fwd' : 'turn-back');

    var done = false;
    function finish(){{
      if (done) return; done = true;
      leaf.removeEventListener('animationend', finish);
      cur = to; busy = false; paint();
    }}
    leaf.addEventListener('animationend', finish);
    setTimeout(finish, TURN + 260);   // safety net if animationend never fires
  }}

  var next = function(){{ go(cur+1); }}, prev = function(){{ go(cur-1); }};
  document.getElementById('next').addEventListener('click', next);
  document.getElementById('prev').addEventListener('click', prev);

  // click / tap the page to advance (hotspots sit above this layer and swallow their own clicks)
  var tap = document.getElementById('tap');
  tap.addEventListener('click', next);
  tap.addEventListener('keydown', function(e){{
    if (e.key === 'Enter' || e.key === ' '){{ e.preventDefault(); next(); }}
  }});

  document.addEventListener('keydown', function(e){{
    if (document.getElementById('sheet').hasAttribute('open')){{
      if (e.key === 'Escape') closeGrid();
      return;
    }}
    if (e.key === 'ArrowRight' || e.key === 'PageDown'){{ e.preventDefault(); next(); }}
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp'){{ e.preventDefault(); prev(); }}
    else if (e.key === 'Home'){{ e.preventDefault(); go(1,false); }}
    else if (e.key === 'End'){{ e.preventDefault(); go(TOTAL,false); }}
  }});

  // swipe
  var sx=0, sy=0, tracking=false;
  book.addEventListener('touchstart', function(e){{
    if (e.touches.length !== 1) return;
    sx = e.touches[0].clientX; sy = e.touches[0].clientY; tracking = true;
  }}, {{passive:true}});
  book.addEventListener('touchend', function(e){{
    if (!tracking) return; tracking = false;
    var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.6){{ dx < 0 ? next() : prev(); }}
  }}, {{passive:true}});

  document.getElementById('scrub').addEventListener('input', function(){{ go(+this.value, false); }});

  // thumbnail drawer
  var sheet = document.getElementById('sheet');
  function openGrid(){{ sheet.setAttribute('open',''); document.getElementById('gridClose').focus(); }}
  function closeGrid(){{ sheet.removeAttribute('open'); document.getElementById('btnGrid').focus(); }}
  document.getElementById('btnGrid').addEventListener('click', openGrid);
  document.getElementById('gridClose').addEventListener('click', closeGrid);
  sheet.addEventListener('click', function(e){{ if (e.target === sheet) closeGrid(); }});
  document.getElementById('grid').addEventListener('click', function(e){{
    var b = e.target.closest('.thumb'); if (!b) return;
    go(+b.dataset.goto, false); closeGrid();
  }});

  // fullscreen
  document.getElementById('btnFull').addEventListener('click', function(){{
    var el = document.documentElement;
    if (document.fullscreenElement) document.exitFullscreen();
    else if (el.requestFullscreen) el.requestFullscreen();
    else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
  }});

  // when embedded in a modal, show a close button that tells the parent page
  if (window.self !== window.top){{
    var bc = document.getElementById('btnClose');
    bc.hidden = false;
    bc.addEventListener('click', function(){{
      parent.postMessage({{type:'poolside-playbook-close'}}, '*');
    }});
  }}

  // deep link  ...#p=7
  var m = /(?:^|[#&])p=(\\d+)/.exec(location.hash);
  if (m) cur = clamp(+m[1]);

  paint();

  var hint = document.getElementById('hint');
  setTimeout(function(){{ hint.classList.add('gone'); }}, 5200);
}})();
</script>
</body>
</html>
"""

with open(OUT, "w") as f:
    f.write(HTML)

n_spots = sum(len(v) for v in HOTSPOTS.values()) + 1
print(f"wrote {OUT}")
print(f"  {PAGES} pages, {n_spots} clickable regions "
      f"({sum(len(v) for v in HOTSPOTS.values())} product + 1 contact)")
