"""Copy the real installed OpenDesign log-list rules and record their provenance."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[2];p=R/'.design-tools/repos/open-design/design-templates/web-prototype/assets/template.html'
rules=re.findall(r'\.log-row(?:\s+\.[\w-]+|\s+h3)?\s*\{[^}]+\}',p.read_text())
if len(rules)!=4:raise RuntimeError('Upstream layout changed. Review before adapting.')
css='/* OpenDesign web-prototype. Apache-2.0. Original rules followed by OIV overrides. */\n:root{--gap-lg:32px;--border:var(--line)}\n'+'\n'.join(rules)+'\n'
css+='''.service-list .log-row{grid-template-columns:76px minmax(0,1fr) 56px;padding-block:30px}.service-list .log-row h3{font:400 clamp(25px,2.2vw,32px)/1.25 var(--serif);margin-bottom:10px}.service-list .log-row p{color:var(--muted);max-width:65ch;font-size:16px}.service-list .log-row:last-child{border-bottom:1px solid var(--line)}.service-list .log-row .meta{font:500 12px/1.5 var(--sans);color:var(--brass-dark)}.service-list .service-action{position:relative;min-width:48px;min-height:48px;display:grid;place-content:center;border:1px solid var(--line);color:var(--ink)}.service-list .service-action:hover{background:var(--navy);color:var(--on-dark)}.project-copy,.project-scope,.note,.research-copy,.research-note{max-width:72ch}@media(max-width:700px){.service-list .log-row{grid-template-columns:25px minmax(0,1fr) 44px;gap:12px;padding-block:24px}.service-list .log-row h3{font-size:25px}.service-list .log-row p{font-size:15px}.service-list .service-action{min-width:44px;min-height:44px}}\n'''
(R/'docs/assets/opendesign.css').write_text(css)
n=R/'design-notes';n.mkdir(exist_ok=True)
(n/'opendesign-component.json').write_text(json.dumps({'upstream':'nexu-io/open-design','revision':'055621c906ad78914d2cd72cdef859e7bd040de5','source':'design-templates/web-prototype/assets/template.html','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'extracted_rules':rules,'output':'docs/assets/opendesign.css'},indent=2))
(n/'OpenDesign-LICENSE.txt').write_text((R/'.design-tools/repos/open-design/LICENSE').read_text())
print('Copied original OpenDesign rules. Added OIV overrides and rendered-detector reading-width corrections.')
