"""Offline release checks. No deployment, network access or third party libraries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import unittest,json,re
ROOT=Path(__file__).resolve().parents[1]/'docs'
class HTML(HTMLParser):
 def __init__(self,path):
  super().__init__();self.path=path;self.tags=[];self.feed(path.read_text(encoding='utf-8'))
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
 def select(self,tag,**attrs):return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in attrs.items())]
class Release(unittest.TestCase):
 def setUp(self):self.pages=[HTML(p) for p in ROOT.rglob('*.html')]
 # 39 built pages + 23 EN and 23 TR Google Play app pages + 11 EN and 11 TR app policies from tools/yasal-sayfa-uret.py.
 def test_all_pages_present(self):self.assertEqual(len(self.pages),107)
 def test_one_heading_each(self):
  for p in self.pages:self.assertEqual(len(p.select('h1')),1,str(p.path))
 def test_ids_are_unique(self):
  for p in self.pages:
   ids=[a['id'] for t,a in p.tags if 'id' in a];self.assertEqual(len(ids),len(set(ids)),str(p.path))
 def test_local_assets_and_cross_page_anchors(self):
  for p in self.pages:
   for tag,a in p.tags:
    for field in ['href','src']:
     raw=a.get(field,'');u=urlsplit(raw)
     if not raw or u.scheme:continue
     target=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else (p.path.parent/unquote(u.path)) if u.path else p.path
     if target.is_dir():target=target/'index.html'
     self.assertTrue(target.exists(),str(p.path)+' '+raw)
     if u.fragment and target.suffix=='.html':self.assertTrue(any(x.get('id')==unquote(u.fragment) for t,x in HTML(target).tags),raw)
 def test_external_scripts_not_required(self):
  for p in self.pages:
   for a in p.select('script'):
    if a.get('src'):self.assertFalse(urlsplit(a['src']).scheme)
 def test_canonical_and_languages(self):
  for p in self.pages:
   if p.path.name=='404.html':continue
   self.assertTrue(p.select('link',rel='canonical')[0]['href'].startswith('https://oiv.onourimpram.com/'))
   langs={a['hreflang'] for a in p.select('link',rel='alternate')}
   self.assertTrue({'tr','en'}<=langs<={'tr','en','x-default'},str(p.path))   # x-default only on the app pages
 def test_all_five_solutions_at_home(self):
  for p in [HTML(ROOT/'index.html'),HTML(ROOT/'tr/index.html')]:
   self.assertEqual(len([a for t,a in p.tags if a.get('class')=='solution-card']),5)
   self.assertEqual(len([a for t,a in p.tags if a.get('class','').startswith('compass-node')]),5)
 def test_no_disallowed_demo_or_placeholder(self):
  for p in self.pages:
   text=p.path.read_text(encoding='utf-8');self.assertFalse(p.select('canvas'));self.assertNotIn('href="#"',text);self.assertNotIn('Lorem ipsum',text)
 def test_no_font_binaries(self):
  self.assertFalse([p for p in ROOT.rglob('*') if p.suffix.lower() in ['.woff','.woff2','.ttf','.otf']])
 def test_assets_have_alt_and_dimensions(self):
  for p in self.pages:
   for a in p.select('img'):
    self.assertIn('alt',a);self.assertIn('width',a);self.assertIn('height',a)
 def test_security_and_no_fake_form_action(self):
  for p in self.pages:
   if p.path.name=='404.html':continue
   c=p.select('meta',**{'http-equiv':'Content-Security-Policy'})[0]['content']
   for rule in ["connect-src 'none'","form-action 'none'","script-src 'self'"]:self.assertIn(rule,c)
   for a in p.select('form'):self.assertFalse(a.get('action'))
 def test_company_and_email_preserved(self):
  for p in self.pages:
   if p.path.name=='404.html':continue
   text=p.path.read_text(encoding='utf-8');self.assertIn('17429906',text);self.assertIn('ONOUR IMPRAM VENTURES LTD',text)
   for a in p.select('a'):
    if a.get('href','').startswith('mailto:'):self.assertTrue(a['href'].startswith('mailto:onour@onourimpram.com'))
 def test_motion_layers_decorative_and_heading_text_kept(self):
  # The values cycle and the process flow add only aria-hidden layers; the heading still reads as written.
  for path,lang in [(ROOT/'index.html','en'),(ROOT/'tr/index.html','tr')]:
   text=path.read_text(encoding='utf-8')
   title=json.loads((ROOT.parent/'src/content.json').read_text(encoding='utf-8'))[lang]['aboutTitle']
   m=re.search(r'<span class="cycle" data-loop>(.*?)<span class="cycle-track" aria-hidden="true"><span class="cycle-light"></span></span></span>',text)
   self.assertTrue(m,str(path))
   self.assertEqual(re.sub(r'<[^>]+>','',m.group(1)),title.replace('<br>',' '))
   self.assertIn('<ol class="process-list" data-loop>',text)
   self.assertEqual(text.count('<i aria-hidden="true"><b></b></i>'),5)
   # The cycle's meaning reaches screen readers as one sentence inside the values band.
   cycle=json.loads((ROOT.parent/'src/content.json').read_text(encoding='utf-8'))[lang]['aboutCycle']
   self.assertIn('</h2><p class="sr-only">'+cycle+'</p>',text)
 # Legal pages (app privacy policies and terms, both languages) stay public but out of search (2026-10-06, decision a7177e8b):
 # <meta name="robots" content="noindex"> on every one, no sitemap entry, no link added to the home page, robots.txt still open.
 def legal_pages(self):return [p for p in self.pages if p.path.name=='index.html' and p.path.parent.parent.name in ('legal','yasal')]
 def robots(self,p):return [a.get('content') for a in p.select('meta',name='robots')]
 def test_legal_pages_are_noindex(self):
  legal=self.legal_pages()
  self.assertEqual(len(legal),34)   # 17 EN + 17 TR; a glob that finds nothing must not pass
  for p in legal:self.assertEqual(self.robots(p),['noindex'],str(p.path))
 def test_other_pages_stay_indexable(self):
  legal={id(p) for p in self.legal_pages()}
  for p in self.pages:
   if id(p) in legal or p.path.name=='404.html':continue   # the 404 is noindex by design
   self.assertEqual(self.robots(p),[],str(p.path))
 def test_sitemap_is_complete(self):
  # Every page except the 404 and the noindex legal pages is listed (a noindex URL in a sitemap contradicts itself).
  self.assertEqual((ROOT/'sitemap.xml').read_text(encoding='utf-8').count('<url>'),len(self.pages)-1-len(self.legal_pages()))
 def test_sitemap_has_no_legal_entries(self):
  locs=re.findall(r'<loc>([^<]+)</loc>',(ROOT/'sitemap.xml').read_text(encoding='utf-8'))
  for u in ['https://oiv.onourimpram.com/','https://oiv.onourimpram.com/tr/','https://oiv.onourimpram.com/apps/platekind/']:self.assertIn(u,locs)   # positive arm: the rest is still listed
  self.assertEqual([u for u in locs if '/legal/' in u or '/yasal/' in u],[])
 def test_robots_txt_still_lets_crawlers_read_the_noindex(self):
  # A Disallow would hide the noindex from crawlers and leave the URLs indexable by link.
  self.assertNotIn('Disallow',(ROOT/'robots.txt').read_text(encoding='utf-8'))
 def test_home_pages_add_no_link_to_legal(self):
  for rel in ['index.html','tr/index.html']:
   for t,a in HTML(ROOT/rel).tags:self.assertNotRegex(a.get('href',''),r'(^|/)(legal|yasal)/',rel)
 def test_search_is_offline(self):
  text=(ROOT/'assets/js/site.js').read_text(encoding='utf-8');self.assertNotIn('fetch(',text);self.assertNotIn('localStorage',text);self.assertNotIn('sessionStorage',text)
if __name__=='__main__':unittest.main(verbosity=2)
