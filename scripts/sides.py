import json,html,re,math
from pyproj import Geod
g=Geod(ellps='WGS84')
FT=0.3048; TOISE=1.949036
d=json.load(open('data.json')); rows=json.load(open('rows.json'))
def val(fi,s):
    s0=s; s=s.replace(',', '.') if fi in (2,3,4) else s
    if fi==11:
        m=re.search(r'/\s*([\d.]+)\s*m',s); return float(m.group(1)) if m else None
    if fi==10:
        m=re.match(r'\s*(\d\.\d+)\s*$',s); return 10**float(m.group(1)) if m else None
    if fi==3:
        m=re.search(r'log s = (\d\.\d+)',s); return 10**float(m.group(1)) if m else None
    m=re.search(r'log\s+([\d.]+)',s)
    if m:
        v=10**float(m.group(1))
        if 'toise' in s: return v*TOISE
        if 'feet' in s or 'ft' in s: return v*FT
        return None
    m=re.search(r'([\d]+(?:\.\d+)?)(\s+(\d)/(\d))?\s*(feet|ft|toises)',s)
    if m:
        v=float(m.group(1))+(int(m.group(3))/int(m.group(4)) if m.group(2) else 0)
        return v*(TOISE if m.group(5)=='toises' else FT)
    return None
def match_pair(key,names):
    hits=[n for n in names if n in key]
    if len(hits)==2: return tuple(hits)
    # longest-match fallback
    for i,a in enumerate(names):
        for b in names[i+1:]:
            if key in (f"{a}-{b}",f"{b}-{a}",f"{a} - {b}",f"{b} - {a}",f"{a} to {b}",f"{b} to {a}"): return (a,b)
    return None
out=0; cnt={}
polys={}
for fi,o in enumerate(d):
    for p in o['polys']: polys[(fi,p['n'])]=p
for r in rows:
    r['sides']={}; p=polys[(r['fi'],r['name'])]; t=html.unescape(p['d'])
    names=[x.strip() for x in r['name'].split(' - ')]
    if len(names)!=3: continue
    m=re.search(r'sides printed: (.*?)<br>',t)
    if not m: continue
    try: S=json.loads(m.group(1))
    except Exception: continue
    items=[]
    if isinstance(S,dict):
        for k,v in S.items(): items.append((k,v))
    else:
        for s in S:
            if r['fi']==3:
                mm=re.search(r'side opposite (.*)$',s); opp=mm.group(1).strip()
                others=[n for n in names if n!=opp]; items.append(('|'.join(others),s))
            else:
                k,_,v=s.partition(':'); items.append((k,v))
    for k,v in items:
        if r['fi']==3: pair=tuple(k.split('|')) if len(k.split('|'))==2 else None
        elif r['fi']==5: continue
        else: pair=match_pair(k.replace(' (base mesuree)',''),names)
        x=val(r['fi'],v)
        if pair and x: r['sides']['||'.join(sorted(pair))]=x
json.dump(rows,open('rows_s.json','w'))
import collections
c=collections.Counter((r['survey'],len(r['sides'])) for r in rows)
for k in sorted(c): print(k,c[k])
