d=Doc('Phụ lục thiết kế và hiện trạng hệ thống')
d.cover('Kèm theo hồ sơ đề xuất cấp độ 4 hệ thống XOR SECURE CLOUD')
d.h('1. Thông tin hệ thống')
d.table(['Nội dung','Thông tin'],[
 ('Tên hệ thống','XOR SECURE CLOUD; nền tảng XOR STACK CLOUD.'),
 ('Chủ quản và đơn vị vận hành',ORG+'; '+OPERATOR+'.'),
 ('Phạm vi','Toàn bộ nền tảng cloud và các dịch vụ quản trị chung. Ranh giới với phần khách hàng quản lý được xác định theo hợp đồng và ma trận trách nhiệm.'),
 ('Địa điểm','DC: Trung tâm Hạ tầng IDC Cầu Giấy. DR: Trung tâm Hạ tầng IDC Nam Thăng Long.'),
 ('Hồ sơ thiết kế','[CẦN ĐIỀN tên, số, ngày, phiên bản và văn bản phê duyệt]'),
 ('Thời điểm chốt hiện trạng','[CẦN ĐIỀN ngày, người kiểm kê/xác nhận và biên bản]')],[1,3])
d.h('2. Thông số thiết kế hạ tầng')
d.table(['Thành phần','Thông số thiết kế','Hiện trạng và bằng chứng'],[
 ('Máy chủ','09 Dell R630: 03 Controller, 03 Compute KVM, 03 Ceph SSD.','[CẦN ĐIỀN số lượng theo site; serial; cấu hình; vai trò; phiên bản; mã EV]'),
 ('Bộ nhớ','2.304 GB RAM theo cấu hình các vai trò.','[CẦN ĐIỀN bộ nhớ khả dụng, dự phòng, năng lực chịu lỗi và mã EV]'),
 ('Lưu trữ','Ceph SSD: 19,2 TB dung lượng thô; SAN: 14,4 TB dung lượng thô; 18 ổ OS 480 GB.','[CẦN ĐIỀN dung lượng sử dụng, replica/RAID, backend, mã hóa và kết quả phục hồi]'),
 ('Mạng và bảo vệ biên','02 Nexus N9K-C93180YC-EX; 02 FortiGate 500E; 01 switch SAN; 01 Access.','[CẦN ĐIỀN phân bổ theo site, port map, dự phòng, giấy phép, hỗ trợ và kết quả chịu lỗi]'),
 ('Kết nối liên trung tâm','Kết nối DC Cầu Giấy – DR Nam Thăng Long.','[CẦN ĐIỀN nhà mạng, tuyến, băng thông, mã hóa, độ trễ và cơ chế đồng bộ]')],[1,1.65,2.1])
d.p('[CẦN XÁC NHẬN phạm vi của bảng cấu hình: một site hoặc toàn hệ thống; phân bổ thiết bị tại DC/DR; sai khác giữa thiết kế và hiện trạng; biên bản nghiệm thu].')
d.page('3. Phân vùng và luồng thông tin')
d.table(['VLAN thiết kế','Chức năng','Thông tin triển khai'],[
 ('10','Dịch vụ điều khiển nội bộ','[CẦN ĐIỀN site, VLAN/VRF/CIDR, gateway, owner, vùng Z và mã rule]'),
 ('20','Transport cho mạng tenant','[CẦN ĐIỀN underlay/overlay, VNI, MTU, chính sách cách ly và mã EV]'),
 ('30','Lưu trữ Ceph client','[CẦN ĐIỀN mạng I/O, client được phép, ACL và mã EV]'),
 ('31','Lưu trữ Ceph cluster','[CẦN ĐIỀN mạng đồng bộ, recovery, heartbeat và mã EV]'),
 ('40','Quản trị và an ninh','[CẦN ĐIỀN phân khu PAM, SIEM, sao lưu, kho log và quyền quản trị]'),
 ('70','API nội bộ XOR STACK CLOUD','[CẦN ĐIỀN endpoint, TLS, danh tính, quyền, audit và mã EV]'),
 ('99','Quản trị ngoài băng','[CẦN ĐIỀN BMC/console, điểm truy cập qua PAM và ACL]'),
 ('100','DMZ và cổng thông tin','[CẦN ĐIỀN endpoint, WAF/LB, origin, luồng API và mã EV]'),
 ('[CẦN ĐIỀN]','Provider/external và SAN','[CẦN ĐIỀN VLAN/VRF, gateway, giao thức, zoning/multipath]')],[.65,1.35,2.3])
