import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const base='/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud';
const tmp=base+'/tmp/ho-so-v2-4';
const name='02_Checklist_ra_soat_XOR_cap_do_4.xlsx';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(base+'/output/XOR-Ho-so-CD4-v2.3/Bo-1-Ky-thuat/'+name));
const phase=process.argv[2]||'before';
if(phase==='after'){
 wb.worksheets.getItem('Cloud').getRange('B6:B23').values=[['Nền tảng cloud']];
 wb.worksheets.getItem('Cloud').getRange('D6').values=[['Bản dựng XOR\nGắn phiên bản XOR, commit, nguồn phần mềm và danh mục khác biệt; đối chiếu tính năng với bản dựng thực tế.']];
 wb.worksheets.getItem('Huong dan').getRange('E31').values=[['XOR STACK CLOUD; toàn nền tảng; DC Cầu Giấy, DR Nam Thăng Long; hồ sơ lần đầu.']];
 const h=wb.worksheets.getItem('Ho so');
 for(const [cell,text] of [['E10','04 Công văn và 08 Ý kiến chuyên môn'],['E14','07 Quyết định phê duyệt cấp độ'],['E20','09 Báo cáo rà soát và báo cáo bên đánh giá'],['E22','12 Thông báo cấp độ'],['E23','11 Công văn đề nghị đánh giá']])h.getRange(cell).values=[[text]];
 h.getRange('E5').values=[['Tài liệu liên quan']];
 wb.recalculate();
 console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:15},maxChars:1500})).ndjson);
 await(await SpreadsheetFile.exportXlsx(wb)).save(base+'/output/XOR-Ho-so-CD4-v2.4/Bo-1-Ky-thuat/'+name);
}
for(const [id,sheetName,range] of [['cloud','Cloud','A5:F7'],['scope','Huong dan','A30:E32'],['documents','Ho so','D5:F14']]){
 const image=await wb.render({sheetName,range,scale:1.3,format:'png'});
 await fs.writeFile(tmp+'/xlsx-'+phase+'-'+id+'.png',new Uint8Array(await image.arrayBuffer()));
}
console.log(phase+' completed');
