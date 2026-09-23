"""Release requirements written before the Precision implementation."""
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
ROOT=Path(__file__).resolve().parents[1]/'docs'
class HTML(HTMLParser):
 def __init__(self,path):
  super().__init__();self.tags=[];self.path=path;self.feed(path.read_text())
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
 def get(self,t,**kw):return [a for tag,a in self.tags if tag==t and all(a.get(k)==v for k,v in kw.items())]
class Precision(unittest.TestCase):
 def setUp(self):self.pages=[HTML(ROOT/'index.html'),HTML(ROOT/'tr/index.html')]
 def test_new_refinement_present(self):
  for p in self.pages:self.assertTrue(p.get('body',**{'data-edition':'precision'}))
 def test_contextual_contact(self):
  for p in self.pages:
   self.assertTrue(p.get('textarea',id='brief-description',maxlength='1200'))
   self.assertTrue(p.get('button',id='copy-brief'))
   self.assertTrue(p.get('a',id='email-brief'))
 def test_consentful_motion_and_view_switch(self):
  for p in self.pages:
   self.assertTrue(p.get('button',id='motion-toggle',**{'aria-pressed':'true'}))
   self.assertTrue(p.get('button',**{'data-view':'wire'}))
 def test_visible_published_products(self):
  for p in self.pages:
   self.assertTrue(p.get('div',id='published-apps'))
   self.assertEqual(len(p.get('article',**{'data-status':'published'})),2)
   self.assertEqual(len(p.get('article',**{'data-status':'submitted'})),4)
 def test_sources_and_bounds_preserved(self):
  for p in self.pages:
   s=p.path.read_text();self.assertIn('17429906',s);self.assertIn('235117532',s)
   for n in ['mneme','mergen']:self.assertIn('https://github.com/OnourImpram/'+n,s)
 def test_local_links_are_valid(self):
  for p in self.pages:
   ids=[a['id'] for t,a in p.tags if 'id' in a];self.assertEqual(len(ids),len(set(ids)))
   for t,a in p.tags:
    for k in ['src','href']:
     u=urlparse(a.get(k,''))
     if u.scheme or u.netloc:continue
     if not u.path:
      if u.fragment:self.assertIn(unquote(u.fragment),ids)
     else:self.assertTrue((p.path.parent/unquote(u.path)).resolve().exists(),u.path)
 def test_security_no_server_submission(self):
  for p in self.pages:
   self.assertFalse(p.get('form'))
   c=p.get('meta',**{'http-equiv':'Content-Security-Policy'})[0]['content']
   self.assertIn("form-action 'none'",c);self.assertNotIn('unsafe-inline',c)
 def test_no_external_dependencies_or_tracking(self):
  for p in self.pages:
   for t in ['script','img']:
    for a in p.get(t):self.assertFalse(urlparse(a.get('src','')).scheme)
 def test_metadata(self):
  for p,s in zip(self.pages,['','tr/']):self.assertEqual(p.get('link',rel='canonical')[0]['href'],'https://oiv.onourimpram.com/'+s)
 def test_real_headings_and_images(self):
  for p in self.pages:
   self.assertEqual(len(p.get('h1')),1)
   for a in p.get('img'):self.assertIn('alt',a);self.assertIn('width',a);self.assertIn('height',a)
 def test_static_sculpture_exists(self):self.assertTrue((ROOT/'assets/art/continuum-static.svg').exists())
 def test_webgl_replaces_cpu_polygon_sorting(self):
  s=(ROOT/'assets/site.js').read_text();self.assertIn("getContext('webgl'",s);self.assertIn('gl.drawElements',s)
 def test_motion_observers_and_reduced_motion(self):
  s=(ROOT/'assets/site.js').read_text()
  for q in ['prefers-reduced-motion','visibilitychange','IntersectionObserver','webglcontextlost']:self.assertIn(q,s)
 def test_404_exists(self):self.assertTrue((ROOT/'404.html').exists())
if __name__=='__main__':unittest.main()