d.p('Hồ sơ luồng kết nối: [CẦN ĐIỀN mã PL04, nguồn, đích, chiều khởi tạo, cổng/giao thức, mục đích, biện pháp kiểm soát, rule ID, người phê duyệt và bằng chứng thử cho phép/từ chối].')
d.h('4. Phạm vi dịch vụ')
d.table(['Nhóm dịch vụ','Thành phần','Trạng thái và phạm vi triển khai'],[
 ('Tính toán và mạng','VM, image, flavor, volume, mạng riêng, router, SG, floating IP, cân bằng tải.','[CẦN ĐIỀN dịch vụ, phiên bản, site, trạng thái và mã EV]'),
 ('Quản trị chung','Portal/API, định danh, quota, usage/billing, CMDB, giám sát, nhật ký, hỗ trợ.','[CẦN ĐIỀN thành phần, trách nhiệm, trạng thái và mã EV]'),
 ('Dữ liệu và sao lưu','Backend, snapshot, backup, cấu hình và khóa phục hồi.','[CẦN ĐIỀN dữ liệu, vị trí, thời hạn lưu, quyền và mã EV]'),
 ('Dịch vụ mở rộng','Kubernetes, GPU, S3, cơ sở dữ liệu quản trị và các dịch vụ khác.','[CẦN XÁC NHẬN đã triển khai, dự kiến hoặc không thuộc phạm vi; mã EV]')],[1,1.8,1.6])
d.page('5. Phân bổ tại DC và DR')
d.table(['Địa điểm','Vai trò','Hồ sơ hiện trạng'],[
 ('Trung tâm Hạ tầng IDC Cầu Giấy','DC chính','[CẦN ĐIỀN địa chỉ chi tiết, hợp đồng/SLA, rack/điện/lạnh, thiết bị, kết nối, kiểm soát vật lý và mã EV]'),
 ('Trung tâm Hạ tầng IDC Nam Thăng Long','DR','[CẦN ĐIỀN cấu hình phục hồi, dữ liệu đồng bộ, tài khoản/khóa, hồ sơ IDC, kết quả chuyển đổi/chuyển về và mã EV]')],[1.3,.55,2.8])
d.p('Chỉ tiêu phục hồi: [CẦN ĐIỀN mã dịch vụ, RPO/RTO/MTD được duyệt, kết quả đo, ngày thử và người xác nhận]. Thứ tự phục hồi và phụ thuộc: [CẦN ĐIỀN mạng, thời gian, DNS, IAM, KMS, lưu trữ, cơ sở dữ liệu, hàng đợi, API và workload].')
d.h('6. Danh mục hồ sơ xác nhận')
d.table(['Mã','Tài liệu','Đơn vị chủ trì','Mã EV / phiên bản'],[
 ('XN01','BOM theo site; serial; rack; port; nguồn điện A/B.','Hạ tầng / IDC','[CẦN ĐIỀN]'),
 ('XN02','Inventory nền tảng, bản dựng XOR, SBOM, cấu hình.','Platform','[CẦN ĐIỀN]'),
 ('XN03','VLAN/VRF/IP, rule liên vùng, OOB, kết nối hai site.','Network','[CẦN ĐIỀN]'),
 ('XN04','Backend, mã hóa, khóa, dung lượng và chịu lỗi.','Storage / IAM','[CẦN ĐIỀN]'),
 ('XN05','Quét lỗ hổng, kiểm thử, kiểm tra lại và thay đổi.','Chuyên trách ANM','[CẦN ĐIỀN]'),
 ('XN06','BIA, sao lưu/phục hồi, diễn tập DR và RPO/RTO.','Vận hành','[CẦN ĐIỀN]'),
 ('XN07','Pháp nhân, phân công, thẩm quyền ký, liên hệ.','Chủ quản / pháp chế','[CẦN ĐIỀN]')],[.5,2.2,1.15,1.1])
d.p('Đơn vị lập: '+OPERATOR+'. Người lập: [CẦN ĐIỀN]. Người kiểm tra: [CẦN ĐIỀN]. Văn bản xác nhận: [CẦN ĐIỀN số, ngày, người ký].')
d.save(ADMIN/'10_Phu_luc_thiet_ke_va_hien_trang.docx')
