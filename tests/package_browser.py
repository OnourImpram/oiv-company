"""Run UI checks against local HTTP or an explicitly labelled in-memory render.
Requires playwright and beautifulsoup4. No writes outside the local package.
Normal run: python tests/browser.py
Restricted renderer: python tests/browser.py --memory
"""
from pathlib import Path
import argparse,base64,json,mimetypes,re,threading,http.server,functools
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'docs';OUT=ROOT/'test-evidence/package-browser';OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--memory',action='store_true');parser.add_argument('--interactions-only',action='store_true');parser.add_argument('--chrome',default='/usr/bin/chromium');args=parser.parse_args()
results=[];faults=[]
def check(name,value):
 results.append({'check':name,'passed':bool(value)})
 if not value:faults.append(name)
 print(('PASS ' if value else 'FAIL ')+name,flush=True)
def data_uri(p):return 'data:'+(mimetypes.guess_type(str(p))[0] or 'application/octet-stream')+';base64,'+base64.b64encode(p.read_bytes()).decode()
def memory_doc(path,js=True):
 soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
 # In-memory layout review only. Production CSP is not altered on disk.
 for x in soup.select('meta[http-equiv="Content-Security-Policy"]'):x.decompose()
 for x in list(soup.select('link[rel="stylesheet"]')):
  p=WEB/x['href'].lstrip('/') if x['href'].startswith('/') else (path.parent/x['href']).resolve()
  css=p.read_text(encoding='utf-8')
  css=re.sub(r'url\([\'\"]?([^\)\'\"]+)[\'\"]?\)',lambda m:'url("'+data_uri((p.parent/m[1]).resolve())+'")',css)
  tag=soup.new_tag('style');tag.string=css;x.replace_with(tag)
 for x in list(soup.select('link[rel="icon"]')):x.decompose()
 for x in soup.select('img[src]'):x['src']=data_uri((path.parent/x['src']).resolve());x['loading']='eager'
 scripts=[]
 for x in list(soup.select('script[src]')):
  if js:scripts.append((path.parent/x['src']).resolve().read_text(encoding='utf-8'))
  x.decompose()
 for code in scripts:
  tag=soup.new_tag('script');tag.string=code;soup.body.append(tag)
 return str(soup)
server=None
if not args.memory:
 handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(WEB))
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);threading.Thread(target=server.serve_forever,daemon=True).start()
 base=f'http://127.0.0.1:{server.server_port}/'
