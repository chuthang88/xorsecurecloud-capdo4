import collections

legacy=json.loads((TMP/'source-controls.json').read_text())
source_name='XOR_SECURE_CLOUD_Ho_so_Cap_do_4_v0.9.4.docx'
bom=[
 ('Controller','03 Dell R630','128 GB RAM/node; 2 × 480 GB OS và 2 × 800 GB/node; máy 1–2 kiêm SEED.','Chốt vai trò ổ 800 GB, NIC 10/25 Gb, placement và inventory.'),
 ('Compute','03 Dell R630','512 GB RAM/node; 2 × 480 GB OS/node; máy 4–6.','Chốt gateway/agent đồng vị trí, uplink và năng lực khi mất một host.'),
 ('Ceph SSD','03 Dell R630','128 GB RAM/node; 10 ổ 1,92 TB phân bố 4/3/3; 19,2 TB raw.','Chốt CRUSH, replica, dung lượng sử dụng và thử recovery.'),
 ('SAN','01 chưa rõ model','24 ổ 600 GB SAS; 14,4 TB raw; backend riêng.','Chốt giao thức, RAID, controller, fabric và multipath.'),
 ('Mạng lõi','02 Nexus N9K-C93180YC-EX','Hai nhánh mạng A/B theo quy hoạch.','Port map, peer/keepalive, MTU, cấu hình và failover.'),
 ('Tường lửa','02 FortiGate 500E','NGFW/IPS/VPN và HA theo thiết kế.','Xác nhận license/support, state sync và phép thử HA.'),
 ('Mạng SAN và OOB','01 switch SAN; 01 Access','Chưa có model và phương án dự phòng xác nhận.','Đánh giá điểm lỗi đơn, phương án xử lý và kiểm thử.')]
vlans=[
 ('10','Internal service','Control/service nội bộ; chỉ luồng đã duyệt sang API private.'),
 ('20','Tenant overlay','Transport tenant; không cấp quyền tới underlay/control/OOB.'),
 ('30','Ceph client','Client I/O; tên “public” của Ceph không có nghĩa Internet công khai.'),
 ('31','Ceph cluster','Replication, recovery và heartbeat; cô lập tenant.'),
 ('40','Security và quản trị','Tách quyền PAM, SIEM, backup và kho log; cần chốt cách phân tách nội vùng.'),
 ('70','OpenStack API private','Broker/gateway và quản trị được duyệt; TLS, audit và giới hạn quyền.'),
 ('99','OOB BMC iDRAC','Quản trị ngoài băng; không mở trực tiếp cho tenant/Internet.'),
 ('100','Portal DMZ','Web/ingress; đường portal tới API thông qua broker theo thiết kế.'),
 ('Chưa chốt','Provider và SAN','Chốt VLAN/VRF, external gateway, SAN zoning hoặc multipath phù hợp.')]
issues=[
 ('C4-GOV-10','Nguồn ghi bundle 07 node, LVM/no-Ceph khác thiết kế 09 server.','Đối soát Kolla inventory, CMDB và cấu hình thực tế; phân biệt lab, staging, production.','Platform / PMO'),
 ('C4-SW-02','Nguồn ghi registry insecure và CVE Critical còn bản vá.','Kiểm tra bản dựng hiện hành, TLS/trust, digest; đối chiếu báo cáo quét và kết quả xử lý.','Platform / SecOps'),
 ('C4-IAM-06','Nguồn ghi 6 SSH host private key trong image.','Xác minh image/digest; loại khóa dùng chung nếu còn, xoay khóa liên quan, lưu kết quả quét lại.','DevSecOps / IAM'),
 ('C4-NET-07','Nguồn chưa chứng minh hai tuyến độc lập và failover.','Thu hợp đồng/tuyến vật lý, cấu hình routing và biên bản thử mất tuyến, mất thiết bị.','NetOps / IDC'),
 ('C4-CLD-16','Nguồn còn IP và tên miền ví dụ.','Kiểm tra cấu hình production, DNS, chứng thư và endpoint; ghi nhận thay thế theo change.','Platform'),
 ('C4-DC-18','Nguồn cũ ghi một DC và chưa có DR độc lập.','Cập nhật DC Cầu Giấy và DR Nam Thăng Long; kiểm tra tài sản, hợp đồng, bản sao và diễn tập.','SRE / IDC'),
 ('C4-SW-04','Nguồn ghi Đạt đối chiếu checksum bundle.','Tái kiểm tra đúng bundle đang dùng; checksum không tự chứng minh chữ ký hay nguồn phát hành.','DevSecOps')]

