# oiv-company

ONOUR IMPRAM VENTURES LTD — company register page (EN + TR).

Static, no build step. `index.html` (EN), `tr/index.html` (TR), `assets/style.css`.
Paths are relative so the site works both at the project-page URL and at the
custom domain.

**Why it exists.** Samsung rejected the Galaxy Store commercial-seller request on
2026-09-21; two of the four reasons require the seller's corporate email domain
to match the domain of the company's official website, and the D-U-N-S record to
name that website. This page is that website: legal name, company number,
D-U-N-S, registered office, director, contact, and the software the company
publishes.

**Custom domain.** `CNAME.bekliyor` holds the intended host
(`oiv.onourimpram.com`). Rename it to `CNAME` once the DNS record exists:
Cloudflare → onourimpram.com → CNAME `oiv` → `onourimpram.github.io`, proxy OFF
(DNS only, so GitHub can issue the certificate). Until then the site is served at
the github.io project URL.

Checks run before publishing: no horizontal overflow at 320/360/390/768/1024/1440,
axe-core WCAG A/AA with zero serious/critical findings on both pages, contrast
measured rather than assumed.
