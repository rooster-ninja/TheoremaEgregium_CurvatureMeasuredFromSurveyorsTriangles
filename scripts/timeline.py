import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'
# (label, field start, field end, published, core?, confirmed-dates?)
S=[('US Eastern Oblique Arc (Schott 1902)',1833,1898,1902,True,True),
   ('US 39th parallel (Schott 1900)',1871,1898,1900,True,True),
   ('Maclear, Cape (pub. 1866)',1837,1848,1866,True,True),
   ('Helmert 52° N (compiled 1893)',None,None,1893,False,True),
   ('Transvaal–Rhodesia (Morris & Gill 1908)',None,None,1908,False,False),
   ('Lambton, Great Arc (pub. 1816–20)',1800,1815,1816,False,True),
   ('Lambton, Madras–Mangalore',1802,1806,1811,False,True),
   ('England OS arcs',1787,1796,1801,False,True),
   ('Anglo-French (Roy 1790)',1784,1788,1790,False,True),
   ('Cassini–Lacaille, 43° 32′ N',1739,1740,1744,False,True)]
# bases: (survey index, year, apparatus class)
APP={'rods/chain':'#8a6d3b','Hassler bars':'#6250d6','Bache–Würdemann':'#2a78d6','Colby bars':'#1baf7a','Schott / Eimbeck bars':'#eda100','steel tapes':'#eb6834'}
B=[(0,1834,'Hassler bars','Fire Island'),(0,1844,'Hassler bars','Massachusetts, Kent Island'),(0,1847,'Bache–Würdemann','Dauphin Island'),(0,1857,'Bache–Würdemann','Epping'),(0,1873,'Bache–Würdemann','Atlanta (×3)'),
   (1,1844,'Hassler bars','Kent Island'),(1,1881,'Schott / Eimbeck bars','Yolo'),(1,1891,'steel tapes','Holton'),(1,1892,'steel tapes','St Albans'),(1,1897,'Schott / Eimbeck bars','Salt Lake'),
   (2,1841,'Colby bars','Zwartland'),
   (5,1800,'rods/chain','Bangalore'),(5,1804,'rods/chain','Bangalore check'),(6,1802,'rods/chain','St Thomas Mount'),
   (8,1784,'rods/chain','Hounslow Heath'),(9,1739,'rods/chain','La Crau')]
fig,ax=plt.subplots(figsize=(12.5,6.2),dpi=160,facecolor=BG); ax.set_facecolor(BG)
n=len(S)
for i,(lab,a,b,pub,core,ok) in enumerate(S):
    y=n-1-i
    ax.text(1728,y,lab,ha='right',va='center',fontsize=10,color=INK,fontweight='bold' if core else 'normal')
    if a: ax.plot([a,b],[y,y],color='#2a5fa8' if core else '#a9a294',lw=9,solid_capstyle='butt',zorder=2)
    else: ax.text(pub-2,y,'field dates vary / unconfirmed',ha='right',va='center',fontsize=8.5,color=MUT,style='italic')
    ax.plot(pub,y,marker='|',ms=14,mew=2,color=INK,zorder=3)
for i,yr,app,name in B:
    y=n-1-i; ax.plot(yr,y,'o',ms=8.5,color=APP[app],mec=BG,mew=1.2,zorder=4)
ax.set_xlim(1730,1912); ax.set_ylim(-0.8,n-0.3); ax.set_yticks([])
for k in ('top','right','left'): ax.spines[k].set_visible(False)
ax.set_xticks(range(1740,1911,20)); ax.grid(axis='x',color='#e3dccb',lw=0.6); ax.set_axisbelow(True)
hs=[plt.Line2D([],[],marker='o',ls='',color=c,ms=8,label=k) for k,c in APP.items()]
hs+= [plt.Line2D([],[],color='#2a5fa8',lw=7,label='field work (core)'),plt.Line2D([],[],color='#a9a294',lw=7,label='field work (appendix)'),plt.Line2D([],[],marker='|',ls='',ms=12,mew=2,color=INK,label='published')]
ax.legend(handles=hs,loc='upper center',bbox_to_anchor=(0.42,-0.07),ncol=5,frameon=False,fontsize=9)
fig.text(0.02,0.955,'WHEN EACH SURVEY WAS OBSERVED · BASE LINES BY APPARATUS',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.subplots_adjust(top=0.92,left=0.27,right=0.98,bottom=0.2)
fig.savefig('timeline.png',facecolor=BG)
