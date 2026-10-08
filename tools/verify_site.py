"""Offline checks for anchors, assets, privacy and basic semantic structure."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


html = (ROOT / 'index.html').read_text(encoding='utf-8')
doc = Document()
doc.feed(html)
errors = []
ids = [a['id'] for _, a in doc.elements if 'id' in a]
errors += [f'Duplicate ID: {key}' for key, count in Counter(ids).items() if count > 1]
for tag, attrs in doc.elements:
    for attr in ('href', 'src'):
        value = attrs.get(attr, '')
        if not value:
            continue
        if value.startswith('#'):
            if value[1:] not in ids:
                errors.append(f'Missing fragment: {value}')
        elif value.startswith('https://'):
            if tag == 'a' and not {'noopener', 'noreferrer'}.issubset(set(attrs.get('rel', '').split())):
                errors.append(f'Unsafe external link: {value}')
        elif value.startswith(('http:', 'mailto:', 'javascript:')):
            errors.append(f'Unexpected URL scheme: {value}')
        elif not (ROOT / value).is_file():
            errors.append(f'Missing local resource: {value}')
    if tag == 'img' and not attrs.get('alt'):
        errors.append('Image without alternative text')
    if tag == 'svg' and attrs.get('aria-hidden') != 'true':
        errors.append('Decorative SVG exposed to assistive technology')

css = (ROOT / 'css/styles.css').read_text(encoding='utf-8')
for asset in re.findall(r'url\([\'"]?([^\)\'\"]+)', css):
    if not (ROOT / 'css' / asset).is_file():
        errors.append(f'Missing CSS asset: {asset}')
for font in (ROOT / 'assets/fonts').glob('*.woff2'):
    if font.read_bytes()[:4] != b'wOF2':
        errors.append(f'Invalid WOFF2 file: {font.name}')
if sum(tag == 'h1' for tag, _ in doc.elements) != 1:
    errors.append('Expected exactly one H1')
if re.search(r'[\w.+-]+@[\w.-]+\.[a-z]{2,}', html, re.I):
    errors.append('An email address is exposed in the page')
if re.search(r'lorem ipsum|placeholder|coming soon|href=[\'"]#[\'"]', html, re.I):
    errors.append('Placeholder content found')
for phrase in ('EU Project Analyst', '14 September 2026', 'October 2025 – September 2026',
               'Degree awarded: March 2025', 'MyFarm'):
    if phrase not in html:
        errors.append(f'Missing confirmed content: {phrase}')
for phrase in ('RECEA', 'FoodTrust AI'):
    if phrase in html:
        errors.append(f'Project is not cleared for public listing: {phrase}')
if 'prefers-reduced-motion' not in css or ':focus-visible' not in css:
    errors.append('Missing reduced-motion or visible-focus styles')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(ids)} unique IDs; fragment links and local assets resolve.')
print('PASS: external-link attributes, WOFF2 signatures, heading and icon semantics.')
print('PASS: no public email or placeholder content; confirmed role/date/project checks.')
print('PASS: reduced-motion and keyboard-focus styles present.')
print('Browser, screen-reader and external destination checks remain separate.')
