from pathlib import Path
P=Path(__file__).parent
ns={"__file__":str(P/"draw_inventory.py")}
exec((P.parent/'ho-so-v2-4/draw_topology.py').read_text().split('a=SVG()')[0],ns)
S=ns['SVG'];a=S(1600,950)
a.text(800,34,'CẤU TRÚC TÀI SẢN THEO KIỂM KÊ NGÀY 18/10/2026',28,True)
a.rect(30,75,1100,790,2)
a.text(580,113,'SITE CHÍNH — 13 THIẾT BỊ VẬT LÝ VÀ 45 MÁY ẢO',26,True)
a.text(580,144,'Đối chiếu DC Cầu Giấy theo phạm vi hồ sơ; vị trí rack/U cần xác nhận',22)
a.box(75,180,460,115,'02 FORTIGATE-500E • CỤM HA',['FG-01: FG5H0E5818904450','FG-02: FG5H0E5819903810'],22)
a.box(620,180,460,115,'02 CISCO N9K-C93180YC-EX',['Core 100: 10.3.99.100','Core 101: 10.3.99.101'],22)
a.text(580,336,'09 DELL POWEREDGE R630 • 324 NHÂN / 648 LUỒNG • RAM 2.336 GiB',23,True)
for x,title,lines in [
 (75,'03 HOST PROXMOX',['RAM 256 / 192 / 192 GiB','IP 10.3.99.151–153','21 VM • 166 vCPU / 340 GiB']),
 (415,'03 HOST COMPUTE',['RAM 288 / 512 / 512 GiB','IP 10.3.10.21–23','24 VM • 113 vCPU / 215,5 GiB']),
 (755,'03 HOST CEPH',['RAM 128 / 128 / 128 GiB','IP 10.3.31.31–33','10 OSD SSD • 19,20 TB raw'])]:a.box(x,375,325,155,title,lines,22)
# Containment links only; no unverified cabling or replication links.
a.path('M237 530 V570',arrow=False)
a.path('M577 530 V570',arrow=False)
a.path('M917 530 V570',arrow=False)
a.box(75,570,325,165,'VM ĐIỀU KHIỂN / HẠ TẦNG',['03 controller, mỗi VM:','24 vCPU / 48 GiB / 300G','18 VM hạ tầng khác','Controller đã nằm trong 21 VM'],21)
a.box(415,570,325,165,'PHÂN BỔ VM COMPUTE',['Compute-01: 10 VM','Compute-02: 0 VM','Compute-03: 14 VM','07 project có VM'],22)
a.box(755,570,325,165,'POOL LƯU TRỮ',['size 3 • min_size 2','.mgr / images / volumes','vms / backups','Không phải bản sao ngoài cụm'],22)
a.text(580,780,'Bond 10/25 Gb theo từng host; port map và tuyến cáp còn phải xác nhận.',22)
a.text(580,815,'VM controller dùng local-lvm; storage Proxmox liệt kê là không shared.',22)
a.rect(1170,75,400,410,2)
a.text(1370,113,'THÀNH PHẦN NGOÀI SITE',24,True)
a.box(1200,155,340,180,'01 VM KVM • mfa-02',['2 vCPU • RAM Linux 3,82 GiB','vda 80 GiB','Public: 103.252.74.40','Kênh riêng: 172.16.100.241'],22)
a.lines(1370,380,['Chưa xác nhận IDC đặt VM','và cấu hình host nhà cung cấp.','Chưa chứng minh cụm DR đầy đủ.'],22,30)
a.rect(1170,520,400,345)
a.text(1370,555,'CHƯA ĐỦ DỮ LIỆU KIỂM KÊ',23,True)
a.lines(1370,600,['SAN FC • S3 ngoài site','UPS / PDU / rack / ISP','Switch quản trị phụ trợ','Cụm phục hồi Nam Thăng Long'],23,34)
a.lines(1370,770,['Chưa tính vào tổng tài sản','đã xác định trong sơ đồ.'],22,30)
a.text(800,912,'Nguồn EV-001. Đường nối thể hiện quan hệ chứa tài nguyên; không thể hiện cáp mạng hoặc đồng bộ DC–DR.',22,italic=True)
ns['P']=P
a.save('03_Topo_hien_trang_kiem_ke.svg')
