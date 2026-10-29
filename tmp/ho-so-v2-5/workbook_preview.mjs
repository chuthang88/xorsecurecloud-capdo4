import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const base='/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(base+'/output/XOR-Ho-so-CD4-v2.4/Bo-1-Ky-thuat/02_Checklist_ra_soat_XOR_cap_do_4.xlsx'));
for(const [id,sheetName,range] of [['assets','Tai san','A5:H9'],['evidence','Bang chung','A5:F8'],['controls','TCVN','H11:O12']]){
 const blob=await wb.render({sheetName,range,scale:1.2,format:'png'});
 await fs.writeFile(base+'/tmp/ho-so-v2-5/before-'+id+'.png',new Uint8Array(await blob.arrayBuffer()));
}
console.log(wb.help('table.resize',{include:'index,examples,notes',maxChars:2000}).ndjson);
console.log((await wb.inspect({kind:'table',sheetId:'Tai san',maxChars:2000,tableMaxRows:1,tableMaxCols:3})).ndjson);
