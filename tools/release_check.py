"""NodeBase release check. Run from anywhere:  python3 tools/release_check.py
Checks the web root (production/v2.2) before a branch is merged to main.
FAIL = do not merge. WARN = known issue, merge allowed if JT accepts it."""
import os, re, json, sys, subprocess, tempfile, shutil, importlib.util
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB=os.path.join(ROOT,'production','v2.2')
GA4='G-WK983SLBZX'
PAGES=['index','cafe-hoppers','cafe-owners','contact','privacy']
EVENTS={'cafe-hoppers':['cafe_card_click','get_directions_click','curator_profile_click',
        'discovery_directions_click','whatsapp_join_click','scroll_depth_90','map_loaded']}
SITE_EXT={'.html','.css','.js','.png','.jpg','.jpeg','.webp','.svg','.ico','.gif','.avif'}
ALLOWED_OTHER={'robots.txt','sitemap.xml','_headers','_redirects','favicon.ico'}
LEAKS=[r'\bCursor\b',r'\bClaude\b',r'cryptocafe',r'investor',r'@gmail\.com',r'C:\\\\',r'Users\\\\',r'OpenClaw',r'\bPWA\b',r'Phase [0-9]']
DRIFT=[r'\bdirectory\b',r'\bloyalty\b',r'\brewards?\b',r'\btokens?\b',r'\bcrypto\b',r'\bCRM\b',r'\bratings?\b',r'\breviews?\b']
res=[]
def add(level,check,msg): res.append((level,check,msg))
def read(p): return open(p,encoding='utf-8').read()

# 1. Only site files are served
for dp,_,fs in os.walk(WEB):
    for f in fs:
        rel=os.path.relpath(os.path.join(dp,f),WEB)
        if f in ALLOWED_OTHER: continue
        if os.path.splitext(f)[1].lower() not in SITE_EXT: add('FAIL','served-files',f'non-site file is public: /{rel}')

# 2. Pages exist in EN and ZH, GA4 loads once
for p in PAGES:
    for suf in ('','-zh'):
        fp=os.path.join(WEB,p+suf+'.html')
        if not os.path.exists(fp): add('FAIL','parity',f'missing {p+suf}.html'); continue
        s=read(fp)
        n=s.count('googletagmanager.com/gtag/js?id='+GA4); c=len(re.findall(r"gtag\(\s*'config'\s*,\s*'"+GA4,s))
        if n!=1 or c!=1: add('FAIL','ga4',f'{p+suf}: gtag loader x{n}, config x{c} (want 1/1)')
        for ev in EVENTS.get(p,[]):
            if f"'{ev}'" not in s: add('FAIL','ga4',f'{p+suf}: event {ev} missing')
        # SEO basics (baseline gaps reported as WARN)
        for tag,pat in (('meta description',r'name="description"'),('canonical',r'rel="canonical"'),('og:title',r'property="og:title"')):
            if not re.search(pat,s): add('WARN','seo',f'{p+suf}: no {tag}')
        if len(re.findall(r'<h1\b',s))!=1: add('WARN','seo',f'{p+suf}: h1 count {len(re.findall(r"<h1",s))}')
        if 'noindex' in s: add('FAIL','seo',f'{p+suf}: noindex present')
        lang=re.search(r'<html[^>]*lang="([^"]+)"',s)
        if suf=='-zh' and (not lang or not lang.group(1).lower().startswith('zh')): add('WARN','parity',f'{p+suf}: html lang is {lang.group(1) if lang else None}, expected zh-HK')
        text=re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>',' ',s,flags=re.S)
        for pat in LEAKS:
            if re.search(pat,s,re.I): add('FAIL','leak',f'{p+suf}: matches {pat}')
        for pat in DRIFT:
            m=re.search(pat,text,re.I)
            if m: add('WARN','positioning',f'{p+suf}: says "{m.group(0)}" - check against locked positioning')

# 3. Curator SSOT in sync with pages and tracked
data=json.load(open(os.path.join(ROOT,'content','curators.json'),encoding='utf-8'))
spec=importlib.util.spec_from_file_location('b',os.path.join(ROOT,'tools','build_curators.py')); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
tmp=tempfile.mkdtemp()
try:
    os.makedirs(os.path.join(tmp,'production','v2.2')); os.makedirs(os.path.join(tmp,'content')); os.makedirs(os.path.join(tmp,'tools'))
    for f in ('cafe-hoppers.html','cafe-hoppers-zh.html'): shutil.copy(os.path.join(WEB,f),os.path.join(tmp,'production','v2.2',f))
    shutil.copy(os.path.join(ROOT,'content','curators.json'),os.path.join(tmp,'content'))
    b.ROOT=tmp; b.WEB=os.path.join(tmp,'production','v2.2')
    import io,contextlib
    with contextlib.redirect_stdout(io.StringIO()): b.build()
    for f in ('cafe-hoppers.html','cafe-hoppers-zh.html'):
        if open(os.path.join(tmp,'production','v2.2',f),'rb').read()!=open(os.path.join(WEB,f),'rb').read():
            add('FAIL','ssot',f'{f} was hand-edited or not rebuilt: run tools/build_curators.py')
finally: shutil.rmtree(tmp)
for c in data['curators']:
    for p in c['picks']:
        if not p.get('maps_url'): add('WARN','content',f"{c['id']}/{p['name']}: no map link")
        if not p.get('quote'): add('WARN','content',f"{c['id']}/{p['name']}: quote pending")
        ph=p.get('photo')
        if ph:
            fp=os.path.join(WEB,ph)
            if not os.path.exists(fp): add('FAIL','images',f'missing image {ph}')
            elif os.path.getsize(fp)>500_000: add('WARN','images',f'{ph} is {os.path.getsize(fp)//1024} KB (target < 300 KB)')

# 4. robots.txt
rb=os.path.join(WEB,'robots.txt')
if os.path.exists(rb):
    for line in read(rb).splitlines():
        if line.lower().startswith('disallow:') and line.split(':',1)[1].strip() not in ('','/'):
            add('WARN','robots',f'robots.txt advertises a hidden path: {line.strip()}')
    if 'sitemap' not in read(rb).lower(): add('WARN','seo','robots.txt has no Sitemap line')
if not os.path.exists(os.path.join(WEB,'sitemap.xml')): add('WARN','seo','no sitemap.xml')
if not os.path.exists(os.path.join(WEB,'_headers')): add('WARN','security','no _headers file (security headers)')

fails=[r for r in res if r[0]=='FAIL']; warns=[r for r in res if r[0]=='WARN']
for lvl in ('FAIL','WARN'):
    rows=[r for r in res if r[0]==lvl]
    if rows:
        print(f'\n{lvl} ({len(rows)})')
        for _,c,m in rows: print(f'  [{c}] {m}')
print(f"\n{'NO-GO' if fails else 'GO'}  -  {len(fails)} fail, {len(warns)} warn")
sys.exit(1 if fails else 0)
