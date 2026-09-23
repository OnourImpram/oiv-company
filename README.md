# Onour Impram Ventures

OIV company website, English and Turkish. Static HTML and CSS, no build step and no client-side JavaScript.

## Brand and page structure

The site presents OIV as a technology and applied research company that brings behavioural science and software engineering together. AI tools, digital products and evaluation work sit within that shared approach. Evaluation is a defined way to work with the company, not a replacement for its wider identity.

The page sequence is company focus, shared approach, open source work, digital products, collaboration, research and founder, contact, company information. Existing logos, product artwork, publication covers and locally hosted fonts are retained. Navy, warm paper and gold remain the visual identity.

English headline: Human insight. Accountable technology.

Turkish headline: İnsanı anlayan araştırma. Denetlenebilir teknoloji.

## Deployment

Only `docs/` is published. GitHub Pages uses `main /docs`. Repository documentation, tests and workflows are not part of the published directory.

The current production base is `https://onourimpram.github.io/oiv-company/`. Both pages use relative internal paths. Canonical links, language alternates, Open Graph URLs, structured data, sitemap, robots and security.txt point to the active host, rather than an unconnected future domain.

`CNAME.bekliyor` remains a pending custom-domain record. This update does not change DNS or enable the custom domain. Before a future cutover, verify domain ownership with GitHub, associate the verified domain with Pages, then configure the DNS record. Move the pending file to `docs/CNAME` only as part of that controlled cutover. Update every absolute production URL and `tests/check_live.py` together, then verify HTTPS and both languages on the new host. Do not enable a wildcard DNS record. If the Pages domain association is removed, remove the matching DNS record as well.

## Content boundaries

Legal identifiers, office details, contact address, original source links and application legal links are retained from the existing site. Product descriptions describe scope, not independently certified outcomes. Mergen is described as repository-based review. mneme is described as file-based context and retrieval. No customer counts, investment, performance figures or clinical efficacy claims have been invented.

Application status preserves the repository's 22 September 2026 record, with two public store listings and four submitted applications. The page dates that record and does not present submitted apps as available. Recheck storefront availability before changing these labels.

Publication contributions are not labelled as two sole-authored company books. The founder's expert-group participation is personal, not institutional endorsement. Clinical practice remains separate from OIV.

Contact links open addressed email drafts with different subjects for project, evaluation, research, training and application support. The website does not send messages, collect form submissions or request sensitive information.

## Verification

Run the standard-library checks from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

After deployment, verify public bytes against the current checkout:

```sh
python3 tests/check_live.py
```

The live verifier waits for the Pages deployment, compares SHA-256 digests for both pages and referenced assets, and checks that repository-only paths return 404. It does not claim that external store listings or third-party websites are continuously available.

The GitHub Actions workflow runs the content tests for pull requests and main pushes. Main runs also check the live deployment. It has read-only contents permission, pins checkout to a commit and does not persist credentials.

During the 23 September 2026 revision, local Chromium rendering covered both languages at 320, 390, 768, 1024, 1440 and 1920 pixels, plus JavaScript-disabled and reduced-motion cases. Layout checks covered overflow, loaded images and fonts, internal navigation, minimum 24-pixel link target heights and the keyboard skip link. These were memory-rendered copies with embedded assets because the local browser could not navigate to a local HTTP server. CSP was removed only in those isolated render copies. The production CSP was retained and checked structurally. This is not a claim of full WCAG conformance or testing on Safari, Firefox or physical devices.

## Fonts and security

Fraunces, IBM Plex Sans and IBM Plex Mono are served from `docs/assets/fonts/`. Existing licenses are retained in that directory. No external font service or analytics is added. The restrictive Content Security Policy remains in both pages, with no executable scripts or form endpoint.
