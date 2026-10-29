d=Doc('Phụ lục thiết kế và hiện trạng hệ thống')
d.cover('Hiện trạng kiểm kê ngày 18 tháng 10 năm 2026')
d.h('1 Phạm vi và số liệu tổng hợp')
d.p(SCOPE)
d.p(SUMMARY)
d.table(['Nhóm','Số lượng','Thông số ghi nhận'],[
 ('Proxmox vật lý','03','108 nhân/216 luồng; 640 GiB RAM DIMM; 21 VM, gồm 03 controller.'),
 ('Compute vật lý','03','108 nhân/216 luồng; 1.312 GiB RAM DIMM; 24 VM.'),
 ('Ceph vật lý','03','108 nhân/216 luồng; 384 GiB RAM DIMM; 10 OSD SSD, 19,20 TB raw.'),
 ('Mạng và firewall','04','02 Nexus và 02 FortiGate-500E trong cụm HA.'),
 ('VM ngoài site','01','mfa-02; 2 vCPU; Linux đọc 3,82 GiB RAM; vda 80 GiB.')],[1.2,.55,2.8])
d.p('Nguồn: '+SOURCE_TITLE+' (EV-001), tr.1–2 và 15. '+LIMIT)
d.p('GiB/TiB dùng cơ số 1024; GB/TB dùng cơ số 1000. CPU vật lý, vCPU cấp phát, RAM DIMM, RAM VM và RAM Linux đọc được là các chỉ tiêu riêng. Dung lượng Ceph, pool, volume và ổ VM không được cộng trùng.')
d.p('[CẦN ĐIỀN số biên bản, người lập, người kiểm tra và người xác nhận hiện trạng; tên, số và ngày văn bản phê duyệt thiết kế].')

d.page('2 Máy chủ vật lý và quản trị phần cứng')
d.p('Chín máy chủ đều là Dell PowerEdge R630; mỗi máy có 02 socket, 36 nhân và 72 luồng. Service tag và địa chỉ quản trị được ghi theo EV-001, tr.2–3. iDRAC thuộc cùng chassis, không phải thiết bị máy chủ bổ sung.')
d.table(['Mã / máy chủ','IP / iDRAC','Service tag','CPU mỗi socket','RAM GiB'],[
 (f'KK-SRV-{i:02}\n'+r[0],r[1]+'\n'+T[3][i][5],r[2],r[3],r[4]) for i,r in enumerate(T[1][1:],1)],[1.15,1.2,1,.95,.65])
d.h('Thông tin vị trí và vòng đời')
d.p('Site chính được đối chiếu DC Cầu Giấy theo phạm vi hồ sơ. [CẦN ĐIỀN phòng máy, rack/U, chủ sở hữu và người quản lý từng máy; nguồn A/B; firmware/OS/hypervisor; hạn hỗ trợ, hợp đồng bảo trì và biên bản nghiệm thu].')
d.p('DIMM lắp đặt theo nhóm Proxmox: 8/6/6 thanh 32 GB; compute: 9/16/16 thanh 32 GB; Ceph: 4/4/4 thanh 32 GB. Tổng quy đổi theo báo cáo: 2.336 GiB.')

d.page('3 Thiết bị mạng và tường lửa')
d.table(['Mã / thiết bị','Địa chỉ truy cập','Model / serial','Phiên bản'],[
 (f'KK-NET-{i:02}\n'+r[0],r[1],r[2]+'\n'+r[3],r[4]) for i,r in enumerate(T[4][1:],1)],[.9,1.25,1.7,1.1])
d.p('Nguồn: EV-001, tr.4. Hai Nexus cùng hiển thị hostname “switch”; hồ sơ phân biệt bằng IP và serial. FG-01/02 được báo cáo trong cụm HA; trạng thái HA không thay thế biên bản thử chuyển đổi.')
d.table(T[5][0],T[5][1:],[1.15,1,1,1.8])
d.p('Số cổng là cấu hình danh định, chưa xác nhận tất cả đã lắp module hoặc đang sử dụng. [CẦN ĐIỀN port map, nhãn cáp, peer/keepalive, thiết bị ISP, license/support, tuyến độc lập và kết quả thử mất thiết bị/mất tuyến].')
d.p('Thiết bị phụ trợ chưa có danh mục đầy đủ: switch quản trị phụ trợ, ODF/patch panel, UPS, PDU, thiết bị ISP, rack và SAN ngoài hệ thống. Các thành phần này chưa được cộng vào tổng 13 chassis.')

