"""Standard-library release contracts for the OIV Continuum redesign."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import unittest
ROOT=Path(__file__).resolve().parents[1]/'docs'
BASE='https://onourimpram.github.io/oiv-company/'
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__();self.path=path;self.tags=[];self.text=[];self.feed(path.read_text())
 def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))
 def handle_data(self,data): self.text.append(data)
 def select(self,tag,**attrs): return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in attrs.items())]
class SiteContract(unittest.TestCase):
 def setUp(self):self.pages=[Page(ROOT/'index.html'),Page(ROOT/'tr/index.html')]
 def test_new_identity_not_old_template(self):
  for p in self.pages:
   self.assertTrue(p.select('body',**{'data-design':'continuum'}))
   self.assertEqual(len(p.select('h1',id='headline')),1)
  self.assertIn('In human',''.join(self.pages[0].text));self.assertIn('İnsanın',''.join(self.pages[1].text))
 def test_clear_primary_action(self):
  for p in self.pages:self.assertTrue(p.select('a',href='#contact',**{'data-primary':'true'}))
 def test_preserved_ids(self):
  for p in self.pages:
   ids=[a['id'] for _,a in p.tags if 'id' in a];self.assertEqual(len(ids),len(set(ids)))
   for i in ['main','approach','work','systems','products','collaborate','about','contact','register']:self.assertIn(i,ids)
 def test_no_broken_local_paths(self):
  for p in self.pages:
   ids={a['id'] for _,a in p.tags if 'id' in a}
   for _,a in p.tags:
    for k in ['src','href']:
     v=a.get(k,'');u=urlparse(v)
     if not v or u.scheme:continue
     if v.startswith('#'):self.assertIn(v[1:],ids)
     else:self.assertTrue((p.path.parent/unquote(u.path)).exists(),v)
 def test_metadata(self):
  for p,s in zip(self.pages,['','tr/']):
   self.assertEqual(p.select('link',rel='canonical')[0]['href'],BASE+s)
   self.assertEqual(p.select('meta',property='og:url')[0]['content'],BASE+s)
   self.assertEqual({a['hreflang'] for a in p.select('link',rel='alternate')},{'en','tr','x-default'})
 def test_company_identity(self):
  for p in self.pages:
   for s in ['ONOUR IMPRAM VENTURES LTD','17429906','235117532','WC2H 9JQ','onour@onourimpram.com']:self.assertIn(s,''.join(p.text))
 def test_real_sources_and_legal_links(self):
  refs=['https://github.com/OnourImpram/mneme','https://github.com/OnourImpram/mergen','https://pypi.org/project/mneme-core/','https://find-and-update.company-information.service.gov.uk/company/17429906']
  refs+=['https://onourimpram.com/legal/'+s+'/' for s in ['gracerhythm','adhdflow','clocktopus','kinlore']]
  for p in self.pages:
   for r in refs:self.assertIn(r,[a.get('href') for a in p.select('a')])
 def test_dated_application_status(self):
  for p in self.pages:
   self.assertEqual(len(p.select('article',**{'data-status':'published'})),2)
   self.assertEqual(len(p.select('article',**{'data-status':'submitted'})),4)
   self.assertIn('2026',''.join(p.text))
 def test_art_has_accessible_pause_and_fallback(self):
  for p in self.pages:
   self.assertTrue(p.select('button',id='motion-toggle'))
   self.assertTrue(p.select('canvas',id='continuum'))
   self.assertTrue(p.select('div',**{'class':'sculpture-fallback'}))
 def test_no_untrusted_scripts_forms_or_trackers(self):
  for p in self.pages:
   c=p.select('meta',**{'http-equiv':'Content-Security-Policy'})[0]['content']
   self.assertIn("default-src 'none'",c);self.assertIn("script-src 'self'",c);self.assertNotIn('unsafe-inline',c)
   self.assertFalse(p.select('form'))
   for a in p.select('script'):
    if a.get('type')!='application/ld+json':self.assertTrue(a.get('src','').endswith('site.js'));self.assertIn('defer',a)
 def test_motion_is_optional(self):
  self.assertTrue((ROOT/'assets/site.js').exists());css=(ROOT/'assets/style.css').read_text();js=(ROOT/'assets/site.js').read_text()
  self.assertIn('prefers-reduced-motion',css);self.assertIn('prefers-reduced-motion',js)
  self.assertIn('visibilitychange',js);self.assertIn('IntersectionObserver',js)
 def test_business_and_support_are_separate(self):
  for p in self.pages:
   links=[unquote(a['href']) for a in p.select('a') if a.get('href','').startswith('mailto:')]
   self.assertGreaterEqual(len(set(links)),3)
   self.assertTrue(all(l.startswith('mailto:onour@onourimpram.com') for l in links))
 def test_security_sitemap_preserved(self):
  for name in ['robots.txt','sitemap.xml','.well-known/security.txt']:self.assertIn(BASE,(ROOT/name).read_text())
if __name__=='__main__':unittest.main()
