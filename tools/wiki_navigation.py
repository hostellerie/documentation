#!/usr/bin/env python3
"""Build an offline searchable index after running wiki_preview.py --all.

This script reads only the metadata CSV and existing HTML filenames.
It replaces preview/index.html, not any source article; no network/publishing.
"""
import argparse
import csv
import html
from pathlib import Path
from urllib.parse import quote
from collections import Counter

CSS = """body{font:16px/1.55 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1.2rem;color:#1b2938}a{color:#155b98}.warning{border-left:4px solid #bd7b00;background:#fff2d6;padding:1rem}input{width:100%;padding:.75rem;font:inherit;box-sizing:border-box;border:1px solid #9baebc;border-radius:5px}nav{margin:1.3rem 0}.tabs{display:flex;flex-wrap:wrap;gap:.6rem}.tabs button{padding:.5rem .8rem;cursor:pointer;border:1px solid #9aafc0;border-radius:5px;background:white;color:#143b5c}.tabs button[aria-pressed=true]{background:#143b5c;color:white}.items{list-style:none;margin:1rem 0;padding:0}.items li{padding:.5rem .2rem;border-bottom:1px solid #e4e9ee}.meta{font-size:.85rem;color:#52647a;margin-left:.6rem}.count{color:#52647a}"""
JS = """const query=document.querySelector('#q'),buttons=[...document.querySelectorAll('[data-filter]')],items=[...document.querySelectorAll('li[data-title]')],result=document.querySelector('#result');let filter='all';function update(){const q=query.value.toLocaleLowerCase().trim();let n=0;for(const li of items){const ok=(filter==='all'||li.dataset.group===filter)&&(!q||li.dataset.title.includes(q));li.hidden=!ok;if(ok)n++}result.textContent=n+' articles affichés';for(const b of buttons)b.setAttribute('aria-pressed',String(b.dataset.filter===filter))}query.addEventListener('input',update);for(const b of buttons)b.addEventListener('click',()=>{filter=b.dataset.filter;update()});update();"""

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--catalog',default='wiki-2024-review.csv',type=Path)
    ap.add_argument('--out',default='wiki-preview-local',type=Path)
    args=ap.parse_args()
    if not args.out.is_dir():
        ap.error('Preview directory does not exist; run wiki_preview.py --all')
    with args.catalog.open(encoding='utf-8-sig',newline='') as file:
        rows=list(csv.DictReader(file))
    if len(rows)!=360:
        ap.error('Expected 360 catalog entries')
    groups=Counter()
    found=[]
    missing=[]
    for row in rows:
        if row['redirection']!='0':continue
        title=row['titre_wiki']
        filename=quote(title,safe='')+'.html'
        if not (args.out/filename).is_file():
            missing.append(title)
            continue
        group=row.get('rubrique_initiale') or row.get('rubrique_proposee') or 'À classer'
        groups[group]+=1
        found.append((title,filename,group))
    if missing:
        ap.error(f'{len(missing)} pages missing. First run extraction --all; first examples: {missing[:5]}')
    found.sort(key=lambda x:x[0].casefold())
    group_ids={g:str(i) for i,g in enumerate(sorted(groups))}
    controls='<button data-filter="all" aria-pressed="true">Tous ('+str(len(found))+')</button> '+' '.join('<button data-filter="'+group_ids[g]+'" aria-pressed="false">'+html.escape(g)+' ('+str(groups[g])+')</button>' for g in sorted(groups))
    listing='\n'.join('<li data-title="'+html.escape(t.replace('_',' ').casefold(),quote=True)+'" data-group="'+group_ids[g]+'"><a href="'+html.escape(f,quote=True)+'">'+html.escape(t.replace('_',' '))+'</a><span class="meta">'+html.escape(g)+'</span></li>' for t,f,g in found)
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Geeklog Wiki 2024 — Offline Archive</title><style>'''+CSS+'''</style></head><body><h1>Geeklog Wiki — Historical archive (2024)</h1><p class="warning"><strong>Local review copy only.</strong> Historical documentation, not validated for current Geeklog versions. MediaWiki markup is displayed as raw text on article pages. Do not publish without privacy, license and technical review.</p><p>Search and browse recovered articles below. Categories are tentative and based on titles, not content.</p><label for="q"><strong>Search titles</strong></label><input id="q" type="search" placeholder="Search 2024 Wiki titles" autocomplete="off"><nav class="tabs" aria-label="Categories">'''+controls+'''</nav><p id="result" class="count"></p><ul class="items">'''+listing+'''</ul><script>'''+JS+'''</script></body></html>'''
    (args.out/'index.html').write_text(page,encoding='utf-8')
    print(f'Searchable local index: {(args.out/"index.html").resolve()}')
    print(f'Listed article pages: {len(found)}; redirects excluded: {sum(r["redirection"]=="1" for r in rows)}')
    print('No archive data uploaded or publicly deployed.')

if __name__=='__main__':
    main()
