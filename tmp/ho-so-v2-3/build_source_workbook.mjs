import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const dir=path.dirname(fileURLToPath(import.meta.url));
const root='/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud';
const data=JSON.parse(await fs.readFile(path.join(dir,'source-controls.json'),'utf8'));
const out=path.join(root,'output/XOR-Ho-so-CD4-v2.3/Bo-1-Ky-thuat/04_Doi_soat_129_hang_muc_v094.xlsx');
const wb=Workbook.create();
const work=wb.worksheets.add('Doi_soat');
const src=wb.worksheets.add('Nguon_v094');
const first=9,last=first+data.length-1;
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
function base(s,headers,widths,rows){
 s.showGridLines=false;
 const end=col(headers.length-1);
 s.getRange(`A1:${end}${last}`).format.font={name:'Times New Roman',size:10,color:'#000000'};
 s.getRange(`A1:${end}${last}`).format.verticalAlignment='center';
 s.getRange(`A8:${end}8`).values=[headers];
 s.getRange(`A8:${end}8`).format={fill:'#FFFFFF',font:{name:'Times New Roman',size:10,bold:true,color:'#000000'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center',rowHeight:38};
 s.getRange(`A${first}:${end}${last}`).values=rows;
 s.getRange(`A${first}:${end}${last}`).format.wrapText=true;
 widths.forEach((w,i)=>s.getRange(`${col(i)}1:${col(i)}${last}`).format.columnWidthPx=w);
 for(let r=first;r<=last;r++)if(r%2===1)s.getRange(`A${r}:${end}${r}`).format.fill='#FFFFFF';
 s.freezePanes.freezeRows(8);s.freezePanes.freezeColumns(1);
 const t=s.tables.add(`A8:${end}${last}`,true,s.name==='Doi_soat'?'DoiSoat129':'Nguon129');
 t.showFilterButton=true;t.style='TableStyleLight1';s.getRange(`A8:${end}${last}`).format.borders={preset:'all',style:'thin',color:'#000000'};
 s.getRange('A2').format.font={name:'Times New Roman',size:15,bold:true,color:'#000000'};
 s.getRange(`A2:${end}2`).format.rowHeight=27;
}
const workRows=data.map(d=>[d.id,d.item,d.priority,d.legacy_status,d.owner,'Chưa xác minh',null,null,null,null,null,null,null,null]);
base(work,['Mã nguồn','Hạng mục','Ưu tiên nguồn','Trạng thái nguồn','Đầu mối nguồn','Kết quả hiện tại','Người phụ trách','Hạn xử lý','Mã hoặc đường dẫn EV','Người xác minh','Ngày xác minh','Hành động và kết luận mới','Mã TC CL HS T liên quan','Tình trạng dữ liệu'],[132,265,85,160,170,175,165,110,240,165,115,420,190,230],workRows);
work.tabColor='#666666';
work.getRange('A2').values=[['Đối soát 129 hạng mục từ hồ sơ tham khảo']];
work.getRange('A3').values=[['Tổng hạng mục']];work.getRange('B3').formulas=[[`=COUNTA(A${first}:A${last})`]];
work.getRange('D3').values=[['Chưa xác minh']];work.getRange('E3').formulas=[[`=COUNTIFS(F${first}:F${last},"Chưa xác minh")`]];
work.getRange('F3').values=[['Cần khắc phục']];work.getRange('G3').formulas=[[`=COUNTIFS(F${first}:F${last},"Không đạt")`]];
work.getRange('I3').values=[['Đủ dữ liệu xác minh']];work.getRange('J3').formulas=[[`=COUNTIFS(N${first}:N${last},"Đủ dữ liệu xác minh")`]];
for(const a of ['B3','E3','G3','J3']){work.getRange(a).format.horizontalAlignment='center';work.getRange(a).format.font.bold=true;}
work.getRange('A5').values=[['Ô nền xám nhạt nhập kết quả hiện tại. Tab Nguon_v094 giữ thông tin lịch sử; không chuyển trạng thái cũ thành kết quả mới.']];
work.getRange('A6').values=[['Đạt hoặc Không áp dụng cần có người phụ trách, EV, người và ngày xác minh, hành động/kết luận. Không áp dụng phải ghi căn cứ và EV phê duyệt.']];
work.getRange('A7').values=[['Mã liên quan do người kiểm tra xác định trong workbook 02; không ghép tự động 129 mục nguồn với 119 dòng TC.']];
work.getRange(`A${first}:N${last}`).format.rowHeight=64;
work.getRange(`F${first}:M${last}`).format.fill='#F2F2F2';
work.getRange(`H${first}:H${last}`).setNumberFormat('dd/mm/yyyy');
work.getRange(`K${first}:K${last}`).setNumberFormat('dd/mm/yyyy');
work.getRange(`F${first}:F${last}`).dataValidation={rule:{type:'list',values:['Chưa xác minh','Chưa đủ bằng chứng','Không đạt','Đạt','Không áp dụng']}};
const formulas=data.map((_,i)=>{const r=first+i;return [`=IF(F${r}="Không đạt","Cần khắc phục",IF(F${r}="Chưa xác minh","Chưa xác minh",IF(F${r}="Chưa đủ bằng chứng","Bổ sung bằng chứng",IF(AND(OR(F${r}="Đạt",F${r}="Không áp dụng"),G${r}<>"",I${r}<>"",J${r}<>"",ISNUMBER(K${r}),K${r}>0,L${r}<>""),"Đủ dữ liệu xác minh","Thiếu hồ sơ xác minh"))))`];});
work.getRange(`N${first}:N${last}`).formulas=formulas;
work.getRange(`N${first}:N${last}`).conditionalFormats.add('containsText',{text:'Cần khắc phục',format:{fill:'#D9D9D9',font:{color:'#000000',bold:true}}});
work.getRange(`N${first}:N${last}`).conditionalFormats.add('containsText',{text:'Thiếu hồ sơ',format:{fill:'#F2F2F2',font:{color:'#000000'}}});

const sourceRows=data.map(d=>[d.id,d.group,d.item,d.criterion,d.legacy_status,d.legacy_gap,d.evidence,d.owner,d.priority,d.legacy_ref]);
base(src,['Mã nguồn','Nhóm nguồn','Hạng mục','Tiêu chí ghi trong nguồn','Trạng thái lịch sử','Tồn tại ghi trong nguồn','Bằng chứng tối thiểu theo nguồn','Đầu mối nguồn','Ưu tiên nguồn','Căn cứ ghi trong nguồn'],[132,220,260,560,160,500,350,180,90,320],sourceRows);
src.getRange('A2').values=[['Dữ liệu tham khảo từ bản 0.9.4']];
src.getRange('A4').values=[['Nguồn: XOR_SECURE_CLOUD_Ho_so_Cap_do_4_v0.9.4.docx, ngày 06/10/2026, Phụ lục D, đủ 129 mã C4.']];
src.getRange('A5').values=[['Các căn cứ và kết quả ở tab này được giữ từ nguồn để truy vết. Phải đối chiếu căn cứ hiện hành và kiểm tra lại trước kết luận.']];
src.getRange('A6').values=[['C4-DC-18: chủ quản đã xác nhận DC Cầu Giấy và DR Nam Thăng Long. Bằng chứng cấu hình, sao chép và diễn tập còn phải kiểm tra.']];
src.getRange('A7').values=[['97 Chưa đánh giá; 21 Đang thực hiện; 6 Không đạt; 4 Cần xác minh; 1 Đạt. Chỉ là phân bố trạng thái của tài liệu nguồn.']];
for(let i=0;i<data.length;i++){
 const cells=sourceRows[i];const widths=[132,220,260,560,160,500,350,180,90,320];
 const lines=Math.max(...cells.map((v,j)=>Math.ceil(String(v).length/Math.floor(widths[j]/6.3))));
 src.getRange(`A${first+i}:J${first+i}`).format.rowHeight=Math.max(74,lines*14+20);
}

// Check the workflow before restoring the blank working fields.
const states=[];const r=first;
work.getRange(`F${r}`).values=[['Đạt']];wb.recalculate();states.push(work.getRange(`N${r}`).values[0][0]);
work.getRange(`G${r}`).values=[['Người thử']];work.getRange(`I${r}:L${r}`).values=[['EV-TEST','Người xác minh',new Date('2026-10-17T00:00:00Z'),'Đã đối chiếu và xác nhận']];wb.recalculate();states.push(work.getRange(`N${r}`).values[0][0]);
work.getRange(`I${r}`).values=[[null]];wb.recalculate();states.push(work.getRange(`N${r}`).values[0][0]);
work.getRange(`F${r}`).values=[['Không đạt']];wb.recalculate();states.push(work.getRange(`N${r}`).values[0][0]);
work.getRange(`F${r}`).values=[['Không áp dụng']];wb.recalculate();states.push(work.getRange(`N${r}`).values[0][0]);
if(JSON.stringify(states)!==JSON.stringify(['Thiếu hồ sơ xác minh','Đủ dữ liệu xác minh','Thiếu hồ sơ xác minh','Cần khắc phục','Thiếu hồ sơ xác minh']))throw Error('Workflow states: '+JSON.stringify(states));
work.getRange(`F${r}:M${r}`).values=[['Chưa xác minh',null,null,null,null,null,null,null]];
wb.recalculate();
if(work.getRange('B3').values[0][0]!==129||work.getRange('E3').values[0][0]!==129||work.getRange('J3').values[0][0]!==0)throw Error('Initial totals incorrect');
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},maxChars:2000});
await fs.writeFile(path.join(dir,'source-workbook-error-scan.txt'),errors.ndjson);
for(const [sheetName,range,file] of [['Doi_soat','A1:G12','work-left'],['Doi_soat','H8:N12','work-right'],['Nguon_v094','A8:E11','source-left'],['Nguon_v094','F8:J11','source-right']]){
 const p=await wb.render({sheetName,range,scale:1.3,format:'png'});
 await fs.writeFile(path.join(dir,file+'.png'),new Uint8Array(await p.arrayBuffer()));
}
const file=await SpreadsheetFile.exportXlsx(wb);await file.save(out);
await fs.writeFile(path.join(dir,'source-workbook-qa.json'),JSON.stringify({rows:data.length,uniqueIds:new Set(data.map(x=>x.id)).size,workflowStates:states,initialUnverified:129,initialComplete:0,output:out},null,2));
console.log(JSON.stringify({output:out,rows:data.length,workflowStates:states,errorScan:errors.ndjson}));
