# OIV institutional review and installed design toolchain

This is a review branch, not the live website. Main and the custom domain are unchanged by this work. The user rejected decorative 3D and asked for a serious institutional design, then explicitly requested that eight design repositories be downloaded, installed and used.

## What is actually installed

`tools/design/sources.lock.tsv` pins all eight full repositories. `bash tools/design/install.sh` clones those revisions into `.design-tools/repos`, registers actual skill directories under `.agents/skills`, invokes the original Impeccable installer, installs original Iris, installs and builds the OpenDesign headless CLI and executes source tools.

These are project-local development installations in the Actions runner. They do not install software on the user's computer, do not run paid models and are not browser dependencies. The repeatable installer and pinned revisions are retained in this branch. An Actions runner itself is temporary.

Apple Design, Awesome Design Skills corporate/refined, Taste redesign/minimalist and UI UX Pro Max are installed as agent skills. UI UX Pro Max's original Python design-system and focused UX searches execute against the OIV brief. img2threejs is installed and its actual image-intake probe inspects the existing company artwork. No 3D reconstruction is added to the page.

The original Impeccable engine scans both files and a rendered local HTTP page. Detector findings are preserved, not equated to installation failure or blanket accessibility results. Original Iris captures desktop, phone and full-page screenshots with Chrome.

OpenDesign's original headless daemon CLI is built from source and its real lintArtifact implementation checks both page variants. Four original log-list CSS rules are copied into `docs/assets/opendesign.css`, with explicit OIV overrides and upstream license/provenance. This is direct component reuse, not only inspiration. No desktop GUI or paid model generation is claimed.

## Candidate design

Navy, ivory, matte brass, existing Fraunces/Plex typography, authentic company and project marks. Real text headings and short company copy, source-backed project descriptions, three collaboration rows, six products with truthful historical publication states, real book covers and a local email note builder. There is no WebGL, canvas, animated knot, fabricated dashboard, tracking or message-sending endpoint in the new pages.

The product filters operate by publication status, with native keyboard-accessible buttons and live result counts. All products remain visible without JavaScript. The mobile menu exposes expanded state and restores focus on Escape. Contact drafts use a fixed recipient, bounded input and encoded URL parameters. Clipboard denial has a visible manual fallback.

Both pages are marked noindex while under review. `docs/CNAME` and canonical addresses preserve the existing `oiv.onourimpram.com` host. Do not deploy until visual approval. A future approved release must retire the old Precision-specific test expectations, remove noindex, update the main test workflow, and verify the actual live build before reporting publication.

## Reproduce

```sh
bash tools/design/install.sh
python3 tools/design/assert-results.py
```

The toolchain performs source acquisition, original tool execution, candidate generation, Python/Node contracts, genuine Iris captures and Chrome/CDP interaction tests. Evidence records every command and return code. A separate write-permitted job can commit only five allowlisted generated files, verified by SHA256, to this exact review branch. Third-party installation/build steps have read-only repository permissions and no persisted checkout credentials.

Some Impeccable style warnings are intentional, including institutional uppercase labels and the ivory palette. A warning-free heuristic scan is not the aesthetic acceptance criterion. Browser testing uses Chrome, not a claim of Safari, Firefox, physical-device coverage or WCAG certification.