d=Doc('Kế hoạch đối soát thiết kế và tồn tại từ hồ sơ tham khảo',False)
d.cover('Bổ sung cho sổ tay và checklist kỹ thuật')
d.p('Khối Hạ tầng & Vận hành sử dụng tài liệu này để đối soát thiết kế trong bản 0.9.4 với nền tảng đang vận hành tại DC Cầu Giấy và DR Nam Thăng Long. Đầu ra cần có là danh mục tài sản được xác nhận, các thay đổi đã nghiệm thu và bằng chứng gắn với từng kiểm soát.')
d.h('1 Dữ liệu kế thừa và cách xác nhận')
d.p('Nguồn tham khảo: '+source_name+', ngày lập 06/10/2026; Phần II–III, Phụ lục D–G. Số liệu BOM/VLAN là thiết kế ghi trong nguồn, chưa có biên bản kiểm kê hoặc nghiệm thu đi kèm. Không tự phân bổ BOM này cho DC hoặc nhân đôi thành cấu hình DR.')
d.table(['Thông tin','Cách dùng khi rà soát'],[
 ('Tổ chức và phạm vi','Dùng tên Công ty Cổ phần XOR CLOUD; Khối Hạ tầng & Vận hành; toàn bộ XOR STACK CLOUD và quản trị chung. Hai IDC theo xác nhận của chủ quản cung cấp hồ sơ.'),
 ('129 mục cũ','Giữ đủ mã, nội dung, trạng thái và tồn tại trong workbook 04_Doi_soat_129_hang_muc_v094.xlsx. Cột kết quả hiện tại tách riêng và bắt đầu Chưa xác minh.'),
 ('119 dòng TC và 18 dòng CL','Tiếp tục dùng workbook 02 để kiểm tra yêu cầu đã diễn giải. Số dòng nội bộ không phải số điều khoản hoặc chứng nhận; không cộng 129 với 119 thành số kiểm soát đã đáp ứng.'),
 ('Dữ liệu thiếu','Điền kết quả thật, người kiểm tra, ngày và EV. Mọi khác biệt với nguồn phải có kết luận giữ, sửa, thay thế hoặc không áp dụng có căn cứ.')],[1,2.6])
d.p('Thống kê trong bản nguồn: 97 Chưa đánh giá; 21 Đang thực hiện; 6 Không đạt; 4 Cần xác minh; 1 Đạt. Đây là trạng thái lịch sử của tài liệu tham khảo, không phải kết quả đánh giá hiện tại.')

d.page('2 Đối soát thiết bị và năng lực')
d.p('Nguồn: Phần II mục 4, trang 12–13 của bản 0.9.4. Kỹ thuật bổ sung serial, site/rack/U, đường điện A/B, NIC–switch, firmware, hạn hỗ trợ và mã EV cho từng thiết bị.')
d.table(['Nhóm','SL và model nguồn','Quy hoạch nguồn','Việc cần chốt'],bom,[.9,1.2,2,2],9)
d.p('Tổng RAM theo vai trò: 3 × 128 + 3 × 512 + 3 × 128 = 2.304 GB. Đây là tổng theo thiết kế, không phải RAM bán được. Không dùng số 5.120 GB của bảng định giá cũ thay cho cụm này.')
d.p('19,2 TB Ceph và 14,4 TB SAN đều là dung lượng raw. Cần tính dung lượng sử dụng riêng theo replica/RAID, dự phòng, mức đầy và khả năng phục hồi. Nguồn chưa có CPU, tải thực, usable/IOPS hoặc kết quả N+1 đủ để cam kết SLA.')

