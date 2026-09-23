# Onour Impram Ventures

English and Turkish OIV website. Precision refines the existing Continuum direction rather than starting another unrelated theme. GitHub Pages serves only `docs/` from `main` at https://oiv.onourimpram.com/. The former address https://onourimpram.github.io/oiv-company/ redirects there.

## What changed

A more controlled sculptural hero, larger small text and controls, asymmetric project plates, two visible published-product records, an optional project brief builder and a branded 404. Existing legal identifiers, store-status dates, source links, artwork and publication covers remain intact.

The hero uses original procedural geometry and native WebGL. Motion starts paused and requires an explicit play action. Surface and Structure are two views of the same geometry. Reduced-motion changes stop animation. Offscreen and hidden tabs do not animate. When WebGL cannot initialize, a single static Canvas rendering is used and motion controls stay hidden. With JavaScript disabled, an SVG illustration remains. Loss of an existing WebGL context falls back to that SVG.

The project brief builder formats a local email draft and copies text when permitted. It has an honest manual-copy fallback. No information is stored persistently or sent by the website. The visitor reviews and sends the email in their own mail app. No form endpoint, tracking, third-party runtime or remote font service was added.

## Reference use

`design-notes/SOURCES.md` records all eight requested repositories, the exact material inspected, the applied principles and what was not executed. These sources informed the implementation. They were not all installed or represented as eight working engines.

## Reproducible checks

```sh
python3 -m unittest discover -s tests -v
node --test tests/core.test.cjs
node tests/browser.mjs
python3 tests/check_live.py
```

The browser check requires Node 22 and a Chrome-family browser. Set `CHROME` to the executable path as needed. Without `OIV_BASE_URL` it serves the exact production files through local HTTP at the site root. With `OIV_BASE_URL` it tests that host. It does not remove or weaken production CSP. No npm dependency is required.

GitHub Actions runs content and geometry tests, then the real browser check on refinement branches. On main, it first verifies live bytes against the checkout and then inspects the live site in Chrome. Browser reports and desktop, mobile, full-page and structure-view screenshots are uploaded as the `oiv-browser-evidence` artifact with three-day retention. Workflow permissions remain read-only for repository contents.

The interactive container cannot navigate to HTTP or initialize WebGL. Local layout checks therefore used transient memory-rendered copies with embedded existing assets and omitted CSP. Local captures demonstrate the static Canvas fallback, not WebGL execution. The separate CI browser checks are the authority for actual HTTP, CSP and WebGL behavior. No blanket WCAG, Safari, Firefox or physical-device claim is made.

## Publishing and content boundaries

The company site has its own host since 23 September 2026: `docs/CNAME` holds `oiv.onourimpram.com`, DNS has CNAME `oiv` to `onourimpram.github.io` (DNS only), and `onourimpram.com` is a verified GitHub Pages domain for the account. Keep the TXT record `_github-pages-challenge-OnourImpram.onourimpram.com`: removing it ends that verification. The founder's personal site at onourimpram.com is separate and not part of this repository. Do not publish a wildcard DNS record. A later host change updates every absolute production URL, `docs/404.html`, the tests and the workflow base URL together. Only `docs/` is published. `DESIGN.md` is the previous Continuum record; the current refinement and its source decisions are documented in `design-notes/SOURCES.md`.

Product artwork is conceptual, not a fabricated application screenshot. Store labels remain tied to the 22 September 2026 record and are not a fresh storefront check. Publication contributions do not imply two sole-authored company books. Clinical practice remains separate. Evaluation does not imply certification or demonstrate clinical effects.
