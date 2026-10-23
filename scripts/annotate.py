# Extract source pages from Schott 1900 / 1902 scans and annotate checks (green = verified, red = misprint).
import fitz,sys
OUT=sys.argv[1] if len(sys.argv)>1 else '../pkg/sources/'
GREEN=(0.1,0.6,0.25); RED=(0.85,0.1,0.1)
def mk(src,pages,out,notes):
    s=fitz.open(src); d=fitz.open()
    for p in pages: d.insert_pdf(s,from_page=p-1,to_page=p-1)
    for i,p in enumerate(pages):
        pg=d[i]
        for kind,text,box in notes.get(p,[]):
            col=GREEN if kind=='g' else RED
            if box:
                sx=pg.rect.width/box[4]; r=fitz.Rect(box[0]*sx,box[1]*sx,box[2]*sx,box[3]*sx)
                h=pg.add_rect_annot(r); h.set_colors(stroke=col); h.set_border(width=1.5); h.set_info(content=text,title='Check'); h.update()
                a=pg.add_text_annot(fitz.Point(r.x1+6,r.y0),text,icon='Note')
            else: a=pg.add_text_annot(fitz.Point(pg.rect.width-40,30),text,icon='Note')
            a.set_colors(stroke=col); a.set_info(title='Check'); a.update()
    d.save(out); print(out,len(d))
mk('sp4.pdf',[424,485,616,619],OUT+'Source_Schott1900_triangle_tables_pp414-591_annotated.pdf',{
 424:[('g','Verified: all 9 triangles on p. 414 match the KML entry by entry (angles to 0.01″).',None),
      ('r','Misprint: Cherry Ridge printed 20° 10′ 13.41″. Printed sides (11 997.12 opposite, 24 389.25, 18 130.38 m) give 28.17° by the law of cosines, so the angle is 28° 10′ 13.41″. Triangle then sums to 179° 59′ 58.55″. Corrected and kept.',(335,606,435,624,946))],
 485:[('g','Verified: all 9 triangles on p. 474 match the KML entry by entry.',None)],
 616:[('g','Verified: all 9 triangles on p. 588 match the KML. Schott carries seconds above 60 (e.g. 63.476″) so the minutes stay fixed; the KML keeps this convention.',None)],
 619:[('g','Verified: all 9 triangles on p. 591 match the KML. No. 32 (Mount Nebo – Tushar – Wheeler Peak) is the largest triangle in the file: excess 75.33″ observed, 73.76″ spherical.',None),
      ('r','Misprint: Ibepah printed 10° 09′ 30.489″; the three angles then sum to 79°. Printed sides (237 769.08 opposite Ibepah, 99 493.31, 184 375.27 m) give 110.15°, so the angle is 110° 09′ 30.489″. Excess 42.957″ vs 43.716″ spherical. Corrected and kept.',(335,728,440,746,951))]})
mk('sp7.pdf',[153],OUT+'Source_Schott1902_triangle_table_p131_annotated.pdf',{
 153:[('g','Verified: all 12 triangles on p. 131 match the KML entry by entry.',None),
      ('r','Misprint: Mount Pleasant printed 19° 54′ 04.38″ (digits swapped). Printed sides (88 811.79 opposite, 50 110.16, 71 681.66 m) give 91.90°, so the angle is 91° 54′ 04.38″. Excess 7.11″ vs 9.11″ spherical. Corrected and kept.',(290,893,400,911,849))]})
mk('sp4.pdf',[435,569,570,571,573,580,591,630],OUT+'Source_Schott1900_plates.pdf',{})
mk('sp7.pdf',[36,38,158,160],OUT+'Source_Schott1902_plates.pdf',{})
