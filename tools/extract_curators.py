import re, json, sys, html
from html.parser import HTMLParser

def norm(s): return re.sub(r'\s+',' ',html.unescape(s)).strip()

def parse(path):
    src=open(path,encoding='utf-8').read()
    a=src.index('<section class="section-curators">'); b=src.index('<section class="section-whatsapp-cta">')
    sec=src[a:b]
    blocks=re.split(r'<div class="curator-profile"',sec)[1:]
    out=[]
    for blk in blocks:
        g=lambda pat: (lambda m: norm(m.group(1)) if m else None)(re.search(pat,blk,re.S))
        c={'track_id':g(r"trackCuratorClick\('([^']*)'"),
           'name':g(r'class="curator-name">(.*?)</h3>'),
           'initial':g(r'class="curator-initials">(.*?)</div>'),
           'descriptor':g(r'class="curator-descriptor">(.*?)</p>'),
           'territory':g(r'class="curator-territory-pill">(.*?)</span>'),
           'pick_count_label':g(r'class="curator-pick-count">(.*?)</span>'),
           'picks':[]}
        for it in re.split(r'<div class="curator-cafe-item',blk)[1:]:
            h=lambda pat: (lambda m: norm(m.group(1)) if m else None)(re.search(pat,it,re.S))
            c['picks'].append({
              'track_cafe':h(r"trackCafeClick\('([^']*)'"),
              'track_directions':h(r"trackDirectionsClick\('([^']*)'"),
              'name':h(r'class="cafe-item-name">(.*?)</span>'),
              'location':h(r'class="cafe-item-location-pill">(.*?)</span>'),
              'quote':h(r'class="cafe-item-quote">(.*?)</p>'),
              'try':h(r'class="cafe-item-try">(.*?)</p>'),
              'pending':h(r'class="cafe-item-pending">(.*?)</p>'),
              'photo':h(r'<img\s+src="([^"]*)"'),
              'photo_alt':h(r'alt="([^"]*)"'),
              'maps_url':h(r'<a href="([^"]*)"'),
            })
        out.append(c)
    return out

en=parse(sys.argv[1]); zh=parse(sys.argv[2])
print('EN curators',len(en),'picks',sum(len(c['picks']) for c in en), file=sys.stderr)
print('ZH curators',len(zh),'picks',sum(len(c['picks']) for c in zh), file=sys.stderr)
issues=[]
merged=[]
zmap={c['track_id']:c for c in zh}
for c in en:
    z=zmap.get(c['track_id'])
    if not z: issues.append(f"ZH missing curator {c['track_id']}"); z={'picks':[]}
    zp={(p['track_cafe'] or p['track_directions']):p for p in z['picks']}
    cur={'id':c['track_id'],'name':c['name'],'initial':c['initial'],
         'descriptor':{'en':c['descriptor'],'zh':z.get('descriptor')},
         'territory':{'en':c['territory'],'zh':z.get('territory')},
         'picks':[]}
    for p in c['picks']:
        q=zp.get(p['track_cafe'],{}) or zp.get(p['track_directions'],{})
        if not q: issues.append(f"ZH missing pick {c['track_id']}/{p['track_cafe']}")
        else:
            for k in ('quote','maps_url','photo'):
                if (p[k] or '')!=(q.get(k) or ''): issues.append(f"EN/ZH differ [{k}] {c['track_id']}/{p['track_cafe']}: EN={p[k]!r} ZH={q.get(k)!r}")
        cur['picks'].append({'id':p['track_cafe'],'directions_id':p['track_directions'],
          'name':p['name'],'location':{'en':p['location'],'zh':q.get('location')},
          'quote':p['quote'],'try':{'en':p['try'],'zh':q.get('try')},
          'status':'pending_quote' if p['pending'] else 'live',
          'photo':p['photo'],'photo_alt':p['photo_alt'],'maps_url':p['maps_url']})
    if c['pick_count_label'] and not c['pick_count_label'].startswith(str(len(c['picks']))):
        issues.append(f"Pick count label mismatch {c['track_id']}: label '{c['pick_count_label']}' vs {len(c['picks'])} cards")
    merged.append(cur)
for z in zh:
    if z['track_id'] not in {c['track_id'] for c in en}: issues.append(f"EN missing curator {z['track_id']}")
json.dump({'_about':'Single source of truth for curator cards on cafe-hoppers.html and cafe-hoppers-zh.html. Edit here; pages are generated from this file.','curators':merged},open(sys.argv[3],'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('\n'.join(issues) or 'no parity issues', file=sys.stderr)
