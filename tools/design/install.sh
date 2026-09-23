#!/usr/bin/env bash
# Project-local installation. No model API calls, credentials or production publishing.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd); cd "$ROOT"
V="$ROOT/.design-tools/repos"; E="$ROOT/tool-evidence"; B="$ROOT/.design-tools/bin"
mkdir -p "$V" "$E" "$B" "$ROOT/.agents/skills"
printf 'step\texit_code\n' > "$E/commands.tsv"
run(){ local name="$1"; shift; echo "RUN $name: $*"; ( "$@" ) > "$E/$name.log" 2>&1; local rc=$?; printf '%s\t%s\n' "$name" "$rc" >> "$E/commands.tsv"; tail -n 10 "$E/$name.log"; echo "RESULT $name $rc"; return 0; }
while IFS=$'\t' read -r repo sha digest; do
 [[ "$repo" == repository ]] && continue
 name=${repo##*/}
 if [[ ! -e "$V/$name/.git" ]]; then git init -q "$V/$name"; git -C "$V/$name" remote add origin "https://github.com/$repo.git"; git -C "$V/$name" fetch --depth 1 origin "$sha"; git -C "$V/$name" checkout --detach FETCH_HEAD; fi
 actual=$(git -C "$V/$name" rev-parse HEAD); [[ "$actual" == "$sha" ]] || { echo "Revision mismatch $repo"; exit 1; }; echo "$repo $actual"
done < tools/design/sources.lock.tsv
link_skill(){ local name=$1 target=$2; ln -sfn "$target" "$ROOT/.agents/skills/$name"; test -f "$ROOT/.agents/skills/$name/SKILL.md"; }
run apple-design-install link_skill apple-design "$V/apple-design-skill"
run open-design-web-install link_skill open-design-web "$V/open-design/design-templates/web-prototype"
run open-design-brief-install link_skill open-design-brief "$V/open-design/skills/design-brief"
run corporate-skill-install link_skill corporate "$V/awesome-design-skills/skills/corporate"
run refined-skill-install link_skill refined "$V/awesome-design-skills/skills/refined"
run taste-skill-install link_skill taste-redesign "$V/taste-skill/skills/redesign-skill"
run taste-minimalist-install link_skill taste-minimalist "$V/taste-skill/skills/minimalist-skill"
run img2threejs-install link_skill img2threejs "$V/img2threejs"
run uipro-skill-install link_skill ui-ux-pro-max "$V/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max"
run uipro-design-system python3 "$ROOT/.agents/skills/ui-ux-pro-max/scripts/search.py" 'research consultancy institutional' --design-system -p 'OIV Institutional'
run uipro-keyboard python3 "$ROOT/.agents/skills/ui-ux-pro-max/scripts/search.py" 'focus not obscured' --domain ux
run uipro-responsive python3 "$ROOT/.agents/skills/ui-ux-pro-max/scripts/search.py" 'orphan heading line balance' --domain ux
run img2threejs-asset-probe python3 "$V/img2threejs/forge/stage1_intake/probe_image.py" "$ROOT/docs/assets/brand/oiv-mark-dark.png"
run compose-opendesign python3 tools/design/compose_opendesign.py
run build-institutional python3 tools/design/build-review.py
run content-tests python3 tools/design/test_review.py
run functional-tests node --test tools/design/core.test.cjs
export IMPECCABLE_HOME="$ROOT/.design-tools/impeccable-cache"
run impeccable-engine sh "$V/impeccable/skill/scripts/impeccable" engine-probe
run impeccable-install node "$V/impeccable/cli/bin/cli.js" install -y --providers=claude,codex --scope=project
run impeccable-detect sh "$V/impeccable/skill/scripts/impeccable" detect --json "$ROOT/docs/index.html" "$ROOT/docs/tr/index.html"
run iris-install env IRIS_INSTALL_DIR="$B" sh "$V/iris/install.sh"
run iris-version "$B/iris" --version
python3 -m http.server 8765 --bind 127.0.0.1 --directory "$ROOT/docs" > "$E/http.log" 2>&1 & SERVER_PID=$!; sleep 2
run iris-desktop "$B/iris" http://127.0.0.1:8765/tr/ --size desktop --scale 1 --wait 1000 --json -o "$E/iris-desktop-tr.png"
run iris-mobile "$B/iris" http://127.0.0.1:8765/tr/ --size iphone --scale 1 --wait 1000 --json -o "$E/iris-mobile-tr.png"
run iris-full "$B/iris" http://127.0.0.1:8765/tr/ --full --scale 1 --json -o "$E/iris-full-tr.png"
run impeccable-rendered sh "$V/impeccable/skill/scripts/impeccable" detect --json http://127.0.0.1:8765/tr/
run prepare-browser python3 tools/design/prepare-browser.py
run browser-review node .design-tools/browser-review.mjs
kill "$SERVER_PID" || true
run pnpm-install npm install --prefix "$ROOT/.design-tools/bootstrap" --no-audit --no-fund pnpm@10.33.2
export PATH="$ROOT/.design-tools/bootstrap/node_modules/.bin:$B:$PATH"; export ELECTRON_SKIP_BINARY_DOWNLOAD=1
run open-design-dependencies bash -c 'cd "$1" && pnpm install --filter "@open-design/daemon..." --frozen-lockfile --ignore-scripts' _ "$V/open-design"
run open-design-build bash -c 'cd "$1" && pnpm --filter "@open-design/daemon..." -r --workspace-concurrency=2 --if-present run build' _ "$V/open-design"
run open-design-help node "$V/open-design/apps/daemon/bin/od.mjs" --help
run open-design-lint node --experimental-strip-types tools/design/lint-opendesign.mjs
find "$ROOT/.agents/skills" "$ROOT/.claude" -maxdepth 3 \( -name SKILL.md -o -type l \) > "$E/installed-paths.txt" 2>/dev/null || true
python3 - <<'PY'
import csv,json,hashlib,pathlib,shutil,sys
r=pathlib.Path.cwd(); rows=list(csv.DictReader(open('tool-evidence/commands.tsv'),delimiter='\t'))
allowed={'impeccable-detect':{'0','2'},'impeccable-rendered':{'0','2'}}
bad=[x for x in rows if x['exit_code'] not in allowed.get(x['step'],{'0'})]
if bad: print('FAILED COMMANDS',bad);sys.exit(1)
# Only explicitly named generated files enter the trusted branch-storage job.
paths=['docs/index.html','docs/tr/index.html','docs/assets/opendesign.css','design-notes/opendesign-component.json','design-notes/OpenDesign-LICENSE.txt']
out=r/'review-generated';out.mkdir(exist_ok=True);manifest={}
for name in paths:
 p=r/name; dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);manifest[name]=hashlib.sha256(p.read_bytes()).hexdigest()
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('All installation and functional commands passed. Detector findings preserved for review.')
PY
cat "$E/commands.tsv"