d.page('4 Kết nối mạng máy chủ')
d.p('Nguồn: EV-001, tr.5. Tốc độ dưới đây là tốc độ mỗi cổng thành viên; không phải tốc độ bảo đảm của một phiên truyền. Bảng không thay thế sơ đồ cáp có số cổng switch và nhãn dây.')
rows=[]
for i in range(1,len(T[6]),2):
 r1,r2=T[6][i:i+2]
 modes='\n'.join(r[1]+': '+r[2].replace('fault-tolerance (active-backup)','active-backup') for r in [r1,r2])
 ports='\n'.join(r[1]+': '+r[3].replace('25000 Mbps','25 Gb').replace('10000 Mbps','10 Gb').replace('\n','; ') for r in [r1,r2])
 rows.append([r1[0],modes,ports])
d.table(['Máy chủ','Bond và chế độ','Cổng thành viên và tốc độ'],rows,[1,1.35,3.2])
d.p('[CẦN ĐIỀN cổng đích, port-channel, MTU, nhánh A/B, VLAN được phép và kết quả thử chuyển đổi đường truyền].')

d.page('5 Lưu trữ tập trung Ceph')
d.table(T[7][0],T[7][1:],[.9,.4,1.3,.6,1.4])
d.table(T[8][0],T[8][1:],[1.4,2.5])
d.table(T[9][0],T[9][1:],[.8,.55,1,1,1])
d.p('Nguồn: EV-001, tr.6. MAX AVAIL 5,02 TB là ước lượng dung lượng logic có thể ghi thêm theo điều kiện pool tại thời điểm đọc; các pool dùng chung cụm nên không cộng các giá trị này. Raw sử dụng/còn lại là số đã làm tròn trong báo cáo.')
d.p('Cấu hình size 3/min_size 2 chưa xác nhận độc lập miền lỗi hoặc bản sao ngoài cụm. [CẦN ĐIỀN CRUSH map, ngưỡng đầy, mã hóa, tải/IOPS, bản sao độc lập và kết quả phục hồi].')

d.page('6 Ổ cục bộ và mức RAID đã kiểm kê')
d.table(T[10][0],T[10][1:],[.9,1.65,.6,2.1])
d.p('Nguồn: EV-001, tr.7. Proxmox-01 có 07 ổ vật lý: 02 SSD SATA 480 GB RAID1, 02 SSD SAS 400 GB RAID1, 02 HDD SAS 600 GB RAID1 và 01 SSD SATA Intel 480 GB trình bày qua RAID0. Mỗi Ceph có 02 SSD 480 GB RAID1 cho OS; OSD 1,92 TB ở chế độ JBOD, phân bố 4/3/3.')
d.p('Chưa đọc trực tiếp cấu hình RAID và bay trên Proxmox-02/03 và Compute-01/02/03. Không có bằng chứng SAN FC gắn với 09 host trong dữ liệu đã thu. [CẦN ĐIỀN cấu hình PERC/iDRAC còn thiếu; model/serial, giao thức và dung lượng SAN nếu thuộc phạm vi].')

d.page('7 Kho lưu trữ cục bộ trên Proxmox')
d.table(T[12][0],T[12][1:],[.95,.9,.7,.6,.6,.6,.6])
d.p('Nguồn: EV-001, tr.8; đơn vị GiB. Chỉ ghi storage có dung lượng lớn hơn 0 tại thời điểm đọc. Các storage liệt kê đều không shared; local và local-lvm có thể cùng nằm trên một RAID đã chia vùng. Không cộng các lớp này với dung lượng đĩa vật lý.')
d.p('Tên SSD/HDD là tên storage cấu hình, không tự xác nhận loại ổ hoặc RAID khi chưa đọc PERC. Kích thước ổ VM là dung lượng cấp phát logic; lượng ghi thực tế được theo dõi riêng.')

