"""Content and release contracts. Run: python -m unittest discover -s tests -v."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'docs'
BASE = 'https://onourimpram.github.io/oiv-company/'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.tags, self.text = path, [], []
        self.feed(path.read_text(encoding='utf-8-sig'))
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
    def handle_data(self, text):
        self.text.append(text)
    def select(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]

class SiteContract(unittest.TestCase):
    def setUp(self):
        self.pages = [Page(ROOT / 'index.html'), Page(ROOT / 'tr/index.html')]
    def test_one_real_text_heading(self):
        for p in self.pages:
            self.assertEqual(len(p.select('h1')), 1)
            self.assertEqual(len(p.select('h1', id='headline')), 1)
    def test_approved_brand_copy(self):
        self.assertIn('Human insight.', ''.join(self.pages[0].text))
        self.assertIn('Denetlenebilir teknoloji.', ''.join(self.pages[1].text))
    def test_clear_primary_action(self):
        for p in self.pages:
            self.assertTrue(p.select('a', href='#contact', **{'class':'button primary'}))
    def test_unified_narrative_sections(self):
        required = ['main', 'approach', 'work', 'systems', 'products', 'collaborate', 'about', 'contact', 'register']
        for p in self.pages:
            ids = [a['id'] for _, a in p.tags if 'id' in a]
            self.assertEqual(len(ids), len(set(ids)))
            for target in required:
                self.assertIn(target, ids)
    def test_valid_local_paths_and_anchors(self):
        for p in self.pages:
            ids = {a['id'] for _, a in p.tags if 'id' in a}
            for tag, a in p.tags:
                for key in ('href', 'src'):
                    link = a.get(key, '')
                    if not link or urlparse(link).scheme:
                        continue
                    if link.startswith('#'):
                        self.assertIn(link[1:], ids)
                    else:
                        path = (p.path.parent / unquote(urlparse(link).path)).resolve()
                        self.assertTrue(path.exists(), str(path))
    def test_metadata_matches_active_host(self):
        for p, suffix in zip(self.pages, ('', 'tr/')):
            self.assertEqual(p.select('link', rel='canonical')[0]['href'], BASE + suffix)
            self.assertEqual(p.select('meta', property='og:url')[0]['content'], BASE + suffix)
            self.assertTrue(p.select('meta', property='og:image')[0]['content'].startswith(BASE))
            self.assertEqual({a['hreflang'] for a in p.select('link', rel='alternate')}, {'en','tr','x-default'})
    def test_project_sources_and_legal_links_preserved(self):
        required = ['https://github.com/OnourImpram/mneme', 'https://github.com/OnourImpram/mergen', 'https://pypi.org/project/mneme-core/', 'https://find-and-update.company-information.service.gov.uk/company/17429906']
        required += ['https://onourimpram.com/legal/' + slug + '/' for slug in ('adhdflow','clocktopus','gracerhythm','kinlore')]
        for p in self.pages:
            links = {a.get('href') for a in p.select('a')}
            for link in required:
                self.assertIn(link, links)
    def test_company_identity_preserved(self):
        for p in self.pages:
            text = ''.join(p.text)
            for item in ['ONOUR IMPRAM VENTURES LTD', '17429906', '235117532', 'WC2H 9JQ', 'onour@onourimpram.com']:
                self.assertIn(item, text)
    def test_no_executable_script_or_form(self):
        for p in self.pages:
            self.assertFalse(p.select('form'))
            self.assertTrue(all(a.get('type') == 'application/ld+json' for a in p.select('script')))
            csp = p.select('meta', **{'http-equiv':'Content-Security-Policy'})[0]['content']
            self.assertIn("default-src 'none'", csp)
            self.assertIn("form-action 'none'", csp)
    def test_email_actions_distinguish_intent(self):
        for p in self.pages:
            links = [unquote(a['href']) for a in p.select('a') if a.get('href','').startswith('mailto:')]
            self.assertGreaterEqual(len({link for link in links if '?subject=' in link}), 2)
            self.assertTrue(all(link.startswith('mailto:onour@onourimpram.com') for link in links))
    def test_app_status_not_flattened(self):
        for p in self.pages:
            self.assertEqual(len(p.select('article', **{'data-status':'published'})), 2)
            self.assertEqual(len(p.select('article', **{'data-status':'submitted'})), 4)
    def test_security_and_sitemap_host_consistent(self):
        for path in ['robots.txt', 'sitemap.xml', '.well-known/security.txt']:
            text = (ROOT / path).read_text(encoding='utf-8-sig')
            self.assertIn(BASE, text)
            self.assertNotIn('https://oiv.onourimpram.com/', text)
    def test_no_dash_or_semicolon_in_visible_copy(self):
        for p in self.pages:
            text = ''.join(p.text)
            for char in ['\u2014','\u2013']:
                self.assertNotIn(char, text)

if __name__ == '__main__':
    unittest.main()
