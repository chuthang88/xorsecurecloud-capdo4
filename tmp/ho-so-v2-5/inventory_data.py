from pathlib import Path
import json
P=Path(__file__).parent
SOURCE='Bao-cao-kiem-ke-ha-tang-he-thong-XOR-Secure-20261018.docx'
SOURCE_TITLE='Báo cáo kiểm kê hạ tầng hệ thống XOR Secure ngày 18/10/2026'
SHA='645d2ff7070da87a1b875204e04f22e2f8aa6bd0319ffade1fd324a9980b22ef'
T={x['index']:x['rows'] for x in json.loads((P/'source.json').read_text()) if x['type']=='table'}
REF='EV-001'
SCOPE='Theo EV-001, số liệu kiểm kê ngày 18/10/2026, khoảng 21:19–21:31 GMT+7. Site chính được đối chiếu với DC Cầu Giấy theo phạm vi hồ sơ; vị trí rack/U và địa điểm đặt VM mfa-02 ngoài site còn phải xác nhận.'
SUMMARY='13 thiết bị chính tại site chính gồm 09 Dell PowerEdge R630, 02 Cisco Nexus N9K-C93180YC-EX và 02 FortiGate-500E. Chín máy chủ có 18 socket, 324 nhân CPU, 648 luồng và 2.336 GiB RAM DIMM. Có 46 VM: 21 trên Proxmox, 24 trên cụm compute và 01 mfa-02 ngoài site.'
LIMIT='Báo cáo kiểm kê xác định tài sản và cấu hình tại thời điểm thu thập; chưa xác nhận hiệu lực kiểm soát an ninh mạng, khả năng chịu lỗi hoặc kết quả phục hồi.'
DR='Đã kiểm kê VM mfa-02 ngoài site: 2 vCPU, Linux đọc 3,82 GiB RAM, ổ vda 80 GiB; IP công khai 103.252.74.40, kết nối riêng 172.16.100.241. Chưa có bằng chứng về cụm phục hồi đầy đủ, đồng bộ dữ liệu và RPO/RTO; [CẦN XÁC NHẬN nhà cung cấp và địa điểm vật lý của VM, quan hệ với DR Nam Thăng Long].'
GAPS=[
 ('KK01','Vị trí và trách nhiệm','EV-001 có site chính và VM ngoài site; chưa có rack/U, chủ tài sản từng dòng, hợp đồng và địa chỉ đặt VM mfa-02.','Hạ tầng / IDC','Xác nhận site, rack/U, nguồn A/B, người quản lý và hợp đồng; bổ sung tài sản phụ trợ.'),
 ('KK02','RAID và ổ cục bộ','Chưa đọc PERC trực tiếp trên Proxmox-02/03 và Compute-01/02/03. SSD-480GB trên Proxmox-01 là một ổ RAID0, chứa ubuntu-93 và mfa-01.','Storage / Platform','Thu cấu hình RAID/ổ vật lý năm host; đánh giá bản sao và phục hồi hai VM trên ổ đơn, không suy RAID từ tên pool.'),
 ('KK03','Control plane và chịu lỗi','controller-01/02/03 là VM trên ba Proxmox, mỗi VM 24 vCPU, 48 GiB RAM, local-lvm 300G. Các storage Proxmox được liệt kê là không shared.','Platform','Xác minh quorum DB/queue, HA VM, bản sao local disk, cold start và thử mất host; chưa xác nhận N+1.'),
 ('KK04','Phân vùng và đường nối','Có VLAN 235 trunk 40; controller-03 có nhiều NIC cùng VLAN; wazuh-01 kết nối nhiều VLAN và một NIC untagged.','Network / SOC','Đối chiếu bridge, trunk, route, forwarding, ACL và sơ đồ cổng; kiểm thử cách ly, không kết luận vi phạm chỉ từ nhiều NIC.'),
 ('KK05','Lưu trữ và bản sao','Ceph 10 OSD, 19,20 TB raw, size 3/min_size 2; pool backups ghi 0,00 GB logic tại thời điểm đọc. SAN FC và S3 ngoài site chưa được kiểm kê đầy đủ.','Storage / Backup','Thu CRUSH, ngưỡng đầy, job backup, kho độc lập, mã hóa và restore; replica nội cụm không chứng minh sao lưu độc lập.'),
 ('KK06','DR và liên site','Báo cáo xác nhận một VM mfa-02 ngoài site; chưa xác nhận compute/storage/control plane tại DR.','SRE / IDC','Chốt năng lực DR, endpoint S3, tuyến và mã hóa liên site, hợp đồng, BIA và diễn tập chuyển đổi/chuyển về.'),
 ('KK07','Chức năng an ninh','Có VM mang tên pam-01, mfa-01/02, wazuh-01, prowler-01, network-detection-01 và các VM CyRadar.','IAM / SOC','Thu phiên bản, chính sách, nguồn log, độ phủ, quyền và phép thử từng chức năng; tên VM không chứng minh chức năng đã hoạt động.'),
 ('KK08','Năng lực và vòng đời','Compute-02 không có VM; VM compute phân bố 10/0/14. Chưa có tải thực, headroom, EOL/EOS hoặc bản dựng đầy đủ.','Platform / Capacity','Đối chiếu scheduler, tài nguyên dự phòng, tải thực và phép thử bảo trì; bổ sung SBOM, phiên bản, giấy phép và hạn hỗ trợ.')
]
# Observations do not change the compliance verdicts.
OBS={
 'TC-007':('13 thiết bị chính và 46 VM; có IP, serial và cấu hình trong phụ lục 10.','Bổ sung rack/U, chủ sở hữu, MAC, EOL/EOS, tài sản phụ trợ và phạm vi DR.'),
 'TC-009':('Có ảnh chụp kiểm kê ngày 18/10/2026; chưa có kết quả discovery toàn mạng.','Bổ sung phạm vi rà quét, đối soát chênh lệch và lịch sử định kỳ.'),
 'TC-012':('Đã ghi NX-OS 9.3(8), FortiOS 7.6.6 build3652; có danh mục VM.','Bổ sung OS, bản dựng XOR, hypervisor, agent, SBOM, giấy phép và EOL.'),
 'TC-028':('Có thông số bond, VLAN, storage và cấu hình VM tại ngày kiểm kê.','Đối chiếu baseline được duyệt, hardening và báo cáo sai lệch.'),
 'TC-042':('Kiểm kê có wazuh-01, monitor-01 và VM cysiem; chưa kiểm tra bên trong guest.','Xác minh nguồn log, NTP, TLS, thu tập trung và thử cảnh báo.'),
 'TC-059':('Ceph dùng size 3/min_size 2 trong cùng cụm; S3 ngoài site chưa kiểm kê.','Xác nhận sơ đồ bản sao độc lập, mã hóa và phép thử phục hồi.'),
 'TC-060':('Pool backups trong Ceph ghi 0,00 GB logic; chưa xác nhận repository ngoài cụm.','Bổ sung kho sao lưu độc lập, versioning, quyền xóa và dữ liệu thực tế.'),
 'TC-063':('Có 02 Nexus, 02 FortiGate trong HA và bond 10/25 Gb theo từng host.','Xác minh port map, ISP/tuyến độc lập, state sync và biên bản failover.'),
 'TC-070':('Đã ghi nhận VLAN/NIC của VM và IP iDRAC; có VLAN 235 trunk 40.','Chốt ánh xạ vùng, bridge/route/ACL và kiểm thử cách ly liên vùng.'),
 'TC-073':('Có pam-01, mfa-01 trên Proxmox và mfa-02 ngoài site.','Xác nhận luồng quản trị, MFA bắt buộc, ghi phiên và thử từ chối.'),
 'TC-076':('Có monitor-01, wazuh-01 và các VM an ninh trong danh mục.','Bổ sung bằng chứng chức năng, độ phủ, ca trực 24/7 và xử lý sự kiện.')
}
ASSETS=[]
def asset(aid,group,name,site,zone,ip,serial,version,note):
 ASSETS.append([aid,group,name,site,zone,ip,serial,version,'[CẦN XÁC NHẬN]','[CẦN PHÂN LOẠI]','[CẦN ĐÁNH GIÁ]','[CẦN ĐIỀN]',REF,'Đã ghi nhận từ báo cáo',note])