for ti in [13,14,15]:
 host=ti-12
 d.page(f'{host+7} Máy ảo hạ tầng trên Proxmox {host:02}')
 d.p(f'Nguồn: EV-001, tr.{ti-4}. Host Proxmox-{host:02}; số VM {len(T[ti])-1}. VMID 100/101/102 là ba controller, đã nằm trong tổng 21 VM Proxmox.')
 rows=[]
 for r in T[ti][1:]:rows.append([r[0]+'\n'+r[1],r[2]+' vCPU\n'+r[3]+' GiB',r[4].replace('scsi0: ',''),r[5]])
 d.table(['VMID / tên VM','CPU / RAM','Ổ VM cấu hình','NIC bridge và VLAN'],rows,[1.45,.75,1,2.3])
 d.p('Cấu hình được đọc từ hypervisor, chưa xác nhận bên trong guest. NIC untagged chưa xác định VLAN tại bridge/switch. [CẦN ĐIỀN IP guest, OS/phiên bản, chủ dịch vụ và trạng thái chức năng].')

for ti in [16,17]:
 d.page(f'{ti-5} Máy ảo trên cụm compute phần {ti-15}')
 rows=[]
 for offset,r in enumerate(T[ti][1:],1):
  idx=(ti-16)*12+offset
  rows.append([f'KK-VM-{idx:02}\n'+r[0],r[1]+'\n'+r[2],r[3]+' / '+r[4],r[5]])
 d.table(['Mã / tên VM','Project / compute','vCPU / GiB','IP cấu hình'],rows,[1.7,1.4,.65,1.4])
 d.p(f'Nguồn: EV-001, tr.{ti-4}. IP là bản ghi control plane, chưa xác nhận cấu hình trong guest. Project rút gọn xscs-78954c30… có ID d94cc6fbf4e54f919f24d54ef018e4b9. [CẦN ĐIỀN UUID VM, chủ sở hữu, OS/phiên bản và ranh giới trách nhiệm].')

d.page('13 Tài nguyên ảo và thành phần ngoài site')
d.table(T[18][0],T[18][1:],[1.2,.6,1,1])
d.p('Cụm compute có 24 VM, 113 vCPU và 215,5 GiB RAM cấp phát; compute-02 có 0 VM tại thời điểm đọc. Có 12 project trong danh mục định danh, 07 project có VM; 19 image; 26 volume thuộc loại __DEFAULT__, tổng 2.387 GiB logic. Nguồn: EV-001, tr.12–14.')
d.h('VM ngoài site')
d.table(T[22][0],T[22][1:],[1,3])
d.p('Nguồn: EV-001, tr.15. [CẦN XÁC NHẬN nhà cung cấp, địa chỉ IDC đặt mfa-02 và quan hệ với DR Nam Thăng Long; CẦN ĐIỀN hợp đồng, host vật lý, miền lỗi và kết quả chuyển đổi]. SAN FC và S3 ngoài site chưa có cấu hình đầy đủ để đưa vào tổng thiết bị đã kiểm kê.')

d.page('14 Phân vùng và đối chiếu hiện trạng')
d.table(['Phân đoạn','Ghi nhận kiểm kê','Thông tin còn phải xác nhận'],[
 ('VLAN 10/20/30/31/40/100','Có trong cấu hình NIC controller; wazuh-01 kết nối nhiều VLAN.','Chức năng theo vùng Z, CIDR/gateway, bridge/route, forwarding và ACL.'),
 ('VLAN 70','Nhiều VM hạ tầng dùng vmbr3 tag 70, gồm PAM, MFA và monitor.','Ranh giới quản trị/API; quyền và luồng liên vùng.'),
 ('VLAN 235 trunk 40','controller-01/02 dùng vmbr1; controller-03 dùng vmbr2.','Vai trò provider/external, VLAN trunk được phép và kiểm thử cách ly.'),
 ('Untagged','net0 trên các controller; net7 trên wazuh-01.','PVID/native VLAN và ánh xạ bridge/switch.'),
 ('Quản trị 10.3.99.x','IP Proxmox, Nexus và iDRAC theo bảng thiết bị.','CIDR, VLAN/VRF thực tế, gateway, ACL và đường PAM; chưa suy VLAN 99 từ IP.'),
 ('Ngoài site','mfa-02: 103.252.74.40; 172.16.100.241.','Loại kênh riêng, route, mã hóa, port dịch vụ và chính sách nguồn.')],[1,1.8,2])