d.page('3 Đối soát phân vùng mạng')
d.p('Nguồn: Phần II mục 5, trang 14–15. Bảng sau là quy hoạch logic tham khảo. Giữ sơ đồ kiến trúc mục tiêu của bộ hồ sơ và bổ sung bản vẽ triển khai tại từng site sau khi phê duyệt.')
d.table(['VLAN','Vai trò trong nguồn','Điểm kiểm tra'],vlans,[.55,1.2,3],9.5)
d.p('Nguồn ghi VLAN 30/40 trong bảng cũ từng có ý nghĩa khác. Không áp cấu hình theo số VLAN khi chưa xác minh ngữ nghĩa. Lập bảng chuyển đổi gồm VLAN/VRF cũ, VLAN/VRF mới, CIDR, gateway, owner, chính sách, ảnh hưởng, kế hoạch chuyển và rollback.')
d.p('Với mỗi luồng: ghi nguồn, đích, hướng, cổng/giao thức, mục đích, điểm kiểm soát, rule ID và phép thử cho phép/từ chối. WAF chỉ áp dụng giao thức web phù hợp; không bắt mọi lưu lượng VM đi qua WAF. OOB, control, storage và tenant phải được kiểm tra cô lập theo thiết kế đã duyệt.')

d.page('4 Các mục cần kiểm tra trước')
d.p('Các mục dưới đây được chọn từ trạng thái Không đạt và Đạt trong bản nguồn. Ưu tiên xác minh phạm vi và phiên bản trước khi quyết định khắc phục; chưa có kết luận chúng còn tồn tại trong production hiện tại.')
d.table(['Mã nguồn','Ghi nhận cũ','Công việc kiểm tra','Đầu mối đề xuất'],issues,[.9,1.5,2.3,1],9)
d.p('Không xóa nhận xét cũ khi đóng việc. Giữ báo cáo trước và sau, ticket thay đổi, EV retest và người chấp nhận. Nếu cùng một tồn tại ảnh hưởng nhiều kiểm soát, dùng chung mã việc/EV và liên kết đủ các dòng.')

d.page('5 Trình tự bàn giao sang hồ sơ hành chính')
d.p('Bước 1. Giao từng dòng trong workbook 04 cho một cá nhân. Các trường vàng là nơi nhập kết quả hiện tại, thời hạn, hành động và bằng chứng. Tab Nguon_v094 giữ dữ liệu lịch sử để đối chiếu.')
d.p('Bước 2. Mỗi mã C4 được liên kết với mã TC/CL/HS/T liên quan trong workbook 02 khi người kiểm tra xác định đúng yêu cầu. Một mục C4 có thể liên quan nhiều dòng; không ghép tự động theo số thứ tự hoặc lấy căn cứ cũ làm căn cứ hiện hành.')
d.p('Bước 3. Hoàn thành rà soát và phép thử phù hợp. Nếu đánh dấu Đạt hoặc Không áp dụng, phải có kết luận/hành động, EV, người xác minh và ngày. Trạng thái Đủ dữ liệu xác minh chỉ thể hiện đủ trường khai báo để người kiểm tra xem xét, không thay kết luận chuyên môn.')
d.p('Bước 4. Chuyển dữ liệu được xác nhận sang phụ lục 10 của Bộ 2, thuyết minh, sổ rủi ro và báo cáo tự rà soát. Chủ quản chốt phạm vi, căn cứ cấp độ, phân công và thẩm quyền; kỹ thuật bàn giao bằng chứng có kiểm soát phiên bản.')
d.table(['Mốc nội bộ đề xuất','Đầu ra','Người xác nhận'],[
 ('Khởi động đối soát','Phạm vi hai site, danh sách dịch vụ, chủ việc 129 dòng và kho EV.','Khối Hạ tầng & Vận hành'),
 ('Chốt thiết kế triển khai','BOM theo site, inventory, IP/port/rack map, luồng mạng và danh mục thay đổi.','Kiến trúc / Platform / NetOps / Storage'),
 ('Xác nhận kết quả kỹ thuật','Kết quả T01–T12 áp dụng, retest, RPO/RTO đo được và rủi ro còn lại.','Người kiểm tra được phân công'),
 ('Bàn giao hồ sơ','Workbook khóa phiên bản, phụ lục xác nhận, hồ sơ chuyên môn và danh sách còn thiếu.','Chủ trì lập hồ sơ / chuyên trách ANM')],[1.1,2.6,1.3])
