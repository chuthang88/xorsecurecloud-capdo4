import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';
const base='/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud';
const tmp=path.join(base,'tmp/ho-so-v2-3');
const out=path.join(base,'output/XOR-Ho-so-CD4-v2.3/Bo-1-Ky-thuat');
const data=JSON.parse(await fs.readFile(path.join(tmp,'data.json'),'utf8'));
const wb=Workbook.create();
const names=['Tong hop','TCVN','Cloud','Ho so','Kiem thu','BIA','Rui ro','Tai san','Bang chung','Huong dan'];
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const col=i=>{let s='';for(let n=i+1;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;};
function baseSheet(name,title,headers,rows,widths){
 const s=sheets[name], end=rows.length+5, last=col(headers.length-1);
 s.showGridLines=false;
 s.getRange(`A1:${last}${end}`).format.font={name:'Times New Roman',size:11,color:'#000000'};
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Times New Roman',size:16,bold:true};
 s.getRange(`A5:${last}5`).values=[headers];
 if(rows.length)s.getRange(`A6:${last}${end}`).values=rows;
 s.getRange(`A5:${last}${end}`).format.wrapText=true;
 s.getRange(`A5:${last}${end}`).format.verticalAlignment='top';
 s.getRange(`A5:${last}5`).format={fill:'#FFFFFF',font:{name:'Times New Roman',size:11,bold:true,color:'#000000'},rowHeight:40,wrapText:true,verticalAlignment:'center'};
 widths.forEach((w,i)=>s.getRange(`${col(i)}1:${col(i)}${end}`).format.columnWidth=w);
 s.getRange(`A6:${last}${end}`).format.rowHeight=98;
 for(let r=6;r<=end;r++)if(r%2===0)s.getRange(`A${r}:${last}${r}`).format.fill='#FFFFFF';
 const table=s.tables.add(`A5:${last}${end}`,true,name.replace(/ /g,'')+'Table');table.showFilterButton=true;table.style='TableStyleLight1';s.getRange(`A5:${last}${end}`).format.borders={preset:'all',style:'thin',color:'#000000'};
 s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(2);
 return {s,end,last};
}
function input(s,range){s.getRange(range).format.fill='#F2F2F2';}
function list(s,range,values){s.getRange(range).dataValidation={rule:{type:'list',values}};}
function colors(s,range){
 for(const [t,c] of [['Đủ hồ sơ kiểm tra','#FFFFFF'],['Đủ hồ sơ theo khai báo','#FFFFFF'],['Cần khắc phục','#D9D9D9'],['Chưa đủ bằng chứng','#ECECEC'],['Thiếu bằng chứng','#ECECEC'],['Chờ duyệt không áp dụng','#ECECEC'],['Không áp dụng đã duyệt','#F2F2F2']])s.getRange(range).conditionalFormats.add('containsText',{text:t,format:{fill:c}});
}
const controlHeads=['Mã','Nhóm','Điều khoản và trang','Nội dung cần rà soát','Cách kiểm tra','Bằng chứng cần có','Đầu mối đề xuất','Phạm vi thực tế','Áp dụng','Triển khai','Mã hoặc đường dẫn bằng chứng','Kết quả kiểm tra','Người kiểm tra','Ngày kiểm tra','Thiếu sót và hành động','Người xử lý','Hạn xử lý','Trạng thái tổng hợp','Căn cứ và phê duyệt không áp dụng'];
function checklist(name,items){
 const rows=items.map(x=>[x.id,x.group,`${x.source}\n${x.clause}${x.page?' • tr.'+x.page:''}`,`${x.title}\n${x.requirement}`,x.test,x.evidence,x.owner,'DC Cầu Giấy và DR Nam Thăng Long',name==='Cloud'&&x.id>='CL-09'?'Chưa chốt':'Có','Chưa xác minh','','Chưa kiểm tra','',null,'','',null,'','']);
 const {s,end}=baseSheet(name,name==='TCVN'?'Rà soát yêu cầu TCVN cấp độ 4':'Rà soát đặc thù XOR STACK CLOUD',controlHeads,rows,[12,23,29,53,46,40,24,31,18,22,36,22,23,18,42,22,18,30,40]);
 s.getRange('A3').values=[['Ô nền xám nhạt để nhập. Phạm vi “cả hai IDC” chỉ hoàn tất khi bằng chứng bao phủ cả DC và DR. Trạng thái do công thức tính, không phải kết luận chứng nhận.']];
 input(s,`H6:Q${end}`);input(s,`S6:S${end}`);
 list(s,`I6:I${end}`,['Có','Không áp dụng','Chưa chốt']);list(s,`J6:J${end}`,['Chưa xác minh','Chưa triển khai','Một phần','Đầy đủ']);list(s,`L6:L${end}`,['Chưa kiểm tra','Đạt','Không đạt']);
 s.getRange(`N6:N${end}`).setNumberFormat('dd/mm/yyyy');s.getRange(`Q6:Q${end}`).setNumberFormat('dd/mm/yyyy');
 s.getRange(`R6:R${end}`).formulas=rows.map((_,i)=>{const r=i+6;return [`=IF(I${r}="Không áp dụng",IF(AND(S${r}<>"",M${r}<>"",ISNUMBER(N${r})),"Không áp dụng đã duyệt","Chờ duyệt không áp dụng"),IF(I${r}<>"Có","Chưa chốt phạm vi",IF(J${r}="Chưa xác minh","Chưa đủ bằng chứng",IF(J${r}<>"Đầy đủ","Cần bổ sung triển khai",IF(K${r}="","Thiếu bằng chứng",IF(L${r}<>"Đạt",IF(L${r}="Không đạt","Cần khắc phục","Chưa kiểm tra"),IF(OR(M${r}="",NOT(ISNUMBER(N${r}))),"Chờ xác nhận","Đủ hồ sơ kiểm tra")))))))`];});
 colors(s,`R6:R${end}`);
 s.getRange(`Q6:Q${end}`).conditionalFormats.addCustom(`AND(ISNUMBER(Q6),Q6<'Huong dan'!$B$4,R6<>"Đủ hồ sơ kiểm tra",R6<>"Không áp dụng đã duyệt")`,{fill:'#D9D9D9',font:{color:'#000000'}});
 return end;
}
const tcEnd=checklist('TCVN',data.controls),cloudEnd=checklist('Cloud',data.extra);
{
 const rows=data.dossier.map(x=>[x[0],x[1],x[2],x[4],x[3],x[5],'Chưa đủ','','',null,'',null,'']);
 const {s,end}=baseSheet('Ho so','Danh mục hồ sơ cần hoàn thiện',['Mã','Tài liệu','Căn cứ','Nội dung phải có','Vị trí dự thảo','Đầu mối','Độ đầy đủ','Bằng chứng bản đã xác nhận','Người xác nhận','Ngày xác nhận','Thiếu sót và hành động','Hạn hoàn thành','Trạng thái'],rows,[12,32,27,60,40,28,20,40,24,18,45,18,30]);
 input(s,`G6:L${end}`);list(s,`G6:G${end}`,['Chưa đủ','Một phần','Đầy đủ']);s.getRange(`J6:J${end}`).setNumberFormat('dd/mm/yyyy');s.getRange(`L6:L${end}`).setNumberFormat('dd/mm/yyyy');
 s.getRange(`M6:M${end}`).formulas=rows.map((_,i)=>{const r=i+6;return [`=IF(G${r}<>"Đầy đủ","Cần bổ sung",IF(H${r}="","Thiếu bằng chứng",IF(OR(I${r}="",NOT(ISNUMBER(J${r}))),"Chờ xác nhận","Đủ hồ sơ theo khai báo")))`];});colors(s,`M6:M${end}`);
}
{
 const rows=data.tests.map(x=>[x[0],x[1],x[3],x[2],x[4],x[5],x[6],x[7],'','Chưa thực hiện',null,'','','','']);
 const {s,end}=baseSheet('Kiem thu','Kế hoạch và kết quả kiểm thử',['Mã','Kịch bản','Căn cứ','Đầu mối','Điều kiện trước thử','Các bước','Tiêu chí chấp nhận','Bằng chứng cần lưu','Kết quả thực tế và số đo','Kết luận','Ngày thực hiện','Người xác nhận','Mã hoặc đường dẫn bằng chứng','Phát hiện và retest','Trạng thái'],rows,[12,30,26,25,48,68,58,46,48,22,18,24,42,44,30]);
 input(s,`I6:N${end}`);list(s,`J6:J${end}`,['Chưa thực hiện','Đạt','Không đạt']);s.getRange(`K6:K${end}`).setNumberFormat('dd/mm/yyyy');s.getRange(`A6:O${end}`).format.rowHeight=142;
 s.getRange(`O6:O${end}`).formulas=rows.map((_,i)=>{let r=i+6;return [`=IF(J${r}="Không đạt","Cần khắc phục",IF(J${r}<>"Đạt","Chưa kiểm tra",IF(OR(I${r}="",L${r}="",M${r}="",NOT(ISNUMBER(K${r}))),"Thiếu bằng chứng","Đủ hồ sơ kiểm tra")))`];});colors(s,`O6:O${end}`);
}
{
 const rows=data.services.map(x=>[x[0],x[1],x[2],x[3],'','','',null,null,null,null,null,'','','']);
 const {s,end}=baseSheet('BIA','Phân tích tác động và mục tiêu phục hồi',['Mã','Dịch vụ','Phụ thuộc cần xác minh','Đối tượng ảnh hưởng','Chủ dịch vụ','Loại dữ liệu','Tác động công cộng xã hội an ninh','RPO phút','RTO phút','MTD phút','Dung lượng GB','Thay đổi GB giờ','Căn cứ và người phê duyệt','Bằng chứng hoặc hợp đồng','Trạng thái'],rows,[12,30,48,36,25,30,48,18,18,18,20,22,45,42,35]);
 input(s,`E6:N${end}`);s.getRange(`H6:L${end}`).setNumberFormat('#,##0.0');
 s.getRange('A3').values=[['RPO: mất dữ liệu tối đa; RTO: thời gian phục hồi; MTD: gián đoạn tối đa chấp nhận. Chưa có chỉ tiêu nào được XOR phê duyệt trong bản này.']];
 s.getRange(`O6:O${end}`).formulas=rows.map((_,i)=>{let r=i+6;return [`=IF(OR(E${r}="",F${r}="",G${r}="",M${r}="",N${r}="",NOT(ISNUMBER(H${r})),NOT(ISNUMBER(I${r})),NOT(ISNUMBER(J${r}))),"Cần hoàn thiện BIA",IF(OR(H${r}<0,I${r}<0,J${r}<0),"Chỉ tiêu không hợp lệ",IF(I${r}>J${r},"RTO vượt MTD","Đủ đầu vào theo khai báo")))`];});
}
{
 const rows=data.risks.map(x=>[x[0],x[1],'[CẦN XÁC ĐỊNH TÀI SẢN]',x[3],x[2],x[4],null,null,'','','',null,'',null,null,'','',null,'']);
 const {s,end}=baseSheet('Rui ro','Sổ đánh giá và xử lý rủi ro',['Mã','Kịch bản','Tài sản và dịch vụ','Tác động cần lượng hóa','Kiểm soát dự kiến','Chủ rủi ro','Khả năng 1 đến 5','Tác động 1 đến 5','Điểm ban đầu','Mức nội bộ','Hành động thực tế','Hạn xử lý','Bằng chứng kiểm soát','Khả năng còn lại','Tác động còn lại','Điểm còn lại','Người chấp nhận','Ngày chấp nhận','Trạng thái'],rows,[12,44,35,50,45,25,19,19,18,23,48,18,42,19,19,18,26,18,35]);
 input(s,`C6:D${end}`);input(s,`F6:H${end}`);input(s,`K6:O${end}`);input(s,`Q6:R${end}`);
 for(const range of [`G6:H${end}`,`N6:O${end}`])s.getRange(range).dataValidation={rule:{type:'whole',operator:'between',formula1:1,formula2:5}};
 s.getRange(`L6:L${end}`).setNumberFormat('dd/mm/yyyy');s.getRange(`R6:R${end}`).setNumberFormat('dd/mm/yyyy');
 s.getRange('A3').values=[['Thang 5×5 là phương pháp nội bộ đề xuất tại Huong dan; không dùng điểm này để tự xác định cấp độ pháp lý. Không điền điểm thay người đánh giá.']];
 for(let r=6;r<=end;r++){
  s.getRange(`I${r}`).formulas=[[`=IF(OR(NOT(ISNUMBER(G${r})),NOT(ISNUMBER(H${r}))),"",G${r}*H${r})`]];
  s.getRange(`J${r}`).formulas=[[`=IF(I${r}="","Chưa đánh giá",IF(I${r}<=4,"Thấp",IF(I${r}<=9,"Trung bình",IF(I${r}<=16,"Cao","Rất cao"))))`]];
  s.getRange(`P${r}`).formulas=[[`=IF(OR(NOT(ISNUMBER(N${r})),NOT(ISNUMBER(O${r}))),"",N${r}*O${r})`]];
  s.getRange(`S${r}`).formulas=[[`=IF(I${r}="","Chưa đánh giá",IF(OR(K${r}="",M${r}="",P${r}=""),"Chưa đủ bằng chứng",IF(OR(Q${r}="",NOT(ISNUMBER(R${r}))),"Chờ chấp nhận rủi ro","Đã ghi nhận chấp nhận")))`]];
 }
}
{
 const cats=['Controller và API','Compute và hypervisor','Mạng và bảo mật','Storage và backup','IAM PAM khóa','SOC và log','OOB và console','PAW và CI CD'];
 const rows=['DC Cầu Giấy','DR Nam Thăng Long'].flatMap(site=>cats.map(g=>['',g,'',site,'','','','','','','',null,'','Chưa kiểm kê','']));
 const {s,end}=baseSheet('Tai san','Danh mục cần kiểm kê theo từng IDC',['Mã tài sản','Nhóm cần kiểm kê','Tên tài sản thực tế','Site','Vùng mạng','IP hoặc endpoint','MAC hoặc serial','Phiên bản phần mềm','Chủ sở hữu','Loại dữ liệu','Mức quan trọng','Hạn hỗ trợ','Bằng chứng cấu hình','Tình trạng kiểm kê','Ghi chú'],rows,[18,31,34,26,23,33,31,30,24,30,23,18,42,25,42]);
 input(s,`A6:O${end}`);list(s,`N6:N${end}`,['Chưa kiểm kê','Đã kiểm kê','Cần xác minh']);s.getRange(`L6:L${end}`).setNumberFormat('dd/mm/yyyy');s.getRange('A3').values=[['Các dòng hiện là nhóm cần kiểm kê, chưa phải danh sách thiết bị có thật. Tạo mã duy nhất cho từng tài sản và ghi rõ phiên bản/phạm vi.']];
}
{
 const rows=Array.from({length:30},(_,i)=>[`EV-${String(i+1).padStart(3,'0')}`,'','','','','','',null,'','','','Chưa thu thập']);
 const {s,end}=baseSheet('Bang chung','Sổ đăng ký bằng chứng',['Mã bằng chứng','Mã yêu cầu hoặc ca thử','Tên nội dung','Site hoặc phạm vi','Loại bằng chứng','Đường dẫn kho','Phiên bản hoặc SHA256','Ngày thu thập','Người thu thập','Người xác minh','Mức bảo vệ','Tình trạng'],rows,[17,27,45,30,27,55,48,18,25,25,26,25]);
 input(s,`B6:L${end}`);list(s,`L6:L${end}`,['Chưa thu thập','Đã thu thập','Đã xác minh','Cần bổ sung']);s.getRange(`H6:H${end}`).setNumberFormat('dd/mm/yyyy');s.getRange('A3').values=[['Mã được đặt sẵn để nhập; không có tệp bằng chứng nào được giả định đã tồn tại. Không đưa mật khẩu, token, khóa bí mật vào workbook.']];
}
{
 const s=sheets['Huong dan'];s.showGridLines=false;s.getRange('A1:F55').format.font={name:'Times New Roman',size:11,color:'#000000'};
 s.getRange('A2').values=[['Hướng dẫn rà soát và nguồn tham chiếu']];s.getRange('A2').format.font={name:'Times New Roman',size:16,bold:true};
 s.getRange('A4:B4').values=[['Ngày chốt báo cáo',new Date('2026-10-17T00:00:00Z')]];s.getRange('B4').setNumberFormat('dd/mm/yyyy');input(s,'B4');
 const notes=[
 ['Phạm vi','Toàn bộ XOR STACK CLOUD và quản trị chung; DC Cầu Giấy, DR Nam Thăng Long. Hồ sơ lần đầu.'],
 ['Trạng thái ban đầu','Không có kết quả kiểm tra thực tế được đưa vào. Các kiểm soát đang chờ xác minh.'],
 ['Quy trình sử dụng','1 Chốt phạm vi. 2 Giao người. 3 Kiểm tra. 4 Thu bằng chứng. 5 Xác nhận độc lập. 6 Khắc phục và retest.'],
 ['Ô nhập','Ô nền xám nhạt là đầu vào. Không ghi đè cột trạng thái có công thức. Ngày phải là ngày Excel, không phải chuỗi văn bản.'],
 ['Đủ hồ sơ kiểm tra','Áp dụng Có; triển khai Đầy đủ; có mã/link bằng chứng; kết quả Đạt; có người và ngày kiểm tra hợp lệ. Công thức chỉ kiểm tra dữ liệu khai báo, không xác thực nội dung tệp.'],
 ['Không áp dụng','Phải có lý do và phê duyệt tại cột S, người xác nhận và ngày. Không loại mục do chưa triển khai hoặc thiếu ngân sách.'],
 ['Phạm vi hai IDC','Bằng chứng phải bao phủ cả hai site. Nếu kiểm tra riêng, ghi rõ kết quả DC và DR trong mô tả/kho bằng chứng; chỉ hoàn tất khi cả hai đáp ứng phạm vi.'],
 ['Điểm TCVN','119 điểm kiểm tra phủ các tiểu mục đánh số Điều 6.1 đến 6.18 và A.4. Các ý a/b/c được diễn giải trong cùng dòng hoặc tách theo nội dung; đối chiếu đầy đủ bản tiêu chuẩn được cấp phép khi kết luận.'],
 ['Điểm Cloud','18 điểm bổ sung; CL-01 đến CL-08 là kiểm tra thiết kế XOR. CL-09 đến CL-18 có tham khảo dự thảo, mặc định chưa chốt áp dụng; không phải checklist đầy đủ để chứng nhận Hạng B hoặc Mức 4 của dự thảo.'],
 ['Bằng chứng','Một mã có thể liên kết nhiều kiểm soát. Ghi phạm vi, phiên bản, ngày, người lập/xác minh và đường dẫn kho được cấp quyền. Che bí mật và dữ liệu khách hàng không cần thiết.'],
 ['Mở rộng bảng','Có thể chèn dòng trong bảng và điền mã duy nhất. Khi mở rộng, sao chép công thức/validation từ dòng liền kề và cập nhật phạm vi tổng hợp; bản này tính trên tập dòng đã lập.'],
 ['Khả năng rủi ro','Thang nội bộ đề xuất: 1 hiếm; 2 ít khả năng; 3 có thể; 4 có khả năng cao; 5 thường xuyên. Ghi căn cứ từ lịch sử, phơi nhiễm và lỗ hổng.'],
 ['Tác động rủi ro','1 không đáng kể; 2 cục bộ dễ phục hồi; 3 ảnh hưởng đáng kể một dịch vụ/nhóm; 4 nghiêm trọng nhiều tenant/dữ liệu; 5 diện rộng hoặc hậu quả đặc biệt nghiêm trọng. Chấm mức cao nhất giữa bí mật, toàn vẹn, sẵn sàng, pháp lý và ảnh hưởng công cộng/xã hội/an ninh.'],
 ['Xếp loại nội bộ','Điểm = khả năng × tác động. 1–4 Thấp; 5–9 Trung bình; 10–16 Cao; 17–25 Rất cao. Chủ quản phải phê duyệt thang và cách xử lý; không thay tiêu chí Điều 14.'],
 ['RPO RTO MTD','BIA điền phút. RTO không vượt MTD. RPO phản ánh mất dữ liệu, không đồng nhất thời gian khôi phục; cần bằng chứng đo và mục tiêu theo từng dịch vụ.'],
 ['Phê duyệt cấp độ','Cấp độ 4 thông thường: ý kiến chuyên trách → Bộ Công an chủ trì thẩm định → chủ quản phê duyệt. Trường hợp quân sự/cơ yếu có thẩm quyền riêng. Công bố nội bộ không thay thủ tục này.'],
 ['Dữ liệu pháp nhân','Thông tin pháp nhân và nhân sự tham chiếu Word v0.9.4; đơn vị vận hành theo xác nhận của chủ quản là Khối Hạ tầng & Vận hành. Mã số doanh nghiệp, hồ sơ phân công và quyền ký vẫn cần xác minh trước trình ký.'],
 ];
 s.getRange(`A7:B${6+notes.length}`).values=notes;s.getRange(`A7:B${6+notes.length}`).format.wrapText=true;s.getRange(`A7:B${6+notes.length}`).format.rowHeight=72;s.getRange(`A7:B${6+notes.length}`).format.verticalAlignment='center';s.getRange(`A7:A${6+notes.length}`).format.font.bold=true;
 s.getRange('A27:E27').values=[['Mã','Nguồn','Vị trí tham chiếu','Liên kết hoặc bản nguồn','Ghi chú']];s.getRange('A28:E32').values=data.sources;s.getRange('A27:E32').format.wrapText=true;s.getRange('A27:E27').format={fill:'#FFFFFF',font:{name:'Times New Roman',size:11,bold:true,color:'#000000'},rowHeight:32};s.getRange('A28:E32').format.rowHeight=112;s.getRange('A27:E32').format.verticalAlignment='center';
 [28,95,55,65,75,16].forEach((w,i)=>s.getRange(`${col(i)}1:${col(i)}55`).format.columnWidth=w);
}
{
 const s=sheets['Tong hop'];s.showGridLines=false;s.tabColor='#666666';s.getRange('A1:H33').format.font={name:'Times New Roman',size:11,color:'#000000'};
 s.getRange('A2').values=[['Tiến độ rà soát XOR SECURE CLOUD']];s.getRange('A2').format.font={name:'Times New Roman',size:16,bold:true};s.getRange('A3').values=[['Ngày chốt']];s.getRange('B3').formulas=[["='Huong dan'!B4"]];s.getRange('B3').setNumberFormat('dd/mm/yyyy');
 s.getRange('A5:D5').values=[['Nhóm theo dõi','Số mục','Đủ hồ sơ','Còn cần xử lý']];
 s.getRange('A6:A9').values=[['TCVN cấp độ 4'],['Cloud bổ sung'],['Danh mục hồ sơ'],['Kiểm thử']];
 const records=[['TCVN','R',tcEnd,'Đủ hồ sơ kiểm tra'],['Cloud','R',cloudEnd,'Đủ hồ sơ kiểm tra'],['Ho so','M',data.dossier.length+5,'Đủ hồ sơ theo khai báo'],['Kiem thu','O',data.tests.length+5,'Đủ hồ sơ kiểm tra']];
 records.forEach(([name,c,end,good],i)=>{let r=6+i;s.getRange(`B${r}`).formulas=[[`=COUNTA('${name}'!$A$6:$A$${end})`]];s.getRange(`C${r}`).formulas=[[`=COUNTIF('${name}'!$${c}$6:$${c}$${end},"${good}")`]];s.getRange(`D${r}`).formulas=[[`=B${r}-C${r}${i<2?`-COUNTIF('${name}'!$${c}$6:$${c}$${end},"Không áp dụng đã duyệt")`:''}`]];});
 s.getRange('A12:C12').values=[['Trạng thái chi tiết','TCVN','Cloud']];
 const states=['Chưa đủ bằng chứng','Cần bổ sung triển khai','Thiếu bằng chứng','Chưa kiểm tra','Cần khắc phục','Chờ xác nhận','Chưa chốt phạm vi','Chờ duyệt không áp dụng','Không áp dụng đã duyệt','Đủ hồ sơ kiểm tra'];
 s.getRange('A13:A22').values=states.map(x=>[x]);
 states.forEach((_,i)=>{let r=i+13;s.getRange(`B${r}`).formulas=[[`=COUNTIF('TCVN'!$R$6:$R$${tcEnd},A${r})`]];s.getRange(`C${r}`).formulas=[[`=COUNTIF('Cloud'!$R$6:$R$${cloudEnd},A${r})`]];});
 s.getRange('A25').values=[['Bắt đầu tại TCVN và Ho so. Lọc trạng thái còn thiếu, điền người xử lý và hạn. Rà Cloud riêng sau khi chốt phần dự thảo áp dụng.']];
 s.getRange('A27').values=[['Số “Đủ hồ sơ” phản ánh khai báo đã có bằng chứng và kiểm tra; không phải tỷ lệ đạt chứng nhận hay quyết định phê duyệt cấp độ.']];
 for(const r of ['A5:D5','A12:C12'])s.getRange(r).format={fill:'#FFFFFF',font:{name:'Times New Roman',size:11,bold:true,color:'#000000'},rowHeight:34};
 s.getRange('A6:D9').format.rowHeight=34;s.getRange('A13:C22').format.rowHeight=29;
 [35,21,21,26,18,18,18,18].forEach((w,i)=>s.getRange(`${col(i)}1:${col(i)}33`).format.columnWidth=w);
}

// Monochrome table rules follow the user's PDF reference.
for(const r of ['A5:D9','A12:C22'])sheets['Tong hop'].getRange(r).format.borders={preset:'all',style:'thin',color:'#000000'};
for(const r of ['A5:D5','A12:C12'])sheets['Tong hop'].getRange(r).format.horizontalAlignment='center';
for(const r of ['A25:D26','A27:D28']){const q=sheets['Tong hop'].getRange(r);q.merge();q.format.wrapText=true;q.format.verticalAlignment='center';q.format.rowHeight=24;}
sheets['Huong dan'].getRange('A27:E32').format.borders={preset:'all',style:'thin',color:'#000000'};
// Kiểm tra các trường hợp có nguy cơ báo hoàn tất sai; khôi phục đầu vào sau phép thử.
const s=sheets.TCVN, saved=s.getRange('H6:S6').values;
const cases=[];
function state(){wb.recalculate();return s.getRange('R6').values[0][0];}
cases.push(['initial',state()]);
s.getRange('J6').values=[['Đầy đủ']];cases.push(['implemented_without_evidence',state()]);
s.getRange('K6').values=[['EV-TEST']];s.getRange('L6').values=[['Đạt']];cases.push(['missing_reviewer',state()]);
s.getRange('M6').values=[['Người thử']];s.getRange('N6').values=[[new Date('2026-10-17T00:00:00Z')]];cases.push(['complete',state()]);
s.getRange('I6').values=[['Không áp dụng']];cases.push(['na_unapproved',state()]);
s.getRange('S6').values=[['Lý do và số phê duyệt thử']];cases.push(['na_approved',state()]);
const expect=['Chưa đủ bằng chứng','Thiếu bằng chứng','Chờ xác nhận','Đủ hồ sơ kiểm tra','Chờ duyệt không áp dụng','Không áp dụng đã duyệt'];
cases.forEach((x,i)=>{if(x[1]!==expect[i])throw new Error('Status test '+JSON.stringify(x));});
s.getRange('H6:Q6').values=[saved[0].slice(0,10)];s.getRange('S6').values=[[saved[0][11]]];
wb.recalculate();
await fs.writeFile(path.join(tmp,'workbook-tests.json'),JSON.stringify(cases,null,2));
console.log((await wb.inspect({kind:'table',range:"'Tong hop'!A5:D9",include:'values,formulas',tableMaxRows:5,tableMaxCols:4,maxChars:4500})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'Final formula error scan',maxChars:2000})).ndjson);
await fs.mkdir(path.join(tmp,'xlsx-previews'),{recursive:true});
const views=[['Tong hop','A1:D23'],['TCVN','A5:D8'],['TCVN','H5:S8'],['Cloud','A5:D8'],['Cloud','H5:S8'],['Ho so','A5:F8'],['Ho so','G5:M8'],['Kiem thu','A5:H7'],['Kiem thu','I5:O8'],['BIA','A5:G8'],['BIA','H5:O8'],['Rui ro','A5:F8'],['Rui ro','G5:S8'],['Tai san','A5:H8'],['Tai san','I5:O8'],['Bang chung','A5:F8'],['Bang chung','G5:L8'],['Huong dan','A7:B12'],['Huong dan','A27:E29']];
for(let i=0;i<views.length;i++){
 const [sheetName,range]=views[i];const b=await wb.render({sheetName,range,scale:1.5,format:'png'});await fs.writeFile(path.join(tmp,'xlsx-previews',String(i+1).padStart(2,'0')+'.png'),new Uint8Array(await b.arrayBuffer()));
}
await fs.mkdir(out,{recursive:true});
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(out,'02_Checklist_ra_soat_XOR_cap_do_4.xlsx'));
console.log('Exported workbook');
