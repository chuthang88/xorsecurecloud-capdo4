import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const base='/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud';
const tmp=base+'/tmp/ho-so-v2-5';
const before=base+'/output/XOR-Ho-so-CD4-v2.4/Bo-1-Ky-thuat/';
const out=base+'/output/XOR-Ho-so-CD4-v2.5/Bo-1-Ky-thuat/';
const data=JSON.parse(await fs.readFile(tmp+'/inventory-values.json','utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(before+'02_Checklist_ra_soat_XOR_cap_do_4.xlsx'));
const edits=[];
function set(sheet,cell,value){wb.worksheets.getItem(sheet).getRange(cell).values=[[value]];edits.push([sheet,cell,value]);}
function multiline(sheet,cell,value){set(sheet,cell,value);wb.worksheets.getItem(sheet).getRange(cell).format.wrapText=true;}
set('Huong dan','B4',new Date('2026-10-18T00:00:00Z'));
set('Huong dan','B8','Đã nhập EV-001 kiểm kê 18/10/2026: 13 thiết bị chính và 46 VM. Chưa có kết luận kiểm thử an ninh mạng; trạng thái kiểm soát tiếp tục chờ xác minh.');
const asset=wb.worksheets.getItem('Tai san');
asset.tables.items[0].rows.add(null,Array.from({length:43},()=>Array(15).fill(null)));
for(let row=22;row<=64;row++)asset.getRange(`A${row}:O${row}`).copyFrom(asset.getRange('A6:O6'),'all');
asset.getRange('A6:O64').values=data.assets.map(r=>r.map((v,i)=>i===13?'Cần xác minh':v));
asset.getRange('N6:N64').dataValidation={rule:{type:'list',values:['Chưa kiểm kê','Đã kiểm kê','Cần xác minh']}};
set('Tai san','A2','Danh mục tài sản theo kiểm kê ngày 18/10/2026');
set('Tai san','A3','59 bản ghi = 13 thiết bị chính + 46 VM theo EV-001; mã KK là mã hồ sơ. Các trường thiếu và vị trí ngoài site còn phải xác nhận.');
set('Tai san','B5','Nhóm tài sản');
asset.getRange('A6:O64').format.wrapText=true;
asset.getRange('A6:O64').format.autofitRows();
const ev=wb.worksheets.getItem('Bang chung');
set('Bang chung','A3','EV-001 là báo cáo đã nhận. H01–H06 chỉ được báo cáo dẫn nguồn, chưa nhận tệp gốc; không đánh dấu Đã xác minh khi chưa đối soát.');
const sourcePath='/Users/thangchu/Work/XOR/Xor Secure Cloud/'+data.source;
ev.getRange('B6:L6').values=[['TC-007; TC-009; TC-012; TC-028; TC-042; TC-059/060; TC-063; TC-070; TC-073; TC-076; HS01/02/11','Báo cáo kiểm kê hạ tầng 18/10/2026; 16 trang','Site chính và VM mfa-02 ngoài site','Báo cáo kiểm kê',sourcePath,data.sha256,new Date('2026-10-18T00:00:00Z'),'[CẦN ĐIỀN người thu]','[CẦN ĐIỀN người xác minh]','Nội bộ; chứa địa chỉ và cấu hình','Đã thu thập']];
const raw=[
 ['H01','infrastructure-hardware-inventory-20261018.txt.json','CPU/RAM, NIC/bond, storage và VM của 09 host'],
 ['H02','infrastructure-storage-detail-20261018.txt.json','PERC, Ceph OSD/pool và lưu trữ cục bộ'],
 ['H03','infrastructure-network-inventory-20261018.json','Model/serial switch và FortiGate'],
 ['H04','infrastructure-openstack-inventory-20261018.txt.json','VM, volume, image và project'],
 ['H05','infrastructure-dr-inventory-20261018.json','VM mfa-02 ngoài site'],
 ['H06','infrastructure-raid-search-20261018.txt.json','Phạm vi kiểm tra RAID trên 05 host còn thiếu']];
for(let i=0;i<raw.length;i++){
 const [code,file,title]=raw[i];const r=7+i;
 ev.getRange(`B${r}:L${r}`).values=[['Đối soát EV-001',code+' — '+title,'Theo phạm vi nguồn được dẫn','Tệp gốc chưa nhận','C:/XOR Secure/openstack-deployment/evidence/'+file,'[CẦN BỔ SUNG tệp và SHA-256]',null,null,null,'[CẦN XÁC ĐỊNH]','Chưa thu thập']];
}
ev.getRange('H6:H12').setNumberFormat('dd/mm/yyyy');ev.getRange('A6:L12').format.autofitRows();
for(const [code,[obs,gap]] of Object.entries(data.observations)){
 const r=Number(code.slice(3))+5;
 multiline('TCVN',`K${r}`,'EV-001; phụ lục 10. '+obs);
 multiline('TCVN',`O${r}`,gap+' Chưa kết luận đạt từ kiểm kê.');
 wb.worksheets.getItem('TCVN').getRange(`A${r}:S${r}`).format.autofitRows();
}
const cloud={
 7:['03 controller VM trên 03 Proxmox; mỗi VM 24 vCPU/48 GiB, local-lvm 300G.','Xác minh quorum DB/queue, HA VM, bản sao local disk và cụm DR.'],
 8:['Có VLAN/NIC VM và 24 VM thuộc 07 project; chưa kiểm tra ACL.','Kiểm tra VLAN 235 trunk 40, NIC trùng VLAN, forwarding và cách ly tenant.'],
 10:['26 volume, 2.387 GiB logic; Ceph size 3/min_size 2.','Kiểm thử quyền attach/detach, snapshot, mã hóa và xóa/tái cấp phát.'],
 13:['01 VM mfa-02 ngoài site; địa điểm vật lý chưa xác nhận.','Thu hợp đồng, địa chỉ IDC và đánh giá miền lỗi chung.'],
 15:['09 host, 02 Nexus, 02 FortiGate HA; bond 10/25 Gb; 03 VM controller.','Bổ sung DNS/IAM/queue, điện và thử mất thành phần.'],
 16:['Controller VM dùng local-lvm; storage Proxmox liệt kê không shared.','Lập phụ thuộc phục hồi, bản sao cấu hình/khóa và diễn tập cold start.'],
 19:['Có mfa-01 và mfa-02 trong danh mục; chưa kiểm tra cơ chế xác thực.','Xác nhận phạm vi MFA, yếu tố phần cứng nếu áp dụng và phép thử.'],
 22:['Có wazuh-01 và VM cysiem theo danh mục.','Xác minh log theo tenant, quyền xem/xóa và lưu độc lập.'],
 23:['Pool backups ghi 0,00 GB logic; S3 và cụm DR đầy đủ chưa kiểm kê.','Thu job backup, kho bất biến, bản sao ngoài cụm và diễn tập RPO/RTO.']};
for(const [r,[obs,gap]] of Object.entries(cloud)){
 multiline('Cloud',`K${r}`,'EV-001. '+obs);multiline('Cloud',`O${r}`,gap);wb.worksheets.getItem('Cloud').getRange(`A${r}:S${r}`).format.autofitRows();
}
const hs={6:'Đã bổ sung quy mô tài sản; còn pháp nhân, chức năng, số khách hàng, dữ liệu và phạm vi dịch vụ.',7:'Có cấu hình kiểm kê và sơ đồ tài sản; còn thiết kế phê duyệt, rack/cáp, route/rule và đối chiếu DR.',16:'Có 13 thiết bị, 46 VM; còn chủ tài sản, vòng đời, phụ trợ, phân loại dữ liệu và phần DR.',17:'Có bond/VLAN/NIC và hai phiên bản thiết bị; còn baseline, ACL, RBAC, TLS và phép thử.',18:'Có VM mang tên Wazuh/monitor/SIEM; chưa xác nhận nguồn log, retention, chức năng hoặc ca trực.',19:'Có Ceph replica và VM ngoài site; còn kho backup độc lập, job, RPO/RTO và diễn tập.',21:'Có serial thiết bị chính; còn hợp đồng, vị trí rack/U, điện/lạnh/PCCC và trách nhiệm IDC.'};
for(const [r,note] of Object.entries(hs)){
 set('Ho so',`G${r}`,'Một phần');multiline('Ho so',`H${r}`,'EV-001; tài liệu 10 (kiểm kê, chưa xác nhận đáp ứng).');multiline('Ho so',`K${r}`,note);wb.worksheets.getItem('Ho so').getRange(`A${r}:M${r}`).format.autofitRows();
}
const risks={
 6:['pam-01; mfa-01 trên Proxmox-01; mfa-02 ngoài site','Xác minh chính sách/PAM/MFA, quyền và phục hồi mfa-01 trên SSD-480GB RAID0.'],
 7:['24 VM compute/07 project; controller-03 và wazuh-01 nhiều NIC','Kiểm tra bridge/forwarding, VLAN 235 trunk 40, ACL và đường vượt ranh giới.'],
 8:['Ceph 03 host/10 OSD; pool backups; S3 chưa kiểm kê','Xác nhận bản sao độc lập và bất biến; thử restore; replica không thay backup.'],
 9:['13 thiết bị chính, 45 VM tại site chính; mfa-02 ngoài site','Xác định cụm DR, khả năng phục hồi control plane/storage/VM và RPO/RTO.'],
 10:['Kênh riêng 172.16.100.241 của mfa-02; liên site chưa đầy đủ','Thu tuyến, mã hóa, luồng đồng bộ, quorum/fencing và kiểm thử.'],
 11:['03 controller VM local-lvm; các VM IAM/PAM/MFA','Lập phụ thuộc, lưu khóa/cấu hình ngoài nền tảng và thử khởi động nguội.'],
 13:['KK-NET-01–04; bond các host; 02 FortiGate HA','Xác minh tuyến ISP, mapping cổng, state sync và kết quả failover.'],
 14:['wazuh-01; monitor-01; cysiem; network-detection-01','Đối chiếu nguồn log, quyền, retention, cảnh báo và ca trực.'],
 15:['DC Cầu Giấy; DR Nam Thăng Long; VM ngoài site chưa xác nhận IDC','Đánh giá điện, cáp, ISP và hợp đồng theo địa điểm thực tế.']};
for(const [r,[assets,action]] of Object.entries(risks)){
 set('Rui ro',`C${r}`,assets);multiline('Rui ro',`K${r}`,action);set('Rui ro',`M${r}`,'EV-001: kiểm kê; chưa xác nhận hiệu lực kiểm soát.');wb.worksheets.getItem('Rui ro').getRange(`A${r}:S${r}`).format.autofitRows();
}
wb.recalculate();
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:10},maxChars:1500})).ndjson);
await(await SpreadsheetFile.exportXlsx(wb)).save(out+'02_Checklist_ra_soat_XOR_cap_do_4.xlsx');
for(const [id,sheetName,range] of [['assets','Tai san','A5:H9'],['asset-detail','Tai san','L6:O8'],['dr','Tai san','A62:H64'],['evidence','Bang chung','A5:F7'],['controls','TCVN','J12:O12'],['cloud','Cloud','J7:O7'],['hs','Ho so','G6:K7'],['risks','Rui ro','K8:M9'],['summary','Tong hop','A3:D9'],['scope','Huong dan','A7:B9']]){
 const blob=await wb.render({sheetName,range,scale:1.15,format:'png'});await fs.writeFile(tmp+'/after-'+id+'.png',new Uint8Array(await blob.arrayBuffer()));
}
await fs.writeFile(tmp+'/xlsx-edit-log.json',JSON.stringify(edits,null,2));

