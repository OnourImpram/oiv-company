"""Institutional candidate contracts, independent of the retired graphics tests."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import unittest
R=Path(__file__).resolve().parents[2]/'docs'
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__();self.path=path;self.tags=[];self.text=[];self.feed(path.read_text())
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
 def handle_data(self,d):self.text.append(d)
 def get(self,t,**attrs):return [a for tag,a in self.tags if tag==t and all(a.get(k)==v for k,v in attrs.items())]
class Institutional(unittest.TestCase):
 def setUp(self):self.pages=[Page(R/'index.html'),Page(R/'tr/index.html')]
 def test_real_headings(self):
  for p in self.pages:self.assertEqual(len(p.get('h1',id='headline')),1)
 def test_three_original_components(self):
  for p in self.pages:self.assertEqual(len(p.get('article',**{'data-source':'open-design-layout-7'})),3)
 def test_no_decorative_runtime(self):
  for p in self.pages:self.assertFalse(p.get('canvas'));self.assertFalse(p.get('button',id='motion-toggle'))
 def test_product_statuses(self):
  for p in self.pages:self.assertEqual(len(p.get('article',**{'data-status':'published'})),2);self.assertEqual(len(p.get('article',**{'data-status':'submitted'})),4)
 def test_filters_and_announcements(self):
  for p in self.pages:self.assertEqual(len([a for t,a in p.tags if t=='button' and 'data-filter' in a]),3);self.assertTrue(p.get('p',id='product-count',role='status'))
 def test_local_paths(self):
  for p in self.pages:
   ids={a['id'] for _,a in p.tags if 'id' in a}
   for _,a in p.tags:
    for key in ['src','href']:
     value=a.get(key,'');u=urlparse(value)
     if not value or u.scheme:continue
     if value.startswith('#'):self.assertIn(value[1:],ids)
     else:self.assertTrue((p.path.parent/u.path).exists(),value)
 def test_current_host(self):
  for p in self.pages:self.assertTrue(p.get('link',rel='canonical')[0]['href'].startswith('https://oiv.onourimpram.com/'))
 def test_review_not_published(self):
  for p in self.pages:self.assertTrue(p.get('meta',name='robots',content='noindex, nofollow'))
 def test_identity_preserved(self):
  for p in self.pages:
   for value in ['ONOUR IMPRAM VENTURES LTD','17429906','235117532','WC2H 9JQ','onour@onourimpram.com']:self.assertIn(value,''.join(p.text))
 def test_no_remote_scripts_or_forms(self):
  for p in self.pages:
   self.assertFalse(p.get('form'))
   for a in p.get('script'):
    if a.get('type')!='application/ld+json':self.assertTrue(a['src'].endswith('institutional.js'))
 def test_no_tracking_or_storage(self):
  s=(R/'assets/institutional.js').read_text()
  for word in ['fetch(','localStorage','sessionStorage','XMLHttpRequest','getContext(']:self.assertNotIn(word,s)
 def test_metadata_and_context_sources(self):
  for p in self.pages:
   links={a.get('href') for a in p.get('a')}
   for url in ['https://github.com/OnourImpram/mergen','https://github.com/OnourImpram/mneme','https://pypi.org/project/mneme-core/']:self.assertIn(url,links)
if __name__=='__main__':unittest.main()
