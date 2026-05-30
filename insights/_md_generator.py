#!/usr/bin/env python3
"""
Generate clean .md markdown endpoints for every insights/*.html post.
Also injects <link rel="alternate" type="text/markdown"> into each HTML head if missing.

Run from anywhere. Idempotent.
"""

import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

POSTS_DIR = Path(__file__).parent
SITE_ROOT = "https://fixyourrevenueengine.com"


def get_meta(soup, name=None, prop=None):
    if name:
        tag = soup.find('meta', attrs={'name': name})
    else:
        tag = soup.find('meta', attrs={'property': prop})
    return tag['content'] if tag and tag.has_attr('content') else ''


def get_title(soup):
    t = soup.find('title')
    if not t:
        return ''
    txt = t.get_text(strip=True)
    # Strip " | Revved for Growth" suffix
    return re.sub(r'\s*\|\s*Revved for Growth\s*$', '', txt)


def node_to_md(node, depth=0):
    """Convert a BeautifulSoup node into markdown."""
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag):
        return ''

    name = node.name.lower()

    # Skip things that don't belong in the markdown body
    if name in ('script', 'style'):
        return ''
    if 'post-cta' in (node.get('class') or []):
        return ''
    if 'related-posts' in (node.get('class') or []):
        return ''

    # TL;DR block
    if 'tldr' in (node.get('class') or []):
        p = node.find('p')
        text = p.get_text(' ', strip=True) if p else ''
        return f"\n> **TL;DR.** {text}\n\n"

    # FAQ section
    if 'post-faq' in (node.get('class') or []):
        out = ["\n## Frequently asked\n"]
        for item in node.select('.faq-item'):
            q = item.select_one('.faq-q')
            a = item.select_one('.faq-a')
            if q and a:
                out.append(f"\n**{q.get_text(' ', strip=True)}**\n\n")
                out.append(f"{a.get_text(' ', strip=True)}\n")
        return ''.join(out) + '\n'

    # Headings
    if name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        level = int(name[1])
        text = node.get_text(' ', strip=True)
        return f"\n{'#' * level} {text}\n\n"

    # Lede quote (custom class) renders as italicized blockquote
    if 'lede-quote' in (node.get('class') or []):
        text = node.get_text(' ', strip=True)
        return f"\n> *{text}*\n\n"

    # Paragraphs
    if name == 'p':
        return node.get_text(' ', strip=True) + '\n\n'

    # Lists
    if name in ('ul', 'ol'):
        items = []
        for i, li in enumerate(node.find_all('li', recursive=False), 1):
            prefix = '- ' if name == 'ul' else f'{i}. '
            text = li.get_text(' ', strip=True)
            items.append(f"{prefix}{text}")
        return '\n'.join(items) + '\n\n'

    # Blockquotes
    if name == 'blockquote':
        text = node.get_text(' ', strip=True)
        return f"\n> {text}\n\n"

    # Tables (used on the comparison page, but also future-proof)
    if name == 'table':
        rows = node.find_all('tr')
        if not rows:
            return ''
        out = []
        for i, row in enumerate(rows):
            cells = row.find_all(['th', 'td'])
            line = '| ' + ' | '.join(c.get_text(' ', strip=True) for c in cells) + ' |'
            out.append(line)
            if i == 0:
                out.append('| ' + ' | '.join('---' for _ in cells) + ' |')
        return '\n' + '\n'.join(out) + '\n\n'

    # Divs and sections: recurse into children
    if name in ('div', 'section', 'article'):
        return ''.join(node_to_md(c, depth + 1) for c in node.children)

    # Inline formatting
    if name in ('strong', 'b'):
        return f"**{node.get_text(' ', strip=True)}**"
    if name in ('em', 'i'):
        return f"*{node.get_text(' ', strip=True)}*"
    if name == 'a':
        href = node.get('href', '')
        text = node.get_text(' ', strip=True)
        if not href:
            return text
        # Convert relative links to absolute
        if href.startswith('/') and not href.startswith('//'):
            href = SITE_ROOT + href
        elif not href.startswith('http') and not href.startswith('#') and not href.startswith('mailto:'):
            # Resolve relative to /insights/
            if href.startswith('../'):
                href = SITE_ROOT + '/' + href[3:]
            elif href.startswith('./') or not href.startswith('http'):
                href = SITE_ROOT + '/insights/' + href.lstrip('./')
        return f"[{text}]({href})"
    if name == 'br':
        return '\n'

    # Fallback: just text content
    return node.get_text(' ', strip=True)


def html_to_md(html_text, slug):
    soup = BeautifulSoup(html_text, 'html.parser')
    # Strip HTML comments so injection markers like <!-- GEO:TLDR --> don't leak
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    title = get_title(soup)
    description = get_meta(soup, name='description')
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    canonical = canonical_tag['href'] if canonical_tag else f"{SITE_ROOT}/insights/{slug}.html"

    # Extract article body
    article = soup.find('div', class_='post-article')
    if not article:
        return None

    body_md = ''.join(node_to_md(c) for c in article.children)

    # Cleanup: collapse 3+ newlines to 2
    body_md = re.sub(r'\n{3,}', '\n\n', body_md).strip()

    front_matter = (
        f"---\n"
        f"title: \"{title}\"\n"
        f"description: \"{description}\"\n"
        f"url: {canonical}\n"
        f"source: {SITE_ROOT}/insights/{slug}.html\n"
        f"---\n\n"
        f"# {title}\n\n"
    )

    return front_matter + body_md + '\n'


def inject_md_link(html_path, slug):
    """Add <link rel='alternate' type='text/markdown' href='...md'> to head if not present."""
    html = html_path.read_text(encoding='utf-8')
    md_url = f"{SITE_ROOT}/insights/{slug}.md"
    if f'href="{md_url}"' in html:
        return False
    # Insert right after canonical (or before </head> as fallback)
    link_tag = f'<link rel="alternate" type="text/markdown" href="{md_url}" />\n'
    canonical_re = re.compile(r'(<link rel="canonical"[^>]*>\s*\n)')
    if canonical_re.search(html):
        html = canonical_re.sub(r'\1' + link_tag, html, count=1)
    else:
        html = html.replace('</head>', link_tag + '</head>', 1)
    html_path.write_text(html, encoding='utf-8')
    return True


def main():
    results = []
    for html_file in sorted(POSTS_DIR.glob('*.html')):
        slug = html_file.stem
        html = html_file.read_text(encoding='utf-8')
        md_content = html_to_md(html, slug)
        if md_content is None:
            results.append(f"SKIP (no post-article): {html_file.name}")
            continue
        md_path = POSTS_DIR / f"{slug}.md"
        md_path.write_text(md_content, encoding='utf-8')
        injected = inject_md_link(html_file, slug)
        results.append(f"OK: {slug}.md ({len(md_content)} chars){' + link injected' if injected else ''}")
    for r in results:
        print(r)


if __name__ == '__main__':
    main()