d.p('Thời hạn thực hiện và ngày hoàn thành do các đầu mối thống nhất, nhập vào workbook; chưa ấn định mốc cam kết khi chưa có kế hoạch nguồn lực được phê duyệt.')
d.save(TECH/'03_Ke_hoach_doi_soat_nguon_v094.docx')

d=Doc('Phụ lục đối chiếu thiết kế và xác nhận hiện trạng hệ thống')
d.cover('Kèm theo thuyết minh hồ sơ đề xuất cấp độ 4')
d.p('Phụ lục này xác định cơ sở thiết kế kế thừa, phạm vi cần xác nhận và trách nhiệm hoàn thiện thông tin trước khi phát hành hồ sơ chính thức. Khối Hạ tầng & Vận hành chịu trách nhiệm đối chiếu số liệu, cấu hình và kết quả kiểm tra với hệ thống thực tế; đơn vị chuyên trách an ninh mạng xem xét theo phân công.')
d.h('1 Thông tin thống nhất trong bộ hồ sơ')
d.table(['Nội dung','Thông tin'],[
 ('Tên hệ thống','XOR SECURE CLOUD; nền tảng XOR STACK CLOUD do XOR CLOUD phát triển lại và đóng gói trên cơ sở OpenStack.'),
 ('Chủ quản và vận hành',ORG+'; đơn vị vận hành: '+OPERATOR+'.'),
 ('Phạm vi','Toàn bộ nền tảng cloud và các dịch vụ quản trị chung. Phần thuộc trách nhiệm khách hàng được xác định theo hợp đồng và ma trận trách nhiệm.'),
 ('Địa điểm','DC: Trung tâm Hạ tầng IDC Cầu Giấy. DR: Trung tâm Hạ tầng IDC Nam Thăng Long.'),
 ('Tình trạng thủ tục','Lập hồ sơ lần đầu; chưa có quyết định phê duyệt cấp độ hoặc chứng nhận theo thông tin được cung cấp.'),
 ('Tài liệu thiết kế tham khảo',source_name+'; phiên bản 0.9.4 ngày 06/10/2026.')],[1,2.6])
d.p('Số lượng và cấu hình dưới đây được kế thừa dưới dạng thông số thiết kế tham khảo. Số liệu hiện trạng và việc phân bổ thiết bị theo địa điểm phải được xác nhận bằng hồ sơ kiểm kê, cấu hình và biên bản nghiệm thu. Việc xác nhận có hai địa điểm không thay thế kết quả kiểm thử phục hồi tại địa điểm dự phòng.')

d.page('2 Cơ sở thiết kế hạ tầng')
d.table(['Thành phần','Thiết kế trong tài liệu tham khảo','Thông tin cần xác nhận'],[
 ('Máy chủ','09 Dell R630: 03 Controller, 03 Compute KVM, 03 Ceph SSD.','Số lượng thực tế từng site; serial; cấu hình; vai trò và phiên bản.'),
 ('Bộ nhớ','2.304 GB RAM theo tổng cấu hình các vai trò.','Bộ nhớ khả dụng; dự phòng; công suất khi mất thành phần.'),
 ('Lưu trữ','Ceph SSD 19,2 TB raw; SAN 14,4 TB raw; 18 ổ OS 480 GB.','Dung lượng usable; replica/RAID; backend; mã hóa và phục hồi.'),
 ('Mạng và bảo vệ biên','02 Nexus N9K-C93180YC-EX; 02 FortiGate 500E; 01 switch SAN; 01 Access.','Sơ đồ và port map; dự phòng; license/support; kết quả chịu lỗi.'),
 ('Kết nối liên trung tâm','Hai địa điểm DC và DR đã được xác nhận về phạm vi.','Nhà mạng; tuyến; băng thông; mã hóa; độ trễ; cơ chế sao chép và khả năng chuyển đổi.')],[1,2,2],10.5)
