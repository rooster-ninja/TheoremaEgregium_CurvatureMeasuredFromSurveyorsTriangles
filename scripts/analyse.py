import json,html,re,math,numpy as np
from pyproj import Geod
g=Geod(ellps='WGS84'); a=6378137.0; f=1/298.257223563; e2=f*(2-f)
d=json.load(open('data.json'))
SHORT={0:'Anglo-French 1787',1:'Maclear, Cape 1837–48',2:'England OS 1787–96',3:'Europe 52°N (Helmert)',4:'Cassini–Lacaille 1739',5:'Brousseaud 45°43′',6:'India GTS meridional',7:'India Madras–Mangalore',8:'Transvaal–Rhodesia',9:'Struve arc',10:'US 39th parallel',11:'US Eastern Oblique'}
def dms(s):
    s=s.replace(',', '.').replace('°',' ').replace("'",' ').replace('"',' ').strip()
    half=0
    if '1/2' in s: half=0.5; s=s.replace('1/2','')
    if '..' in s: return None
    p=[x for x in s.split() if x]
    try: v=[float(x.rstrip('.')) if x.rstrip('.') else 0 for x in p]
    except: return None
    while len(v)<3: v.append(0)
    return v[0]*3600+v[1]*60+v[2]+half
def angles(fi,t):
    m=re.search(r'angles printed: (.*?)<br>',t+'<br>'); 
    try: A=json.loads(m.group(1))
    except: return None,None
    if fi==3:  # Helmert: use OBSERVED seconds (final are adjusted)
        out=[]
        for s in A:
            mm=re.match(r"(\d+)° (\d+)' [\d,]+\" \(final; observed ([\d,]+)\"",s)
            if not mm: return None,None
            out.append(int(mm.group(1))*3600+int(mm.group(2))*60+float(mm.group(3).replace(',','.')))
        # observed seconds may wrap; fix by comparing to final
        return out,'observed'
    if fi==2: A=[v['observed'] for v in A.values()]; kind='observed'
    elif fi==4: A=list(A['reduced_to_centre_and_horizon'].values()); kind='reduced to centre'
    elif fi==5:
        vs=[v['spherical'] for k,v in A.items() if not k.startswith('_')]
        out=[]
        for s in vs:
            x=float(s.split()[0].replace(',',''))  # e.g. 88.58977 grades
            out.append(x*0.9*3600)
        return out,'spherical (grades)'
    else: kind='as printed'
    if any(x is None for x in A): return None,None
    out=[dms(x) for x in A]
    if any(x is None for x in out): return None,None
    return out,kind
def excess_printed(t):
    m=re.search(r'spherical excess printed: (.*?)<br>',t+'<br>')
    if not m: return None
    s=m.group(1)
    nums=re.findall(r'(\d+[.,]\d+)',s)
    if not nums: return None
    v=[float(x.replace(',','.')) for x in nums]
    return sum(v) if s.strip().startswith('[') else v[0]  # US oblique gives per-angle thirds
rows=[]
for fi,o in enumerate(d):
    for p in o['polys']:
        t=html.unescape(p['d'])
        c=p['c'][:3]
        lons=[x[0] for x in c]; lats=[x[1] for x in c]
        area,_=g.polygon_area_perimeter(lons,lats); area=abs(area)
        A,kind=angles(fi,t)
        # Source-verified corrections: degree misprints in the printed tables, fixed from the printed sides (law of cosines)
        CORR={(10,'Mount Nebo - Wheeler Peak - Ibepah'):('23 07 63.497','46 42 68.971','110 09 30.489'),   # Schott 1900 p.591 no.33: Ibepah printed 10 deg
              (10,'Cherry Ridge - Twin Creek - Round Top'):('28 10 13.41','106 18 47.42','45 30 57.72'),     # Schott 1900 p.414 no.25: Cherry Ridge printed 20 deg
              (11,'Gunstock - Mount Pleasant - Mount Independence'):('34 19 40.20','91 54 04.38','53 46 22.53')}  # Schott 1902 p.131 no.16: Mount Pleasant printed 19 deg
        corrected=(fi,p['n']) in CORR
        if corrected: A=[dms(x) for x in CORR[(fi,p['n'])]]
        E=None
        qc='ok' if not corrected else 'corrected: printed degree misprint, fixed from printed sides'
        if fi==5: A=None; qc='excluded: spherical angles are computed (mean+ε/3), not observed'
        if A:
            E=sum(A)-180*3600
            ms=re.search(r'angle sum printed: "([^"]*)"',t)
            if ms and fi in (0,1,6,10) and not corrected:
                tok=ms.group(1).split()
                try:
                    ps=float(tok[-1]) if fi==10 else dms(' '.join(tok[:3]))-180*3600
                    if fi==10: ps = min((ps, ps-60), key=lambda v: abs(v-E))   # printed seconds only: 180 00 ss or 179 59 ss, whichever the angles imply
                    if abs(ps-E)>0.06: qc='dropped: angles disagree with printed sum (%.2f vs %.2f)'%(E,ps); E=None
                except Exception: pass
            if E is not None:
                _A=abs(g.polygon_area_perimeter([x[0] for x in c],[x[1] for x in c])[0]); _E0=_A/6371000.0**2*206264.806
                if abs(E-_E0)>20: qc='dropped: blunder, |excess - A/R0^2| > 20" (%.1f vs %.1f)'%(E,_E0); E=None
            if fi==3 and E is not None and abs(E)>30:   # seconds wrap guard
                E=None
        lat=np.radians(np.mean(lats)); s2=math.sin(lat)**2
        M=a*(1-e2)/(1-e2*s2)**1.5; N=a/math.sqrt(1-e2*s2)
        Kref=1/(M*N)
        rows.append(dict(fi=fi,survey=SHORT[fi],name=p['n'],lat=float(np.degrees(lat)),lon=float(np.mean(lons)),area=area,E=E,Ep=excess_printed(t),Kref=Kref,kind=kind,qc=qc,coords=c))
