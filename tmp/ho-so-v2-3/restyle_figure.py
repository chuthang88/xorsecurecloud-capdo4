from pathlib import Path
from lxml import etree as E
root=Path('/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud')
src=root/'output/XOR-Ho-so-CD4-v2.2/Bo-1-Ky-thuat/So_do_kien_truc_muc_tieu.svg'
tree=E.parse(str(src));ns={'s':'http://www.w3.org/2000/svg'}
for n in tree.iter():
 tag=E.QName(n).localname
 if tag=='text':
  n.set('font-family','Times New Roman, Times, serif');n.set('fill','#000000')
 elif tag=='rect':
  n.set('fill','#FFFFFF')
  if n.get('stroke'):n.set('stroke','#000000')
  if n.get('rx'):n.set('rx','8')
 elif tag in ['polyline','path']:
  if n.get('stroke'):n.set('stroke','#000000')
  if n.get('fill') not in [None,'none']:n.set('fill','#000000')
# Double outlines emphasize the control plane and independent recovery boundary.
svg=tree.getroot()
for n in list(svg):
 if E.QName(n).localname=='rect' and (n.get('x'),n.get('y')) in [('630','690'),('630','880'),('40','1230')]:
  inner=E.Element('{http://www.w3.org/2000/svg}rect')
  for k,v in {'x':float(n.get('x'))+7,'y':float(n.get('y'))+7,'width':float(n.get('width'))-14,'height':float(n.get('height'))-14}.items():inner.set(k,str(v))
  inner.set('fill','none');inner.set('stroke','#000000');inner.set('stroke-width','1');inner.set('rx','4');n.addnext(inner)
(root/'tmp/ho-so-v2-3/So_do_kien_truc_muc_tieu.svg').write_bytes(E.tostring(svg,xml_declaration=True,encoding='UTF-8'))
