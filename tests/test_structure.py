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
 def test_all_pages_present(self):self.assertEqual(len(self.pages),27)
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
   self.assertEqual({a['hreflang'] for a in p.select('link',rel='alternate')},{'tr','en'})
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
 def test_sitemap_is_complete(self):
  self.assertEqual((ROOT/'sitemap.xml').read_text(encoding='utf-8').count('<url>'),26)
 def test_search_is_offline(self):
  text=(ROOT/'assets/js/site.js').read_text(encoding='utf-8');self.assertNotIn('fetch(',text);self.assertNotIn('localStorage',text);self.assertNotIn('sessionStorage',text)
if __name__=='__main__':unittest.main(verbosity=2)
