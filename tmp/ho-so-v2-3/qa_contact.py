from pathlib import Path
from PIL import Image,ImageDraw
import json,pdfplumber
tmp=Path(__file__).parent
out=tmp/'contact';out.mkdir(exist_ok=True)
data=json.loads((tmp/'render-results.json').read_text())
manifest=[];audit=[]
for d in sorted(data,key=lambda x:x['index']):
    folder=Path(d['dir'])
    pdf=next(folder.glob('*.pdf'))
    doc=pdfplumber.open(pdf)
    pages=sorted(folder.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1]))
    for n,p in enumerate(pages):
        manifest.append({'doc':d['index'],'page':n+1,'path':str(p)})
        text=doc.pages[n].extract_text() or ''
        audit.append({'doc':d['index'],'page':n+1,'chars':len(text),'head':text[:110],'tail':text[-150:]})
for start in range(0,len(manifest),6):
    canvas=Image.new('RGB',(1200,2640),'#dddddd');draw=ImageDraw.Draw(canvas)
    for j,rec in enumerate(manifest[start:start+6]):
        im=Image.open(rec['path']).convert('RGB');im.thumbnail((590,845))
        x=(j%2)*600+(600-im.width)//2;y=(j//2)*880+24
        canvas.paste(im,(x,y));draw.text((x,y-19),f"DOC {rec['doc']:02d} / PAGE {rec['page']:02d}",fill='black')
    canvas.save(out/f'{start//6+1:02d}.png')
(tmp/'page-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
(tmp/'page-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(len(manifest),'pages',len(list(out.glob('*.png'))),'contacts')
print('Sparse pages:',[(x['doc'],x['page'],x['chars'],x['head']) for x in audit if x['chars']<250])
