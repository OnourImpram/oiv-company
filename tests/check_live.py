"""Verify the deployed site against this checkout, not just an HTTP 200.

Run after the GitHub Pages deployment. Uses only the Python standard library.
The bounded retry loop permits Pages and its CDN to update after a main push.
"""
import argparse
import hashlib
import os
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1] / 'docs'
DEFAULT_BASE = 'https://oiv.onourimpram.com/'
CORE = ['index.html', 'tr/index.html', 'assets/style.css', 'robots.txt', 'sitemap.xml', '.well-known/security.txt']


def get(url):
    request = Request(url, headers={'User-Agent': 'OIV-site-verification/1.0', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise ValueError(f'Expected 200, got {response.status}: {url}')
        return response.read()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def public_path(path):
    if path == 'index.html':
        return ''
    if path == 'tr/index.html':
        return 'tr/'
    return path


def resources():
    """Include all assets referenced by HTML and CSS. Never follow external URLs."""
    found = set(CORE)
    for relative in ['index.html', 'tr/index.html']:
        file = ROOT / relative
        text = file.read_text(encoding='utf-8')
        for link in re.findall(r'(?:href|src)="([^"]+)"', text):
            parsed = urlparse(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            asset = (file.parent / parsed.path).resolve()
            if asset.is_file():
                found.add(asset.relative_to(ROOT).as_posix())
    for relative in list(found):
        if not relative.endswith('.css'):
            continue
        css = ROOT / relative
        for link in re.findall(r'url\([\'\"]?([^\)\'\"]+)', css.read_text()):
            if urlparse(link).scheme:
                continue
            asset = (css.parent / link).resolve()
            if asset.is_file():
                found.add(asset.relative_to(ROOT).as_posix())
    return sorted(found)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default=DEFAULT_BASE)
    parser.add_argument('--attempts', type=int, default=24)
    parser.add_argument('--delay', type=float, default=10)
    args = parser.parse_args()
    if args.attempts < 1:
        parser.error('--attempts must be positive')
    base = args.base.rstrip('/') + '/'
    release = quote(os.environ.get('GITHUB_SHA', 'local-check'), safe='')
    for attempt in range(args.attempts):
        try:
            for relative in CORE:
                url = base + public_path(relative) + '?oiv_release=' + release
                actual = get(url)
                expected = (ROOT / relative).read_bytes()
                if digest(actual) != digest(expected):
                    raise ValueError(f'Not updated yet: {relative}')
            break
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
            print(f'Attempt {attempt + 1}/{args.attempts}: {error}', flush=True)
            if attempt == args.attempts - 1:
                raise
            time.sleep(args.delay)
    checked = resources()
    for relative in checked:
        url = base + public_path(relative) + '?oiv_release=' + release
        actual = get(url)
        expected = (ROOT / relative).read_bytes()
        if digest(actual) != digest(expected):
            raise ValueError(f'Deployed bytes differ: {relative}')
        print(f'PASS {relative} sha256={digest(actual)}', flush=True)
    # Non-public repository files must not be included in the Pages tree.
    for relative in ['README.md', 'tests/check_live.py', 'tests/test_site.py']:
        try:
            get(base + relative + '?oiv_release=' + release)
        except HTTPError as error:
            if error.code == 404:
                print(f'PASS not published: {relative}', flush=True)
                continue
            raise
        raise ValueError(f'Repository-only file was published: {relative}')
    print(f'LIVE VERIFIED: {len(checked)} page/assets match the checkout; 3 private-to-repo paths return 404.', flush=True)


if __name__ == '__main__':
    main()
