#!/usr/bin/env python3
"""MD -> Confluence storage. Robust: python-markdown parses MD; thin post-proc adds storage macros.
Requires: pip install --user markdown  (pc host)."""
import re, sys, html
import markdown

def panel_kind(text):
    if any(k in text for k in ['⚠','주의','금지','선결','필수','블로커']): return 'warning'
    if any(k in text for k in ['즉 ','정리','한 줄','요약','종합']): return 'note'
    if any(k in text for k in ['참고','참조','tip']): return 'tip'
    return 'info'

def convert(md):
    md = re.sub(r'^## 목차\n.*?(?=\n## )', '', md, flags=re.S|re.M)   # drop manual TOC
    md = re.sub(r'\A# .*\n', '', md)                                    # drop h1 (page title)
    h = markdown.markdown(md, extensions=['tables','fenced_code','sane_lists'])
    # code block -> code macro (unescape entities for CDATA)
    def code_repl(m):
        lang=(m.group(1) or 'text').strip()
        body=html.unescape(m.group(2))
        return (f'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">{lang}'
                f'</ac:parameter><ac:plain-text-body><![CDATA[{body}]]></ac:plain-text-body></ac:structured-macro>')
    h=re.sub(r'<pre><code(?: class="language-([^"]*)")?>(.*?)</code></pre>', code_repl, h, flags=re.S)
    # blockquote -> panel (preserve nested HTML inside)
    def bq_repl(m):
        inner=m.group(1).strip()
        text=re.sub(r'<[^>]+>','',inner)
        return (f'<ac:structured-macro ac:name="{panel_kind(text)}"><ac:rich-text-body>'
                f'{inner}</ac:rich-text-body></ac:structured-macro>')
    h=re.sub(r'<blockquote>\s*(.*?)\s*</blockquote>', bq_repl, h, flags=re.S)
    # img -> placeholder (attach later, then PUT with <ac:image>)
    h=re.sub(r'<img[^>]*?src="[^"]*?([^/"]+\.png)"[^>]*?/?>', lambda m:f'<!--IMG:{m.group(1)}-->', h)
    # TOC macro at top
    toc='<ac:structured-macro ac:name="toc"><ac:parameter ac:name="maxLevel">3</ac:parameter><ac:parameter ac:name="minLevel">2</ac:parameter></ac:structured-macro>'
    return toc+'\n'+h

if __name__=='__main__':
    sys.stdout.write(convert(open(sys.argv[1],encoding='utf-8').read()))