d.p('Nguồn số liệu: Phần II mục 3–5 và Phần III của tài liệu tham khảo; bảng thiết bị tại trang 12–13. Chưa sử dụng các giá trị raw để công bố dung lượng khai thác. Chưa xác định BOM này là toàn bộ cấu hình của cả hai địa điểm hoặc là cấu hình riêng của một địa điểm.')
d.h('Phân vùng và luồng thông tin')
d.p('Thiết kế tham khảo gồm các mạng internal service, tenant overlay, Ceph client, Ceph cluster, quản trị và bảo vệ, API private, OOB và DMZ. Các VLAN 10, 20, 30, 31, 40, 70, 99 và 100 được dùng làm mã đối chiếu thiết kế. Provider/external và SAN còn phải xác định chi tiết. Bản vẽ triển khai, địa chỉ, rule và luồng cho phép là thành phần cần bổ sung trước xác nhận hiện trạng.')

d.page('3 Phạm vi dịch vụ và hai địa điểm')
d.table(['Nhóm dịch vụ','Phạm vi dự kiến rà soát','Xác nhận triển khai'],[
 ('Tính toán và mạng','VM, image, flavor, volume, mạng riêng, router, SG, floating IP; LB nếu có.','[CẦN ĐIỀN dịch vụ, phiên bản, site và EV]'),
 ('Quản trị chung','Portal/API, identity, quota, usage/billing, CMDB, giám sát, log và hỗ trợ.','[CẦN ĐIỀN thành phần, đơn vị chịu trách nhiệm và EV]'),
 ('Dữ liệu và sao lưu','Backend thực tế, snapshot, backup, cấu hình và khóa phục hồi.','[CẦN ĐIỀN loại dữ liệu, vị trí, retention và EV]'),
 ('Dịch vụ mở rộng','Kubernetes, GPU, S3, cơ sở dữ liệu quản trị hoặc dịch vụ khác trên sơ đồ mục tiêu.','[CẦN XÁC NHẬN đã triển khai, dự kiến hoặc không thuộc phạm vi đợt này]')],[1,2,1.7],10.5)
d.p('Việc một dịch vụ có trên sơ đồ mục tiêu không xác nhận dịch vụ đó đã cung cấp. Phụ lục danh mục dịch vụ phải ghi rõ trạng thái và giới hạn đánh giá; không loại bỏ thành phần dùng chung nếu thành phần đó ảnh hưởng tới hệ thống thuộc phạm vi.')
d.table(['Địa điểm','Vai trò đã xác nhận','Hồ sơ cần bổ sung'],[
 ('IDC Cầu Giấy','DC chính','Địa chỉ chi tiết; hợp đồng/SLA; rack/điện/lạnh; danh mục thiết bị; kết nối và kiểm soát vật lý.'),
 ('IDC Nam Thăng Long','DR','Cấu hình phục hồi; dữ liệu và phiên bản sao chép; tài khoản/khóa; hồ sơ IDC; bằng chứng thử chuyển đổi và chuyển về.')],[1,1,2.8],10.5)
d.p('BIA phải xác định RPO/RTO cho từng dịch vụ, trình tự phục hồi và các phụ thuộc IAM, DNS, mạng, khóa, cơ sở dữ liệu, lưu trữ và giám sát. Giá trị mục tiêu, số đo thực tế và người xác nhận được ghi trong biên bản; không tự đặt kết quả đạt khi chưa thử.')

