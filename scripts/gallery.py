from PIL import Image,ImageDraw,ImageFont
import textwrap
items=[('sp4_591','Uncompahgre Peak station: observing the heliotrope on Mount Ellen, 294.1 km away','Schott 1900, No. 45'),
 ('sp4_569','Heliotropes of the latest pattern','Schott 1900, No. 37'),
 ('sp4_570','The 50 cm (20-inch) theodolite used at the primary stations in the Rocky Mountains','Schott 1900, No. 38'),
 ('sp4_571','Ogden Peak station: instrument on its position stand (2,924 m)','Schott 1900, No. 39'),
 ('sp4_573','Tushar Mountain summit station: ring wall and double shelter tent (3,702 m)','Schott 1900, No. 41'),
 ('sp4_580','Summit station on Uncompahgre Peak, Colorado (4,355 m)','Schott 1900, No. 44'),
 ('sp4_435','Scaffolding at station Greene, Indiana: instrument 46.3 m above ground','Schott 1900, No. 29'),
 ('sp4_630','The Great Caspar signal, California: instrument 41.1 m up, observer on a separate frame','Schott 1900, No. 50'),
 ('sp7_160','75 cm (30-inch) direction theodolite','Schott 1902, Plate 19'),
 ('sp7_158','30 cm (12-inch) theodolite','Schott 1902, Plate 20'),
 ('sp7_36','Epping base, Maine: view of the line as graded for measurement (1857)','Schott 1902, Plate 2'),
 ('sp7_38','Epping base: placing the apparatus over a mark (1857)','Schott 1902, Plate 3')]
W,H=520,600; cols=4; rows=3; cap=96
sheet=Image.new('RGB',(cols*W,rows*(H+cap)+70),(246,241,231)); d=ImageDraw.Draw(sheet)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',16)
FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',14); FT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',18)
d.text((20,22),'EQUIPMENT AND STATIONS · PLATES FROM SCHOTT 1900 AND 1902 · PREVIEW, NOT IN REPORT',fill=(42,95,168),font=FT)
for i,(n,c,s) in enumerate(items):
    im=Image.open(f'crop/{n}.jpg'); im.thumbnail((W-20,H-20)); x=(i%cols)*W; y=70+(i//cols)*(H+cap)
    sheet.paste(im,(x+(W-im.width)//2,y+(H-im.height)//2)); yy=y+H+4
    d.text((x+12,yy),f'{i+1}',fill=(29,29,27),font=FB)
    for j,l in enumerate(textwrap.wrap(c,46)[:3]): d.text((x+42,yy+j*20),l,fill=(29,29,27),font=F)
    d.text((x+42,yy+64),s,fill=(90,86,80),font=FS)
sheet.save('plates_preview.jpg',quality=88)