for i,r in enumerate(T[1][1:]):
 group='Máy chủ Proxmox' if i<3 else 'Máy chủ compute' if i<6 else 'Máy chủ Ceph'
 asset(f'KK-SRV-{i+1:02}',group,r[0],'Site chính / DC Cầu Giấy','[CẦN ÁNH XẠ]',r[1],r[2],'[CẦN ĐIỀN]',f'Dell R630; 2 × {r[3]}; 36 nhân/72 luồng; RAM {r[4]} GiB; iDRAC {T[3][i+1][5]}. EV-001 tr.2–3; rack/U cần xác nhận.')
for i,r in enumerate(T[4][1:]):
 asset(f'KK-NET-{i+1:02}','Switch' if i<2 else 'Firewall',r[0],'Site chính / DC Cầu Giấy','[CẦN ÁNH XẠ]',r[1],r[3],r[4],r[2]+'; EV-001 tr.4. Cổng/nguồn A/B và hiệu lực HA cần kiểm tra.')
for ti in [13,14,15]:
 host=f'Proxmox-{ti-12:02}'
 for r in T[ti][1:]:
  asset('KK-PVE-'+r[0],'VM hạ tầng',r[1],'Site chính / '+host,'[CẦN ÁNH XẠ]','[CẦN ĐIỀN IP guest]','VMID '+r[0],'[CẦN ĐIỀN]',f'{r[2]} vCPU; {r[3]} GiB RAM; {r[4]}; {r[5]}. EV-001 tr.{ti-4}; cấu hình từ hypervisor, chưa kiểm tra guest.')
for i,r in enumerate(T[16][1:]+T[17][1:],1):
 asset(f'KK-VM-{i:02}','VM trên compute',r[0],'Site chính / '+r[2],'Project '+r[1],r[5],'[CẦN ĐIỀN UUID VM]','[CẦN ĐIỀN]',f'{r[3]} vCPU; {r[4]} GiB RAM. IP từ control plane; EV-001 tr.{12 if i<=12 else 13}. Chủ thể và ranh giới quản lý cần xác nhận.')
asset('KK-DR-01','VM ngoài site','mfa-02','Ngoài site; [CẦN XÁC NHẬN IDC]','[CẦN ÁNH XẠ]','103.252.74.40; 172.16.100.241','[CẦN ĐIỀN UUID VM]','[CẦN ĐIỀN]','KVM; 2 vCPU; RAM Linux 3,82 GiB; vda 80 GiB. EV-001 tr.15; chưa biết cấu hình host nhà cung cấp.')
assert len(ASSETS)==59
assert sum(int(r[4]) for r in T[1][1:])==2336
assert sum(int(r[2]) for ti in [13,14,15] for r in T[ti][1:])==166
assert sum(float(r[4]) for ti in [16,17] for r in T[ti][1:])==215.5
if __name__=='__main__':
 (P/'inventory-values.json').write_text(json.dumps({'assets':ASSETS,'observations':OBS,'gaps':GAPS,'source':SOURCE,'sha256':SHA},ensure_ascii=False,indent=2))