d.page('4 Danh mục hồ sơ xác nhận')
d.table(['Mã','Tài liệu phải đối chiếu','Đơn vị chủ trì','Mã EV và phiên bản'],[
 ('XN01','BOM theo site, serial, rack, port và điện A/B.','Hạ tầng / IDC','[CẦN ĐIỀN]'),
 ('XN02','OpenStack/Kolla inventory, bản dựng XOR, SBOM và cấu hình.','Platform','[CẦN ĐIỀN]'),
 ('XN03','VLAN/VRF/IP, rule liên vùng, OOB và kết nối hai site.','Network','[CẦN ĐIỀN]'),
 ('XN04','Backend dữ liệu, mã hóa, khóa, dung lượng và chịu lỗi.','Storage / IAM','[CẦN ĐIỀN]'),
 ('XN05','Quét lỗ hổng, kiểm thử độc lập, retest và thay đổi.','Chuyên trách ANM','[CẦN ĐIỀN]'),
 ('XN06','BIA, backup/restore, diễn tập DR và RPO/RTO.','SRE / vận hành','[CẦN ĐIỀN]'),
 ('XN07','Hồ sơ pháp nhân, phân công, thẩm quyền ký và liên hệ.','Chủ quản / pháp chế','[CẦN ĐIỀN]')],[.55,2.4,1.2,1],10.5)
d.p('129 mục kiểm soát của bản tham khảo được lưu trong workbook đối soát của Bộ 1. Các trạng thái lịch sử không được chuyển thành kết luận hiện tại nếu chưa có xác minh. Việc dẫn chiếu căn cứ trong bảng cũ phải được đối chiếu với văn bản áp dụng và phụ lục yêu cầu của bộ hồ sơ này; số dòng không xác định mức độ đáp ứng.')
d.p('Sau đối soát, đơn vị vận hành cập nhật thuyết minh, thiết kế triển khai, báo cáo rủi ro và báo cáo tự rà soát; đồng thời lập danh sách nội dung chưa hoàn thành, người chịu trách nhiệm và thời hạn. Hồ sơ xin ý kiến hoặc thẩm định phải phản ánh đúng tình trạng triển khai và kế hoạch bảo đảm an ninh mạng tại thời điểm trình.')
d.save(ADMIN/'10_Phu_luc_doi_chieu_thiet_ke_va_hien_trang.docx')

# Mỗi bộ có bản hướng dẫn đọc riêng; các tài liệu cốt lõi giữ cùng phiên bản.
for p in [TECH/'01_So_tay_ra_soat_ky_thuat.docx',ADMIN/'00_Huong_dan_hoan_thien_va_trinh_ho_so.docx']:
 x=Document(p)
 if p.parent==TECH:
  x.add_page_break();x.add_heading('Bổ sung đối soát tài liệu tham khảo',1)
  x.add_paragraph('Bắt đầu đối soát bản 0.9.4 bằng tài liệu 03 và workbook 04. Workbook 02 tiếp tục là checklist yêu cầu và bằng chứng chính. Workbook 04 giữ đủ 129 mục nguồn, có trường kết quả hiện tại riêng; cần liên kết mã TC/CL/HS/T theo nội dung sau khi người kiểm tra xác nhận, không cộng gộp số dòng thành tỷ lệ đáp ứng.')
  x.add_paragraph('Các tồn tại nguồn ưu tiên gồm: khác biệt inventory, registry và bản vá, khóa SSH trong image, dự phòng mạng, IP/tên miền mẫu và hồ sơ DR. Thông tin có DC Cầu Giấy và DR Nam Thăng Long đã được cập nhật theo xác nhận; cấu hình và kết quả kiểm thử từng site còn cần EV.')
 else:
  x.add_page_break();x.add_heading('Đối chiếu thiết kế trước khi trình',1)
  x.add_paragraph('Đọc phụ lục 10 cùng thuyết minh 01. Phụ lục bổ sung BOM, phân vùng và giới hạn dữ liệu kế thừa từ bản 0.9.4; danh mục XN01–XN07 xác định hồ sơ cần xác nhận trước phát hành. Bộ 1 có workbook giữ đủ 129 mục nguồn để truy vết và cập nhật kết quả mới.')
  x.add_paragraph('Không dùng các trạng thái cũ của bản tham khảo thay cho kết quả đánh giá. Các mẫu công văn, tờ trình, ý kiến, quyết định và thông báo trong Bộ 2 được dùng theo điều kiện ghi trong từng văn bản. Không có chữ ký, số văn bản hoặc kết luận đánh giá được tạo thay cơ quan, tổ chức có thẩm quyền.')
 x.save(p)
