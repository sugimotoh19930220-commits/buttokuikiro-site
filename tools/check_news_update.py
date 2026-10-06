"""Verify the approved 2026-10-07 news addition against its production base."""
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
BASE = '65c91c99b5fead64729d97164c572215ef7e6db4'
NEW = '2026-10-07-noodle-update'
LANGS = ['', 'en/', 'ko/', 'zh-hans/', 'zh-hant/']
OLD = ['2026-10-duck-mazesoba', '2026-10-opening-hours', '2026-10-buttoku-day']

def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:public/{path}'], cwd=ROOT)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.canonical = []
        self.dates = []
        self.entries = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('a', 'link') and 'href' in a:
            self.links.append(a['href'])
        if tag in ('img', 'script', 'video') and 'src' in a:
            self.links.append(a['src'])
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a['href'])
        if tag == 'time':
            self.dates.append(a.get('datetime'))
        if tag == 'a' and a.get('class') == 'news-entry':
            self.entries.append(a)

strip_news = lambda s: re.sub(r'<!-- NEWS START -->.*?<!-- NEWS END -->', '', s, flags=re.S)
for prefix in LANGS:
    home_path = prefix + 'index.html'
    home = (PUBLIC / home_path).read_text()
    assert strip_news(home) == strip_news(original(home_path).decode()), home_path
    section = re.search(r'<!-- NEWS START -->.*?<!-- NEWS END -->', home, re.S).group()
    p = Parser(); p.feed(section)
    assert len(p.entries) == 3 and p.entries[0]['href'] == '/' + prefix + 'news/' + NEW + '/', prefix
    assert p.dates == ['2026-10-07', '2026-10-03', '2026-10-03'], prefix
    assert 'data-valid-until' not in p.entries[0], prefix
    for slug in OLD:
        rel = prefix + 'news/' + slug + '/index.html'
        assert (PUBLIC / rel).read_bytes() == original(rel), rel
    rel = prefix + 'news/index.html'
    p = Parser(); p.feed((PUBLIC / rel).read_text())
    assert len(p.entries) == 4 and p.dates == ['2026-10-07'] + ['2026-10-03'] * 3, rel
    rel = prefix + 'news/' + NEW + '/index.html'
    s = (PUBLIC / rel).read_text(); p = Parser(); p.feed(s)
    assert p.canonical == ['https://buttokuikiro.com/' + prefix + 'news/' + NEW + '/'], rel
    assert p.dates == ['2026-10-07'] and '村上朝日製麺' in s, rel
    assert 'instagram.com' not in s and 'news-duck-202610.jpg' not in s, rel
    schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))
    assert schema['datePublished'][:10] == '2026-10-07' and schema['headline'], rel
    assert len(re.findall(r'rel="alternate"', s)) == 6, rel

for rel in ['news.css', 'recruit/index.html', 'robots.txt', 'llms.txt']:
    if (PUBLIC / rel).exists():
        assert (PUBLIC / rel).read_bytes() == original(rel), rel

for path in PUBLIC.rglob('*.html'):
    s = path.read_text(); p = Parser(); p.feed(s)
    for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        json.loads(data)
    for href in p.links:
        url = urlsplit(href)
        if url.scheme or url.netloc or not url.path:
            continue
        target = PUBLIC / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)
        if url.path.endswith('/'):
            target = target / 'index.html'
        assert target.exists(), f'{path.relative_to(PUBLIC)} -> {href}'

ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
tree = ET.parse(PUBLIC / 'sitemap.xml')
urls = {u.find('s:loc', ns).text: u.find('s:lastmod', ns).text for u in tree.findall('s:url', ns)}
for prefix in LANGS:
    assert urls['https://buttokuikiro.com/' + prefix + 'news/' + NEW + '/'] == '2026-10-07'
    for slug in OLD:
        assert urls['https://buttokuikiro.com/' + prefix + 'news/' + slug + '/'] == '2026-10-03'

approved = [
    '麺の仕入れ先を村上朝日製麺へ変更し、製麺に使用する切刃も3番から4番へ変更しました。',
    '国産もち小麦の使用割合を、従来の約3割から約8割へ高めたことで、もちもちとした食感がさらに強くなりました。茹で時間も短くなり、これまで以上に美味しくなった麺を、ぜひお楽しみください。',
]
s = (PUBLIC / 'news' / NEW / 'index.html').read_text()
assert all('<p>' + text + '</p>' in s for text in approved)
print('PASS: 5 languages; one new article; home latest 3; archive 4; approved copy; old articles/dates, design, non-news content preserved; JSON-LD, sitemap and local links valid.')
