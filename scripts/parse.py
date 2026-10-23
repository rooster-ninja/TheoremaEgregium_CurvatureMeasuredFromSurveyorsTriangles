import sys, re, json, xml.etree.ElementTree as ET
ns={'k':'http://www.opengis.net/kml/2.2'}
t=ET.parse(sys.argv[1]); doc=t.getroot()[0]
out=[]
for f in doc.findall('k:Folder',ns):
    name=f.find('k:name',ns).text
    pts=[];polys=[]
    def walk(e,sub=None):
        for c in e:
            tag=c.tag.split('}')[1]
            if tag=='Folder': walk(c,c.find('k:name',ns).text)
            elif tag=='Placemark':
                n=c.find('k:name',ns).text; d=c.find('k:description',ns); d=d.text if d is not None else ''
                s=c.find('k:styleUrl',ns); s=s.text if s is not None else ''
                p=c.find('.//k:Point/k:coordinates',ns)
                if p is not None:
                    lon,lat,h=map(float,p.text.strip().split(','));pts.append(dict(n=n,lon=lon,lat=lat,h=h,d=d,sub=sub))
                else:
                    cs=c.find('.//k:coordinates',ns).text.split()
                    polys.append(dict(n=n,s=s,d=d,sub=sub,c=[tuple(map(float,x.split(',')))[:3] for x in cs]))
    walk(f)
    out.append(dict(name=name,pts=pts,polys=polys))
json.dump(out,open('data.json','w'))
for o in out:
    lats=[p['lat'] for p in o['pts']]; lons=[p['lon'] for p in o['pts']]; hs=[p['h'] for p in o['pts']]
    print(len(o['pts']),len(o['polys']),o['name'][:140])
    if lats: print('   lat %.2f..%.2f lon %.2f..%.2f h %.0f..%.0f'%(min(lats),max(lats),min(lons),max(lons),min(hs),max(hs)))
    subs=set(p['sub'] for p in o['pts']); 
    if subs!={None}: print('   subs',subs)
    if o['polys']: print('   poly ex:',o['polys'][0]['n'],'|',o['polys'][0]['d'][:200])
    if o['pts']: print('   pt ex:',o['pts'][0]['d'][:200])
