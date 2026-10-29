import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const root='/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(root+'/output/XOR-Ho-so-CD4-v2.5/Bo-1-Ky-thuat/02_Checklist_ra_soat_XOR_cap_do_4.xlsx'));
for(const [id,range] of [['controller','L32:O32'],['vm','A60:H64']]){
 const b=await wb.render({sheetName:'Tai san',range,scale:1.25,format:'png'});
 await fs.writeFile(root+'/tmp/ho-so-v2-5/final-'+id+'.png',new Uint8Array(await b.arrayBuffer()));
}