const legacy=await SpreadsheetFile.importXlsx(await FileBlob.load(before+'04_Doi_soat_129_hang_muc_v094.xlsx'));
const ls=legacy.worksheets.getItem('Doi_soat');
const map={
 18:['13 thiết bị và 46 VM; controller là VM trên Proxmox. Đối soát lại thiết kế, không đóng tồn tại as-built từ inventory.','TC-007; HS02'],
 31:['Đã nhập IP, serial, cấu hình 13 thiết bị chính và 46 VM. Còn MAC/UUID, rack/U, owner, EOL và phụ trợ/DR.','TC-007; HS11'],
 33:['Có model/serial nhưng chưa có EOL/EOS và hợp đồng hỗ trợ.','TC-012; HS11'],
 35:['Có NX-OS/FortiOS và danh mục VM; còn SBOM, OS, hypervisor, phiên bản XOR và giấy phép.','TC-012'],
 46:['Có bond/VLAN/VM/storage; chưa có baseline hardening và báo cáo drift.','TC-028'],
 51:['Có mfa-01/02; cần xác minh cấu hình và phép thử bắt buộc MFA.','TC-073'],
 54:['Có pam-01, chưa xác minh JIT, ghi phiên và tách quyền.','TC-073'],
 60:['Có wazuh-01/cysiem; còn log nguồn, pipeline, retention và thử cảnh báo.','TC-042; TC-076'],
 68:['Ceph size 3/min_size 2 trong cụm; pool backups 0,00 GB logic; S3 ngoài site chưa kiểm kê.','TC-059; TC-060'],
 71:['Có VLAN/NIC và IP thiết bị; thêm VLAN 235 trunk 40, NIC untagged. Còn vùng Z, cáp, route/ACL.','TC-070; HS02'],
 72:['controller-03 nhiều NIC cùng VLAN và wazuh-01 đa mạng; kiểm tra forwarding/bridge/ACL, chưa kết luận vượt vùng.','TC-070; T01'],
 77:['Có 02 FortiGate HA, 02 Nexus; chưa có hai tuyến ISP và biên bản failover.','TC-063'],
 78:['Có bond LACP/active-backup, cổng 10/25 Gb; còn port map switch và thử mất đường.','TC-063; HS02'],
 96:['Đối chiếu cấu trúc 03 Proxmox/03 compute/03 Ceph và 46 VM; hoàn thiện as-built theo site/rack/cáp.','TC-007; HS02'],
 98:['03 controller VM, mỗi VM 24 vCPU/48 GiB, local-lvm 300G; cần xác minh quorum, HA và restore.','CL-02; T07'],
 100:['10 OSD SSD, 19,20 TB raw, size 3/min_size 2. Còn CRUSH, miền lỗi, tải và thử mất host.','CL-10; T07'],
 108:['VM compute phân bố 10/0/14; tổng 113 vCPU/215,5 GiB RAM cấp. Chưa chứng minh headroom hoặc dự phòng.','CL-10; T07'],
 130:['01 VM mfa-02 ngoài site; cần xác nhận IDC, cấu hình DR đầy đủ, hợp đồng, đồng bộ và diễn tập.','CL-08; CL-18; T09'],
 135:['324 nhân/648 luồng, RAM DIMM 2.336 GiB; Ceph raw 19,20 TB. Còn tải thực, overcommit và phép thử N+1.','CL-10; T07']};
for(const [r,[note,links]] of Object.entries(map)){
 ls.getRange(`I${r}`).values=[['EV-001 — kiểm kê 18/10/2026; phụ lục 10']];ls.getRange(`L${r}`).values=[[note]];ls.getRange(`M${r}`).values=[[links]];ls.getRange(`A${r}:N${r}`).format.autofitRows();
}
legacy.recalculate();
console.log((await legacy.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!',options:{useRegex:true,maxResults:10},maxChars:1000})).ndjson);
await(await SpreadsheetFile.exportXlsx(legacy)).save(out+'04_Doi_soat_129_hang_muc_v094.xlsx');
const b=await legacy.render({sheetName:'Doi_soat',range:'I96:N98',scale:1.1,format:'png'});await fs.writeFile(tmp+'/after-legacy.png',new Uint8Array(await b.arrayBuffer()));
await fs.writeFile(tmp+'/legacy-edited-rows.json',JSON.stringify(Object.keys(map).map(Number)));
console.log('Both workbooks updated; 59 inventory records; compliance verdicts preserved.');
