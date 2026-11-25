"""Build curator cards on cafe-hoppers pages from content/curators.json.
Usage: python3 tools/build_curators.py   (run from repo root)
Replaces everything between the SSOT markers in both pages."""
import json, re, html, sys, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB=os.path.join(ROOT,'production','v2.2')
START='<!-- SSOT:CURATORS START (generated from content/curators.json - do not edit by hand) -->'
END='<!-- SSOT:CURATORS END -->'
L={'en':{'try':'Try: ','dir':'Get Directions →','pending':'Quote coming soon.',
         'count':lambda n:f"{n} pick" if n==1 else f"{n} picks"},
   'zh':{'try':'試試：','dir':'查看地圖 →','pending':'評語即將更新。',
         'count':lambda n:f"{n} 個推薦"}}
e=lambda s: html.escape(s or '',quote=False)
a=lambda s: html.escape(s or '',quote=True)
js=lambda s: (s or '').replace('\\','\\\\').replace("'","\\'")
I=' '*20
def card(c,p,lang):
    t=L[lang]; cls='curator-cafe-item'+(' curator-cafe-item--has-photo' if p.get('photo') else '')
    o=[f'{I}    <div class="{cls}"',
       f"{I}      onclick=\"event.stopPropagation(); trackCafeClick('{js(p['id'])}','{js(c['id'])}')\">"]
    if p.get('photo'):
        o.append(f'{I}      <img src="{a(p["photo"])}" class="cafe-item-photo" alt="{a(p.get("photo_alt") or p["name"])}" loading="lazy">')
    o.append(f'{I}      <div class="cafe-item-header">')
    o.append(f'{I}        <span class="cafe-item-name">{e(p["name"])}</span>')
    loc=(p.get('location') or {}).get(lang)
    if loc: o.append(f'{I}        <span class="cafe-item-location-pill">{e(loc)}</span>')
    o.append(f'{I}      </div>')
    if p.get('quote'): o.append(f'{I}      <p class="cafe-item-quote">{e(p["quote"])}</p>')
    else: o.append(f'{I}      <p class="cafe-item-pending">{t["pending"]}</p>')
    tr=(p.get('try') or {}).get(lang)
    if tr: o.append(f'{I}      <p class="cafe-item-try">{e(tr)}</p>')
    if p.get('maps_url'):
        o.append(f'{I}      <a href="{a(p["maps_url"])}" target="_blank" class="cafe-item-directions"')
        o.append(f"{I}        onclick=\"event.stopPropagation(); trackDirectionsClick('{js(p.get('directions_id') or p['id'])}','{js(c['id'])}',event)\">")
        o.append(f'{I}        {t["dir"]}')
        o.append(f'{I}      </a>')
    o.append(f'{I}    </div>')
    return '\n'.join(o)
def curator(c,lang):
    t=L[lang]; live=[p for p in c['picks'] if not p.get('hidden')]
    o=[f'{I}<!-- {e(c["name"]).upper()} -->',
       f"{I}<div class=\"curator-profile\" onclick=\"trackCuratorClick('{js(c['id'])}')\">",
       f'{I}  <div class="curator-header-row">',
       f'{I}    <div class="curator-initials">{e(c["initial"])}</div>',
       f'{I}    <div class="curator-meta">',
       f'{I}      <h3 class="curator-name">{e(c["name"])}</h3>',
       f'{I}      <p class="curator-descriptor">{e(c["descriptor"][lang])}</p>',
       f'{I}      <div class="curator-footer-row">',
       f'{I}        <span class="curator-territory-pill">{e(c["territory"][lang])}</span>',
       f'{I}        <span class="curator-pick-count">{t["count"](len(live))}</span>',
       f'{I}      </div>', f'{I}    </div>', f'{I}  </div>',
       f'{I}  <div class="curator-cafes">']
    o+= [card(c,p,lang) for p in live]
    o+= [f'{I}  </div>', f'{I}</div>','']
    return '\n'.join(o)
def build(check=False):
    data=json.load(open(os.path.join(ROOT,'content','curators.json'),encoding='utf-8'))
    problems=[]
    for c in data['curators']:
        for k in ('descriptor','territory'):
            for lg in ('en','zh'):
                if not c[k].get(lg): problems.append(f"{c['id']}: missing {k}.{lg}")
    if problems: sys.exit('STOP - fix content first:\n'+'\n'.join(problems))
    for lang,fn in (('en','cafe-hoppers.html'),('zh','cafe-hoppers-zh.html')):
        path=os.path.join(WEB,fn); raw=open(path,'rb').read(); crlf=b'\r\n' in raw
        src=raw.decode('utf-8').replace('\r\n','\n')
        if START not in src: sys.exit(f'{fn}: SSOT markers missing')
        block='\n'.join(curator(c,lang) for c in data['curators'] if not c.get('hidden'))
        new=re.sub(re.escape(START)+r'.*?'+re.escape(END), lambda m: START+'\n'+block+I+END, src, flags=re.S)
        if crlf: new=new.replace('\n','\r\n')
        open(path,'w',encoding='utf-8',newline='').write(new)
        print(f'built {fn}: {sum(1 for c in data["curators"] if not c.get("hidden"))} curators')
if __name__=='__main__': build()