json.dump(rows,open('rows.json','w'))
R=[r for r in rows if r['E'] is not None and r['area']>0]
print('triangles total',len(rows),' with observed angle sums',len(R))
RAD=math.pi/180/3600
def fit(sub):
    x=np.array([r['area'] for r in sub]); y=np.array([r['E'] for r in sub])*RAD
    # model y = q*Kref*A + closure noise; fit q
    k=np.array([r['Kref'] for r in sub]); X=k*x
    q=(X@y)/(X@X); res=y-q*X; s=math.sqrt(res@res/(len(y)-1)); sq=s/math.sqrt(X@X)
    return q,sq,s/RAD,len(y)
print(f"{'survey':28s} n   q=K_obs/K_ell  ±σ    z(q=0)  z(q=1)  σ_closure\"  R_obs km")
summary=[]
for fi in sorted(set(r['fi'] for r in R)):
    sub=[r for r in R if r['fi']==fi]
    if len(sub)<2: continue
    q,sq,sc,n=fit(sub); kr=np.mean([r['Kref'] for r in sub])
    Robs=1/math.sqrt(q*kr)/1000 if q>0 else float('nan')
    print(f"{SHORT[fi]:28s}{n:4d}  {q:7.3f} ±{sq:6.3f}  {q/sq:6.1f}  {(q-1)/sq:6.2f}   {sc:6.2f}   {Robs:8.0f}")
    summary.append(dict(fi=fi,survey=SHORT[fi],n=n,q=q,sq=sq,sclos=sc,Kref=kr,lat=float(np.mean([r['lat'] for r in sub])),kind=sub[0]['kind']))
# global weighted (inverse variance per survey)
num=den=0
for s in summary: w=1/s['sq']**2; num+=w*s['q']; den+=w
qg=num/den; sqg=1/math.sqrt(den)
chi=sum(((s['q']-qg)/s['sq'])**2 for s in summary)
print('GLOBAL q=%.4f ± %.4f  chi2=%.1f dof=%d'%(qg,sqg,chi,len(summary)-1))
Kmean=np.mean([r['Kref'] for r in R])
print('mean K_ell %.4e /m^2 ; K_obs = %.4e ± %.1e'%(Kmean,qg*Kmean,sqg*Kmean))
print('R_obs = %.0f km  (+%.0f / -%.0f)'%(1/math.sqrt(qg*Kmean)/1e3, 1/math.sqrt((qg-sqg)*Kmean)/1e3-1/math.sqrt(qg*Kmean)/1e3, 1/math.sqrt(qg*Kmean)/1e3-1/math.sqrt((qg+sqg)*Kmean)/1e3))
# printed excess vs computed from area*Kref
P=[r for r in rows if r['Ep'] is not None and r['area']>0]
rat=np.array([r['Ep']*RAD/(r['area']*r['Kref']) for r in P])
print('printed eps / (A*K_ell): n=%d median %.3f  IQR %.3f-%.3f'%(len(P),np.median(rat),*np.percentile(rat,[25,75])))
json.dump(dict(summary=summary,qg=qg,sqg=sqg,chi=chi,Kmean=Kmean,nR=len(R),ntot=len(rows)),open('summary.json','w'))
