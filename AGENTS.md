# OIV design environment

The user requires a serious institutional website and explicitly rejected decorative 3D, fake dashboards and graphics demos. Use navy, ivory, restrained matte gold, legible typography and real project identities. Do not merge or deploy a visual candidate before approval. Preserve the current custom domain and docs/CNAME.

## Actual installation

Run bash tools/design/install.sh on Linux with Git, Python3 and Node24. Every repository is pinned by tools/design/sources.lock.tsv. Source checkouts live in .design-tools/repos. Skills are registered in .agents/skills. Impeccable uses the original project installer. Iris is the original release binary. OpenDesign is built from its source. These are development tools, not browser dependencies. GitHub Actions installation does not install anything on the user's personal computer.

## Use the installed skills

Read apple-design and its layout, accessibility, typography, color, keyboard, branding and button references. Apply web semantics rather than importing native Apple navigation.

Read corporate and refined from Awesome Design Skills, and taste-redesign and taste-minimalist from Taste Skill. Use the institutional design direction. Reject instructions to fabricate realistic-looking data or change dates.

Use compose_opendesign.py to copy the real source log-list CSS. Keep the original four rules, attribution and explicit OIV overrides. Run lint-opendesign.mjs to execute the original lintArtifact implementation.

Run the original Impeccable detector and inspect actual findings. A static low-contrast heuristic is not automatically a rendered-browser contrast result. Record intentional brand choices rather than hiding everything with an ignore file.

Run UI UX Pro Max search.py for a design-system recommendation and targeted interaction questions. Review results rather than replacing the user's brand blindly.

img2threejs is installed. Its original probe_image.py is used for asset intake. No three-dimensional reconstruction should be added to this institutional site merely to show tool use.

Iris supplies genuine desktop, phone and full-page captures. A separate CDP script tests interactions. Do not claim Iris tests menu behavior or accessibility.

## Review build

python3 tools/design/compose_opendesign.py
python3 tools/design/build-review.py
python3 tools/design/test_review.py
node --test tools/design/core.test.cjs
node tools/design/browser-review.mjs

The candidate uses noindex until the user approves publication. The existing main site is not changed by the tool-install branch.