def load(page,rel,js=True):
 if args.memory:page.set_content(memory_doc(WEB/rel,js),wait_until='load')
 else:page.goto(base+rel,wait_until='networkidle')
 page.wait_for_timeout(35)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=args.chrome if Path(args.chrome).exists() else None,headless=True,args=['--no-sandbox'])
 for width in ([] if args.interactions_only else [320,390,768,1440]):
  page=browser.new_page(viewport={'width':width,'height':950},device_scale_factor=1)
  for path in sorted(WEB.rglob('*.html')):
   rel=path.relative_to(WEB).as_posix();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   load(page,rel)
   layout=page.evaluate('''() => ({width:document.documentElement.scrollWidth,images:[...document.images].every(i=>i.complete&&i.naturalWidth>0),head:[...document.querySelectorAll('h1')].every(e=>{let r=e.getBoundingClientRect();return r.right<=innerWidth+1&&r.left>=-1})})''')
   check(f'{rel}/{width}/no-overflow',layout['width']<=width+1)
   check(f'{rel}/{width}/images',layout['images'])
   check(f'{rel}/{width}/heading',layout['head'])
   check(f'{rel}/{width}/javascript',not errors)
   if rel in ['index.html','tr/index.html'] and width in [390,1440]:
    label='TR' if rel.startswith('tr/') else 'EN';page.screenshot(path=str(OUT/f'{label}-{width}.png'));page.screenshot(path=str(OUT/f'{label}-{width}-full.png'),full_page=True)
  page.close()
 for lang in ['tr','en']:
  rel='tr/index.html' if lang=='tr' else 'index.html'
  page=browser.new_page(viewport={'width':390,'height':844},accept_downloads=True);page.set_default_timeout(5000)
  load(page,rel)
  page.locator('.menu-toggle').click();check(f'{lang}/menu-open',page.locator('#main-nav').is_visible())
  page.keyboard.press('Escape');check(f'{lang}/menu-escape-focus',page.evaluate('document.activeElement.classList.contains("menu-toggle")'))
  page.locator('.search-toggle').click();check(f'{lang}/search-dialog',page.locator('#site-search').evaluate('(e)=>e.open'))
  page.locator('#search-input').fill('is akis' if lang=='tr' else 'workflows');check(f'{lang}/search-results',page.locator('#search-results a').count()>0)
  page.locator('#search-input').fill('zzzzzz');check(f'{lang}/search-empty',page.locator('#search-results a').count()==0)
  page.keyboard.press('Escape');check(f'{lang}/search-escape',not page.locator('#site-search').evaluate('(e)=>e.open'))
  work='tr/calismalar.html' if lang=='tr' else 'work.html';load(page,work)
  page.locator('[data-filter="source"]').click();check(f'{lang}/filter-source',page.locator('[data-category]:visible').count()==2)
  page.locator('[data-filter="product"]').focus();page.keyboard.press('Enter');check(f'{lang}/filter-keyboard',page.locator('[data-category]:visible').count()==6)
  page.locator('[data-filter="all"]').click();check(f'{lang}/filter-reset',page.locator('[data-category]:visible').count()==8)
  contact='tr/iletisim.html' if lang=='tr' else 'contact.html';load(page,contact)
  page.locator('#brief-form button[type="submit"]').click();check(f'{lang}/validation-empty',page.locator('#message-error').is_visible())
  page.locator('#message').fill('Kurumumuz için iş akışları ve eğitim konusunda bir görüşme yapmak istiyoruz.')
  page.locator('#email').fill('invalid');page.locator('#brief-form button[type="submit"]').click();check(f'{lang}/validation-email',page.locator('#email-error').is_visible())
  page.locator('#email').fill('');page.locator('#topic').select_option('training');page.locator('#name').fill('Test Visitor')
  page.locator('#brief-form button[type="submit"]').click();check(f'{lang}/preview',page.locator('#brief-preview').is_visible())
  check(f'{lang}/preview-content','Test Visitor' in page.locator('#brief-text').input_value())
  check(f'{lang}/fixed-recipient',page.locator('#email-draft').get_attribute('href').startswith('mailto:onour@onourimpram.com?subject='))
  with page.expect_download() as download:
   page.locator('#save-brief').click()
  content=Path(download.value.path()).read_text(encoding='utf-8-sig');check(f'{lang}/download',content==page.locator('#brief-text').input_value())
  page.locator('#copy-brief').click();check(f'{lang}/copy-feedback',len(page.locator('#copy-result').inner_text())>0)
  page.locator('.edit-brief').click();check(f'{lang}/edit-preserves',page.locator('#name').input_value()=='Test Visitor')
  page.locator('#message').fill('İ'.ljust(2500,'İ'));page.locator('#brief-form button[type="submit"]').click()
  check(f'{lang}/long-note',page.locator('.long-brief-note').is_visible());check(f'{lang}/bounded-email-url',len(page.locator('#email-draft').get_attribute('href'))<1800)
  # Save a complete functional-state screenshot.
  page.set_viewport_size({'width':1440,'height':1000});load(page,contact);page.screenshot(path=str(OUT/f'{lang}-contact.png'),full_page=True)
  if args.memory:
   load(page,rel,js=False);check(f'{lang}/no-js-navigation',page.locator('#main-nav').is_visible())
   check(f'{lang}/no-js-services',page.locator('.solution-card').count()==5)
  page.close()
 # Larger accessibility-related layout cases, with movement suppressed.
 page=browser.new_page(viewport={'width':1920,'height':1080},reduced_motion='reduce')
 load(page,'tr/index.html');check('reduced-motion',page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto')
 check('wide-layout',page.evaluate('document.documentElement.scrollWidth')==1920)
 page.set_viewport_size({'width':320,'height':900});load(page,'tr/index.html');page.add_style_tag(content='body{font-size:200%}')
 check('text-resize-page-overflow',page.evaluate('document.documentElement.scrollWidth')<=321)
 page.close();browser.close()
if server:server.shutdown()
report={'mode':'memory render, CSP omitted only in transient documents' if args.memory else 'local HTTP, production CSP retained','checks':len(results),'passed':len(results)-len(faults),'failed':faults,'results':results}
(OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False,indent=2))
raise SystemExit(bool(faults))
