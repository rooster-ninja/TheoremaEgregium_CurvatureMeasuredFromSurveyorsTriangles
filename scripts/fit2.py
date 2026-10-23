import json,math,re,html,numpy as np,collections
RAD=math.pi/180/3600; K0=1/6371000.0**2
rows=json.load(open('rows_s.json'))
# re-read per-vertex observed angles in vertex order (for 1-2 side area formula)
exec(open('analyse.py').read().split("rows=[]")[0])   # reuse dms/angles helpers
polys={(fi,p['n']):p for fi,o in enumerate(d) for p in o['polys']}
def angles_by_vertex(r):
    p=polys[(r['fi'],r['name'])]; t=html.unescape(p['d'])
    names=[x.strip() for x in r['name'].split(' - ')]
    A,_=angles(r['fi'],t)
    if r['qc'].startswith('corrected'):
        CORR={'Mount Nebo - Wheeler Peak - Ibepah':('23 07 63.497','46 42 68.971','110 09 30.489'),'Cherry Ridge - Twin Creek - Round Top':('28 10 13.41','106 18 47.42','45 30 57.72'),'Gunstock - Mount Pleasant - Mount Independence':('34 19 40.20','91 54 04.38','53 46 22.53')}
        A=[dms(x) for x in CORR[r['name']]]
    if not A: return None
    m=re.search(r'angles printed: (.*?)<br>',t); raw=json.loads(m.group(1))
    if isinstance(raw,dict):
        keys=list(raw['reduced_to_centre_and_horizon'].keys()) if r['fi']==4 else [k for k in raw if not k.startswith('_')]
        if sorted(keys)!=sorted(names): return None
        return dict(zip(keys,A))
    return dict(zip(names,A))
stats=collections.defaultdict(list)
for r in rows:
    r['A_side']=None; r['tier']=None; r['ratio_side']=None
    if r['E'] is None: continue
    names=[x.strip() for x in r['name'].split(' - ')]
    S=r['sides']; ns=len(S)
    if ns==3:
        a,b,c=S.values(); s=(a+b+c)/2; v=s*(s-a)*(s-b)*(s-c)
        r['A_side']=math.sqrt(v) if v>0 else None
        # law-of-sines check of vertex order
        av=angles_by_vertex(r)
        if av and len(av)==3:
            chk=[]
            for n in names:
                opp='||'.join(sorted([x for x in names if x!=n]))
                if opp in S: chk.append(S[opp]/math.sin(av[n]/3600*math.pi/180))
            if len(chk)==3: stats[r['survey']].append(max(chk)/min(chk)-1)
    elif ns in (1,2):
        av=angles_by_vertex(r)
        if av and len(av)==3:
            ests=[]
            for k,sv in S.items():
                pq=k.split('||'); opp=[n for n in names if n not in pq]
                if len(opp)!=1: continue
                aP,aQ,aR=[av[x]/3600*math.pi/180 for x in (pq[0],pq[1],opp[0])]
                ests.append(sv*sv*math.sin(aP)*math.sin(aQ)/(2*math.sin(aR)))
            if ests: r['A_side']=float(np.mean(ests))
    if r['A_side']:
        r['ratio_side']=r['A_side']/r['area']
        r['tier']=('A' if ns==3 else 'B') if abs(r['ratio_side']-1)<=0.02 else 'C'
    else: r['tier']='C'
print('law-of-sines spread (3-side triangles), median per survey:')
for k,v in stats.items(): print(f'  {k:26s} {np.median(v):.2e}  n={len(v)}')
print('side-area / coord-area by survey: median, n within 2%, n flagged')
for sv in sorted(set(r['survey'] for r in rows)):
    R=[r for r in rows if r['survey']==sv and r['ratio_side']]
    if R: print(f'  {sv:26s} {np.median([r["ratio_side"] for r in R]):.5f}  ok={sum(abs(r["ratio_side"]-1)<=0.02 for r in R)} flagged={sum(abs(r["ratio_side"]-1)>0.02 for r in R)}')
json.dump(rows,open('rows_t.json','w'))
print(collections.Counter((r['survey'],r['tier']) for r in rows if r['E'] is not None))
