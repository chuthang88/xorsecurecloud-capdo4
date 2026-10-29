from pathlib import Path
import json
import pdfplumber
from PIL import Image,ImageOps,ImageDraw
P=Path(__file__).parent
results=json.loads((P/'render-results.json').read_text()); pages=[];alerts=[]
for r in results:
 pdf=list(Path(r['dir']).glob('*.pdf'))[0]
 with pdfplumber.open(pdf) as d:
  for i,p in enumerate(d.pages):
   t=p.extract_text() or ''; pages.append({'index':r['index'],'file':r['file'],'page':i+1,'png':str(Path(r['dir'])/f'page-{i+1}.png'),'text':t,'chars':len(t),'width':p.width,'height':p.height})
   if len(t)<40 and not p.images:alerts.append({'index':r['index'],'page':i+1,'text':t})
(P/'pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
print('Pages',len(pages),'Blank candidates',alerts)
out=P/'contact';out.mkdir(exist_ok=True)
for k in range(0,len(pages),6):
 batch=pages[k:k+6];canvas=Image.new('RGB',(1600,2220),'#bbb');draw=ImageDraw.Draw(canvas)
 for j,p in enumerate(batch):
  img=Image.open(p['png']).convert('RGB');img.thumbnail((780,1020));x=(j%2)*800+(800-img.width)//2;y=(j//2)*740+32
  # Thumbnail keeps whole page visible including landscape.
  img.thumbnail((780,690));x=(j%2)*800+(800-img.width)//2
  canvas.paste(img,(x,y));draw.text(((j%2)*800+10,(j//2)*740+8),f"{p['index']:02d} / p{p['page']}  {p['file'][:45]}",fill='black')
 canvas.save(out/f'{k//6+1:02d}.png')
