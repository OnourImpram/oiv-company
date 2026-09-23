# Onour Impram Ventures

Bilingual OIV website. The Continuum redesign replaces the prior large emblem and text-heavy corporate layout with a typographic opening, original procedural artwork, visual product presentations and progressive disclosure.

## Published files

GitHub Pages serves only `docs/` from `main`. Production is https://onourimpram.github.io/oiv-company/ and the Turkish page is `/oiv-company/tr/`. No build step is needed. HTML, CSS, a small first-party JavaScript file and the existing local assets are sufficient.

`DESIGN.md` records the brief, reference repositories, design choices and content boundaries. OpenDesign and OpenArt were researched, not installed as runtime dependencies. The sculpture is original code, not an OpenArt generation.

## Behaviour

The Canvas 2D sculpture honours reduced motion and has an explicit pause button. Animation pauses offscreen and when the document is hidden. JavaScript is an enhancement. Without it, content, native disclosures, email links and navigation remain available, alongside a CSS artwork fallback.

The mobile menu supports Escape and expanded state. Project scope, the six-app catalogue, services and company details use native disclosures. Contact links open email drafts. The site does not send messages, collect form data or add analytics.

## Content boundaries

The legal name, company identifiers, registered address, source repositories and application legal links are preserved. The two published and four submitted application statuses are explicitly dated to the prior 22 September 2026 record, not presented as a fresh store verification. Publication contributions do not imply sole authorship or company ownership of the books. Clinical practice remains separate. Product descriptions do not claim certification, clinical efficacy or independent validation.

## Verification

Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 tests/check_live.py
```

The existing read-only GitHub Actions workflow runs the content contracts, then checks that live page and asset bytes match the checkout. It also checks that repository-only files are absent from the Pages publication.

Local verification for this revision ran 13 standard-library content tests and 26 Chromium UI scenarios. UI checks cover both languages at 320, 360, 390, 768, 1024, 1440 and 1920px, plus mobile menu and Escape focus, app catalogue, project scope, services, company details, reduced motion, pause/resume and JavaScript-disabled navigation. Final desktop, mobile and full-page screenshots were inspected after lazy images loaded.

The local browser was administratively unable to navigate to HTTP, localhost or file URLs. Local UI tests therefore used memory-rendered copies with embedded existing assets. CSP was removed only from those transient copies and the deferred first-party script was executed after the document body. Production files retain CSP. This is not a full accessibility audit or live browser, Safari, Firefox or physical-device validation. The separate live verifier checks deployed byte identity, not visual rendering or third-party availability.

## Hosting and security

The existing fonts and their license files are unchanged. No CDN or external font request is introduced. CSP permits only first-party scripts, styles, fonts and images and disallows form submission. Canonical, language, social, sitemap and security metadata continue to use the active GitHub Pages host.

`CNAME.bekliyor` remains pending. This redesign makes no DNS or custom-domain change. A future cutover requires verified domain ownership and coordinated Pages association, DNS, production metadata and live-verifier changes. Do not publish an unverified custom domain or wildcard DNS record.
