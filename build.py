#!/usr/bin/env python3
"""Stamp partials/header.html and partials/footer.html into every page.
Run after editing a partial:  python3 build.py
Pages mark the slots with <!-- header --> ... <!-- /header --> and
<!-- footer --> ... <!-- /footer -->."""
import re, os
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index.html', 'spaces/index.html', 'plan/index.html', 'directions/index.html', 'faq/index.html', 'kaplan/index.html']
hdr = open(os.path.join(ROOT, 'partials/header.html'), encoding='utf-8').read().rstrip('\n')
ftr = open(os.path.join(ROOT, 'partials/footer.html'), encoding='utf-8').read().rstrip('\n')
LOGO_ALT = 'Rocket Farm RV Park for SpaceX Contractors in Kaplan Louisiana'
changed = 0
for rel in PAGES:
    path = os.path.join(ROOT, rel)
    s = open(path, encoding='utf-8').read()
    url = '/' if rel == 'index.html' else '/' + rel.rsplit('/', 1)[0] + '/'
    def fill(t):
        t = t.replace('{{reserve}}', '#reserve' if url == '/' else '/#reserve')
        return re.sub(r'\{\{cur:([^}]+)\}\}', lambda m: ' aria-current="page"' if m.group(1) == url else '', t)
    h = fill(hdr)
    if url == '/':
        h = h.replace('<svg viewBox="0 0 24 34" aria-hidden="true">', '<svg viewBox="0 0 24 34" role="img" aria-label="%s">' % LOGO_ALT, 1)
    f = fill(ftr)
    new = re.sub(r'<!-- header -->.*?<!-- /header -->', lambda m: '<!-- header -->\n' + h + '\n<!-- /header -->', s, flags=re.S)
    new = re.sub(r'<!-- footer -->.*?<!-- /footer -->', lambda m: '<!-- footer -->\n' + f + '\n<!-- /footer -->', new, flags=re.S)
    if new != s:
        open(path, 'w', encoding='utf-8').write(new); changed += 1
print('build: %d page(s) updated' % changed)
