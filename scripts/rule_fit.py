import json,math,numpy as np,collections
RAD=math.pi/180/3600; K0=1/6371000.0**2
TIERW={'A':1.0,'B':0.5,'C':0.25}
rows=[r for r in json.load(open('rows_t.json')) if r['E'] is not None]
def area(r,src): return r['A_side'] if (src=='sides' and r['A_side'] and r['tier']!='C') else r['area']
def sigmas(src):
    sig={}
    for sv in set(r['survey'] for r in rows):
        S=[r for r in rows if r['survey']==sv]; A=np.array([area(r,src) for r in S]); E=np.array([r['E'] for r in S])*RAD
        k=(A@E)/(A@A); res=E-k*A; sig[sv]=1.4826*np.median(np.abs(res-np.median(res)))
    return sig
def run(cut=2,tw=TIERW,src='sides',verbose=False):
    sig=sigmas(src)
    S=[r for r in rows if tw.get(r['tier'],0)>0 and K0*area(r,src)/sig[r['survey']]>=cut]
    A=np.array([area(r,src) for r in S]); E=np.array([r['E'] for r in S])*RAD
    s=np.array([sig[r['survey']] for r in S]); w=np.array([tw[r['tier']] for r in S])/s**2
    Kell=np.array([r['Kref'] for r in S])
    K=(w*A)@E/((w*A)@A)
    var=np.sum((w*A)**2*s**2)/((w*A)@A)**2
    res=E-K*A; chi=np.sum((res/s)**2); dof=len(E)-1; inf=max(1,math.sqrt(chi/dof))
    sK=math.sqrt(var)*inf
    Kref=(w*A)@(Kell*A)/((w*A)@A)       # same-weighted ellipsoid curvature of this sample
    q=K/Kref; sq=sK/Kref
    out=dict(cut=cut,tw=tw,src=src,n=len(S),K=K,sK=sK,Kref=Kref,q=q,sq=sq,chi_dof=chi/dof,inf=inf,R=1/math.sqrt(K)/1e3,
             Rlo=1/math.sqrt(K+sK)/1e3,Rhi=1/math.sqrt(K-sK)/1e3,
             surveys=collections.Counter(r['survey'] for r in S),
             wshare={sv:float(sum(wi*a*a for wi,a,r in zip(w,A,S) if r['survey']==sv)/((w*A)@A)) for sv in set(r['survey'] for r in S)},
             tiers=collections.Counter(r['tier'] for r in S),sig={k:v/RAD for k,v in sig.items()})
    return out,S
def show(o,label):
    print(f"{label:34s} n={o['n']:4d}  K={o['K']*1e14:.4f}±{o['sK']*1e14:.4f}e-14  q={o['q']:.4f}±{o['sq']:.4f}  z={(o['q']-1)/o['sq']:+.2f}  R={o['R']:.0f} ({o['Rlo']:.0f}–{o['Rhi']:.0f}) km  χ²/dof={o['chi_dof']:.2f}")
H,HS=run(); show(H,'HEADLINE (rule as declared)')
print('  noise σ per survey (″):',{k:round(v,2) for k,v in sorted(H['sig'].items())})
print('  kept:',dict(H['surveys'])); print('  tiers:',dict(H['tiers']))
print('  weight share:',{k:round(v,3) for k,v in sorted(H['wshare'].items(),key=lambda x:-x[1])})
print('--- sensitivity')
sens=[]
for c in (0,1,2,3):
    o,_=run(cut=c); show(o,f'SNR cut {c}'); sens.append(('SNR ≥ %d'%c,o))
o,_=run(tw={'A':1,'B':1,'C':1}); show(o,'equal tier weights'); sens.append(('Equal tier weights',o))
o,_=run(tw={'A':1}); show(o,'tier A only'); sens.append(('Tier A only',o))
o,_=run(src='coords'); show(o,'area from coordinates'); sens.append(('Area from coordinates',o))
# per-survey within headline
print('--- per survey, headline rule')
per=[]
for sv in sorted(set(r['survey'] for r in HS)):
    S=[r for r in HS if r['survey']==sv]
    A=np.array([area(r,'sides') for r in S]); E=np.array([r['E'] for r in S])*RAD; Kell=np.array([r['Kref'] for r in S])
    s=H['sig'][sv]*RAD; K=(A@E)/(A@A); sK=s/math.sqrt(A@A)
    res=E-K*A; inf=max(1,math.sqrt(np.sum((res/s)**2)/max(1,len(E)-1))); sK*=inf
    q=K/((A@(Kell*A))/(A@A)); sq=sK/((A@(Kell*A))/(A@A))
    snr=np.median(K0*A/s)
    print(f"  {sv:26s} n={len(S):4d} medSNR={snr:5.1f} q={q:.3f}±{sq:.3f} z={(q-1)/sq:+.2f} tiers={dict(collections.Counter(r['tier'] for r in S))}")
    per.append(dict(survey=sv,n=len(S),snr=float(snr),q=q,sq=sq,K=K,sK=sK,tiers=dict(collections.Counter(r['tier'] for r in S)),sigma=H['sig'][sv]))
def clean(o): o=dict(o); o['surveys']=dict(o['surveys']); o['tiers']=dict(o['tiers']); return o
json.dump(dict(head=clean(H),sens=[(l,clean(o)) for l,o in sens],per=per),open('rule_results.json','w'),default=float)
json.dump([dict(survey=r['survey'],name=r['name'],tier=r['tier'],A=area(r,'sides'),E=r['E'],Kref=r['Kref'],lat=r['lat'],lon=r['lon'],coords=r['coords'],sig=H['sig'][r['survey']]) for r in HS],open('headline_rows.json','w'))