d.p('Bảng thể hiện cấu hình đã ghi nhận, chưa xác nhận luồng nào đã được phê duyệt. [CẦN ĐIỀN ma trận PL04 gồm nguồn, đích, chiều, cổng/giao thức, rule ID, chủ thể phê duyệt và kết quả thử cho phép/từ chối].')
d.p('Đối với controller-03, nhiều NIC cùng số VLAN xuất hiện trên vmbr2/vmbr3; đối với wazuh-01, cần xác nhận cơ chế thu thập và việc chuyển tiếp giữa các NIC. Hiện trạng nhiều NIC chưa đủ căn cứ kết luận có hoặc không có đường vượt ranh giới.')

d.page('15 Hồ sơ xác nhận và phần còn thiếu')
d.table(['Nội dung','Tình trạng hồ sơ'],[
 ('Danh mục tài sản','Đã có 13 thiết bị và 46 VM tại EV-001. [CẦN ĐIỀN MAC/UUID, chủ tài sản, rack/U, EOL/EOS và tài sản phụ trợ].'),
 ('Thiết kế và phê duyệt','[CẦN ĐIỀN số, ngày hồ sơ thiết kế được duyệt; đối chiếu thay đổi controller VM, RAM và SAN với thiết kế cũ].'),
 ('Chức năng bảo vệ','Có VM mang tên PAM/MFA/Wazuh và các thành phần an ninh; [CẦN ĐIỀN cấu hình, giấy phép, độ phủ, log và kết quả kiểm thử].'),
 ('Sao lưu và DR','[CẦN ĐIỀN kho độc lập, S3, dữ liệu đồng bộ, cấu hình DR đầy đủ, BIA, RPO/RTO và biên bản diễn tập].'),
 ('An toàn vật lý','[CẦN ĐIỀN hồ sơ hai IDC, hợp đồng/SLA, UPS/PDU, điện A/B, PCCC, kiểm soát ra vào và kết quả kiểm tra].'),
 ('Xác nhận số liệu','[CẦN ĐIỀN người lập/kiểm tra, số biên bản, ngày và người ký xác nhận].')],[1.1,3.1])
d.h('Tài liệu kiểm kê')
d.p('EV-001: '+SOURCE_TITLE+', 16 trang; tên tệp '+SOURCE+'.')
d.p('SHA-256: '+SHA)
d.p('Nguồn H01–H06 được EV-001 dẫn gồm dữ liệu phần cứng, lưu trữ, thiết bị mạng, tài nguyên cloud, VM ngoài site và phạm vi đọc RAID. [CẦN BỔ SUNG tệp gốc, hash, người thu và biên bản đối soát].')

sec=d.doc.add_section(WD_SECTION_START.NEW_PAGE)
sec.page_width=Cm(29.7);sec.page_height=Cm(21);sec.orientation=1
sec.left_margin=sec.right_margin=Cm(2);sec.top_margin=sec.bottom_margin=Cm(1.5)
for x in list(sec._sectPr.findall(qn('w:pgNumType'))):sec._sectPr.remove(x)
d.h('16 Sơ đồ cấu trúc tài sản theo kiểm kê')
p=d.p();p.paragraph_format.line_spacing=1;p.paragraph_format.space_after=Pt(0)
p.add_run().add_picture(str(TMP/'03_Topo_hien_trang_kiem_ke.png'),width=Cm(25.3))
d.p('Hình 3. Cấu trúc tài sản được ghi nhận ngày 18/10/2026 theo EV-001.',style='Caption')
d.save(ADMIN/'10_Phu_luc_thiet_ke_va_hien_trang.docx')
