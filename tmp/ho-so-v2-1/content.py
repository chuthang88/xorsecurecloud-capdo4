from pathlib import Path
import json

ROOT=Path('/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud')
OUT=ROOT/'output/XOR-Ho-so-CD4-v2.1'
TMP=ROOT/'tmp/ho-so-v2-1'
DATE='17/10/2026'
ORG='Công ty Cổ phần XOR CLOUD'
OPERATOR='Khối Hạ tầng & Vận hành'
ADDRESS='Tầng 7, Tòa nhà Việt Á, số 09 phố Duy Tân, phường Cầu Giấy, TP Hà Nội'
SIGNER='Lê Anh Vũ'
ROLE='TỔNG GIÁM ĐỐC'
OPS_SIGNER='Trần Văn Dũng'
OPS_ROLE='GIÁM ĐỐC KHỐI HẠ TẦNG & VẬN HÀNH'
SPECIALIST='Trung tâm Vận hành'
AUTHOR_NAME='Chử Quang Thắng'
AUTHOR_ROLE='Giám đốc Vận hành'
LEGAL='Nghị định số 331/2026/NĐ-CP ngày 19 tháng 8 năm 2026 của Chính phủ về bảo vệ an ninh mạng đối với hệ thống thông tin'
URL='https://vanban.chinhphu.vn/?docid=219243&pageid=27160'
SOURCE='TCVN 14423:2026'

# Các hàng là diễn giải phục vụ kiểm tra, không sao chép nội dung tiêu chuẩn.
# Mỗi tiểu mục đánh số tại Điều 6.1–6.18 và A.4 đều được ánh xạ.
GROUPS={
 '6.1':'Rủi ro','6.2':'Phần cứng','6.3':'Phần mềm','6.4':'Dữ liệu',
 '6.5':'Cấu hình','6.6':'Tài khoản và quyền','6.7':'Lỗ hổng và bản vá','6.8':'Nhật ký',
 '6.9':'Web và email','6.10':'Chống mã độc','6.11':'Sao lưu', '6.12':'Hạ tầng mạng',
 '6.13':'Giám sát','6.14':'Nhân sự','6.15':'Nhà cung cấp','6.16':'Phát triển an toàn',
 '6.17':'Ứng phó sự cố','6.18':'Kiểm tra an ninh','A.4':'An toàn vật lý'}
CONTROLS=[]
def add(group, owner, text):
 for line in text.strip().splitlines():
  ref,pg,title,req,plan,evidence,test=line.split('|')
  CONTROLS.append(dict(id=f'TC-{len(CONTROLS)+1:03}',group=GROUPS[group],clause=ref,page=pg,title=title,requirement=req,plan=plan,evidence=evidence,test=test,owner=owner,source=SOURCE))

add('6.1','GRC và chủ quản', '''
6.1.2.1|58|Quy trình rủi ro|Có quy trình xác định, phân tích, đánh giá, xử lý; rà soát ít nhất hằng năm và khi thay đổi.|Ban hành QT01 cho nền tảng, tenant và dịch vụ chung; phân công người phê duyệt rủi ro.|Quy trình đã ký; lịch sử sửa đổi; biên bản rà soát.|Đối chiếu đủ các bước và ngày rà soát gần nhất.
6.1.2.2|58|Nhận diện rủi ro|Nhận diện cả rủi ro nội bộ và nhà cung cấp ít nhất 1 lần/6 tháng, khi thay đổi liên quan.|Lập sổ rủi ro DC, DR, XOR STACK, IDC, ISP và chuỗi phần mềm.|Sổ rủi ro; đầu vào CVE; đánh giá IDC/ISP.|Chọn một thay đổi và kiểm tra có cập nhật rủi ro.
6.1.2.3|58|Đánh giá tác động|Phân tích khả năng, tác động, quyết định xử lý hoặc chấp nhận; đánh giá lại khi thay đổi.|Thực hiện BIA theo từng dịch vụ; phân tích ảnh hưởng khách hàng và lợi ích công cộng.|BIA; thang điểm; hồ sơ quyết định của chủ quản.|Kiểm tra căn cứ chấm điểm và người chấp nhận rủi ro.
6.1.2.4|58|Xử lý rủi ro|Có biện pháp, ứng phó rủi ro còn lại; đánh giá hiệu lực ít nhất 1 lần/6 tháng.|Gắn rủi ro với ticket khắc phục, người phụ trách, hạn và phép thử lại.|Kế hoạch xử lý; ticket; kết quả retest; chấp nhận tồn dư.|Theo dõi một rủi ro từ phát hiện đến đóng hoặc chấp nhận.
6.1.2.5|59|Theo dõi rủi ro|Theo dõi thay đổi khả năng, tác động, mức rủi ro, tài sản và biện pháp.|GRC cập nhật sổ rủi ro theo cảnh báo SOC và thay đổi kiến trúc.|Phiên bản sổ rủi ro; báo cáo định kỳ.|Đối chiếu rủi ro với tài sản và các thay đổi gần nhất.
6.1.2.6|59|Thông tin rủi ro|Chia sẻ kết quả và thông báo kịp thời thay đổi quan trọng cho bên liên quan.|Thiết lập danh sách nhận thông tin theo phạm vi và trách nhiệm.|Thông báo; biên bản họp; xác nhận tiếp nhận.|Kiểm tra một rủi ro ảnh hưởng tenant đã được chuyển đúng đầu mối.
''')
add('6.2','Hạ tầng và IT', '''
6.2.1; 6.2.2.1|59|Danh mục phần cứng|Kiểm kê toàn bộ tài sản, kể cả bên ngoài kết nối; rà soát ít nhất hằng năm; đủ IP/MAC/serial, vị trí, EOL, mục đích, chủ sở hữu; kiểm tra trước dùng và đăng ký thiết bị di động.|CMDB chung DC/DR chứa host, switch, storage, BMC, PAW và thiết bị thuê; tài sản mới có phiếu tiếp nhận.|CMDB; rack map; biên bản bàn giao và kiểm tra; danh sách thiết bị di động.|Chọn tài sản từ rack và từ scan rồi đối chiếu hai chiều với CMDB.
6.2.2.2|59|Thiết bị chưa quản lý|Có quy trình phát hiện và xử lý thiết bị trái phép ít nhất hằng quý; loại bỏ, chặn hoặc cách ly theo quyết định.|NAC và kiểm kê định kỳ; gắn ticket cho thiết bị chưa rõ chủ.|Quy trình; kết quả phát hiện; ticket cách ly.|Thử một thiết bị kiểm thử chưa đăng ký trên phạm vi được duyệt.
6.2.2.3|60|Rà quét tài sản|Rà quét thiết bị kết nối ít nhất hằng quý và cập nhật danh mục.|So khớp discovery với Neutron, hypervisor, IPAM và CMDB.|Báo cáo discovery có ngày; đối soát chênh lệch.|Chọn một tài sản mới và xác minh đã nhập CMDB.
6.2.2.4|60|DHCP và IPAM|Ghi DHCP hoặc sử dụng IPAM nếu có; rà soát nhật ký ít nhất hằng quý để cập nhật tài sản.|Lưu DHCP/Neutron/IPAM về kho log có định danh tenant.|Cấu hình log; mẫu log; biên bản đối soát.|Đối chiếu lease hoặc cấp IP với tài sản và tenant.
6.2.2.5|60|Thanh lý và xóa dữ liệu|Có quy trình thanh lý; xóa sạch dữ liệu khi chuyển giao hoặc đổi mục đích.|Sanitize ổ đĩa, volume và thiết bị theo loại media; xác nhận hủy khóa khi phù hợp.|Phiếu thanh lý; chứng cứ sanitize; biên bản xác nhận.|Kiểm tra mẫu tài sản đã thu hồi và kết quả xác minh xóa.
''')
add('6.3','Platform và DevSecOps', '''
6.3.1; 6.3.2.1|60|Danh mục phần mềm|Kiểm kê ít nhất hằng năm; có phiên bản, bản quyền, phạm vi, EOL, người quản lý và phần mềm thực tế cài đặt.|Quản lý phiên bản XOR, OpenStack upstream, OS, agent, firmware và container theo release.|Danh mục; SBOM; inventory máy chủ; giấy phép.|Đối chiếu một host và một image với danh mục phát hành.
6.3.2.2|60–61|Phần mềm được phép|Danh sách được duyệt bao gồm runtime và dịch vụ nhà cung cấp; kiểm soát cài/gỡ/thực thi trái phép; rà soát ít nhất hằng năm hoặc khi thay đổi.|Kho gói và image đã duyệt; quyền cài đặt qua ticket; ghi vết thay đổi.|Allowlist; quyền repository; log cài đặt; phê duyệt ngoại lệ.|Thử chặn gói/image không được duyệt trong môi trường thử nghiệm.
6.3.2.3|61|Hỗ trợ vòng đời|Rà soát ít nhất hằng năm để phần mềm được phép còn được hỗ trợ.|Lập kế hoạch hỗ trợ bản fork XOR và bản upstream; xử lý thành phần hết hỗ trợ.|Ma trận EOL; cam kết hỗ trợ; kế hoạch nâng cấp.|Đối chiếu phiên bản đang chạy với thời hạn hỗ trợ thực tế.
6.3.2.4|61|Phần mềm trái phép|Phát hiện và xử lý ít nhất 1 lần/6 tháng; ngoại lệ có biện pháp giảm rủi ro; gỡ phần mềm không được chấp thuận.|Đối soát inventory với allowlist; quản lý ngoại lệ có hạn.|Báo cáo đối soát; sổ ngoại lệ; ticket gỡ.|Chọn một sai lệch và kiểm tra xử lý hoặc phê duyệt ngoại lệ.
''')
add('6.4','Chủ dữ liệu và bảo mật', '''
6.4.2.1|61–62|Quy định quản lý dữ liệu|Quy định phân loại, chủ sở hữu, xử lý, lưu giữ, hủy và thay đổi dữ liệu; kiểm tra phân quyền ít nhất hằng quý; rà soát quy định hằng năm/khi thay đổi.|Phân loại dữ liệu nền tảng và tenant; gắn chính sách truy cập và retention theo loại.|Quy định; danh mục phân loại; biên bản rà soát quyền.|Kiểm tra dữ liệu nhạy cảm có người sở hữu và quy tắc xử lý.
6.4.2.2|62|Danh mục dữ liệu|Lập và cập nhật danh mục ít nhất hằng năm hoặc khi có thay đổi.|Liệt kê DB nền tảng, bí mật, log, ảnh, volume, backup và dữ liệu khách hàng theo phạm vi.|Danh mục dữ liệu có phiên bản.|Chọn một kho lưu trữ và đối chiếu chủ dữ liệu, mức nhạy cảm.
6.4.2.3|62|Quyền trên dữ liệu|Có danh sách quyền của từng tài khoản/nhóm đối với từng loại dữ liệu.|Ánh xạ Keystone, DB role, object ACL và tài khoản backup tới chủ thể.|Ma trận quyền; trích cấu hình ACL/RBAC.|Thử quyền đọc/ghi đúng và sai tenant với dữ liệu thử.
6.4.2.4 a|62|Mã hóa khi lưu|Bảo vệ dữ liệu xác thực, nhạy cảm và quan trọng khi lưu bằng mã hóa hoặc kiểm soát rủi ro tương đương.|Mã hóa volume/object/backup và kho bí mật; mô tả các ngoại lệ và giới hạn bảo vệ.|Cấu hình; danh mục phạm vi mã hóa; đánh giá tương đương.|Kiểm tra dữ liệu lưu có được bảo vệ và ai có quyền giải mã.
6.4.2.4 b c|62|Mã hóa khi truyền|Bảo vệ dữ liệu quan trọng khi truyền; tối thiểu hai lần mã hóa hoặc kiểm soát rủi ro tương đương theo điều khoản.|Đề xuất TLS ứng dụng trong kênh IPsec cho luồng quan trọng; thuyết minh từng luồng.|Ma trận luồng; cấu hình TLS/IPsec; hồ sơ tương đương.|Kiểm tra đồng thời hai lớp tại cùng đoạn truyền; không tính TLS kết thúc rồi tái mã hóa là hai lớp đồng thời.
6.4.2.4 d e|62|Quản lý khóa và thuật toán|Có phương án chuyên dụng bảo vệ khóa và dữ liệu mã hóa; sử dụng mật mã mạnh.|Quản lý vòng đời khóa trong KMS; tách người quản trị khóa; danh mục thuật toán được phép.|Chính sách khóa; RBAC; log luân chuyển; danh mục thuật toán.|Thử thu hồi, khôi phục khóa và từ chối quản trị viên không được cấp quyền.
6.4.2.5|62|Toàn vẹn dữ liệu|Có kiểm tra toàn vẹn, cảnh báo sửa đổi và khôi phục dữ liệu quan trọng.|FIM/checksum/chữ ký phù hợp từng loại; đối chiếu bản sao tin cậy.|Cấu hình FIM; cảnh báo; biên bản khôi phục.|Sửa dữ liệu thử có kiểm soát và xác minh phát hiện, phục hồi.
6.4.2.6|62|Luồng dữ liệu|Tài liệu hóa luồng và quản lý phiên bản; cập nhật ít nhất hằng năm hoặc khi thay đổi.|Duy trì DFD API, metadata, lưu trữ, log, backup và liên site.|DFD; lịch sử sửa; phê duyệt luồng.|Chọn một API/dịch vụ và truy vết đường đi, kho đích, chủ thể.
6.4.2.7|63|Phân tách dữ liệu nhạy cảm|Tách xử lý/lưu trữ theo độ nhạy cảm hoặc biện pháp tương đương; bảo vệ trao đổi bằng kênh riêng hoặc tương đương.|Phân khu dữ liệu và khóa; kiểm soát xuất dữ liệu; không dùng vùng ít nhạy cảm cho dữ liệu quan trọng.|Sơ đồ phân khu; policy; đánh giá phương án tương đương.|Thử luồng chéo vùng và xuất dữ liệu ngoài danh sách cho phép.
6.4.2.8|63|Chống thất thoát|Triển khai kiểm soát thất thoát dữ liệu quan trọng, nhạy cảm.|DLP và hạn chế egress/export theo kênh; tích hợp SOC.|Cấu hình; chính sách phân loại; cảnh báo thử.|Dùng mẫu dữ liệu giả lập để thử kênh email, web, USB hoặc API áp dụng.
6.4.2.9|63|Log dữ liệu quan trọng|Ghi hành vi truy cập và rà soát thường xuyên, ít nhất hằng quý.|Thu DB audit/object access log/volume export và rà soát theo tenant.|Mẫu log; biên bản rà soát; ticket bất thường.|Truy ngược một thao tác đọc/sửa/xuất tới người thực hiện.
6.4.2.10|63|Chữ ký số|Trao đổi thông tin quan trọng dùng chữ ký số từ chủ thể có thẩm quyền hoặc nhà cung cấp được phép; bảo vệ việc sử dụng.|Xác định giao dịch cần ký số; quản lý chứng thư và thiết bị khóa; phân biệt với TLS.|Danh sách giao dịch; chứng thư; quy trình; kết quả xác minh chữ ký.|Thử xác minh chữ ký đúng/sai, hết hạn hoặc bị thu hồi.
''')
add('6.5','Platform và IT', '''
6.5.2.1|63–64|Cấu hình chuẩn|Có quy trình và baseline; giao thức an toàn, host firewall, chống đăng nhập tự động vào tài sản quan trọng, vô hiệu dịch vụ thừa; hardening trước dùng; rà soát hằng năm/khi thay đổi.|Baseline riêng controller, compute, storage, network, PAW và ứng dụng XOR; theo dõi lệch cấu hình.|Baseline; export đã che bí mật; báo cáo drift; phê duyệt ngoại lệ.|Đối chiếu host mẫu và kiểm tra phát hiện một thay đổi ngoài baseline.
6.5.2.2|64|Khóa phiên|Thiết lập tự khóa theo nhu cầu/rủi ro và cơ chế mở khóa khẩn cấp; các ngưỡng trong điều khoản là cấu hình có thể áp dụng.|Đề xuất PAW 15 phút, phiên quản trị 5 phút; chốt ngưỡng khóa sau đăng nhập sai và phục hồi theo đánh giá rủi ro.|Chính sách đã chốt; cấu hình timeout; log thử và khẩn cấp.|Đo thời gian không hoạt động; thử khóa và mở khóa có phê duyệt.
6.5.2.3|64|Dịch vụ không cần thiết|Có quy định gỡ hoặc vô hiệu tính năng và dịch vụ không cần thiết.|Tối thiểu hóa image OS và dịch vụ; kiểm soát package/port được phép.|Danh sách dịch vụ; kết quả scan port; baseline.|Đối chiếu cổng và service thực tế với danh sách được duyệt.
6.5.2.4|64|DNS tin cậy|Cấu hình DNS tin cậy trên tài sản khi có.|Resolver nội bộ có dự phòng; ACL chỉ cho DNS được duyệt.|Cấu hình resolver; ACL; log DNS.|Thử resolver đúng và chặn truy vấn trực tiếp tới DNS ngoài.
6.5.2.5|64|Xóa thiết bị từ xa|Có khả năng xóa sạch từ xa đối với thiết bị di động cấp người dùng.|MDM cho thiết bị quản trị di động được cấp; thử trên thiết bị mẫu.|Danh sách MDM; cấu hình; biên bản remote wipe.|Kiểm tra thu hồi/xóa dữ liệu công việc trên thiết bị kiểm thử.
6.5.2.6|64|Không gian làm việc di động|Quy định tách không gian làm việc trên thiết bị di động được cấp.|Tách dữ liệu công việc/cá nhân; hạn chế sao chép theo chính sách.|Policy MDM/work profile; cấu hình.|Thử chuyển dữ liệu giữa hai không gian theo chính sách.
''')
add('6.6','IAM và bộ phận an ninh', '''
6.6.1; 6.6.2.1|65|Danh mục tài khoản|Quản lý đủ tài khoản và chủ sở hữu, loại, trạng thái, tài sản, ngày kích hoạt/vô hiệu; rà soát ít nhất hằng quý; ghi log hoạt động.|Đối soát IdP, Keystone, OS, DB, network, backup và tài khoản dịch vụ.|Danh mục; ma trận quyền; biên bản rà soát; audit log.|Chọn tài khoản bất kỳ và xác minh chủ thể, lý do quyền, trạng thái.
6.6.2.2|65–66|Chính sách mật khẩu|Đổi mặc định; quy định độ dài, thành phần, kỳ thay và hiệu lực theo rủi ro. Điều khoản có các cấu hình tham khảo cho MFA và không MFA.|Ban hành baseline xác thực phù hợp nền tảng; chốt tham số và kiểm soát ngoại lệ; không ghi mật khẩu vào hồ sơ.|Policy; cấu hình; thử mật khẩu; hồ sơ ngoại lệ.|Thử mật khẩu mặc định/yếu và kiểm tra thực thi kỳ thay đã phê duyệt.
6.6.2.3|66|Quản lý tài khoản đặc quyền|PAM hoặc tương đương, quản lý tập trung, tách loại tài khoản, định danh cá nhân; quản lý khóa; xử lý mặc định; vô hiệu tài khoản không hoạt động sau 45 ngày hoặc khi thay đổi nhân sự; rà soát quy định hằng năm.|Cấp phiên PAM theo ticket, ghi phiên và JIT; tài khoản dùng chung chỉ theo ngoại lệ có truy trách nhiệm.|Danh mục PAM; log phiên; ticket nghỉ việc; danh sách không hoạt động.|Thử thu hồi quyền, hết thời hạn; kiểm tra tài khoản nhàn rỗi trên toàn hệ thống.
6.6.2.4|66|MFA và quyền tối thiểu|Quyền tối thiểu, tách nhiệm vụ; MFA với truy cập ngoài tổ chức, đối tác, Internet và quyền quản trị; rà soát quy định hằng năm/khi đổi.|IdP/MFA bắt buộc cho portal quản trị, VPN và PAM; tách vận hành, bảo mật/khóa, kiểm toán.|Ma trận RBAC; policy MFA; log thử; phê duyệt vai trò.|Thử truy cập khi thiếu MFA và truy cập vượt vai trò.
6.6.2.5|66|Cấp đổi thu hồi quyền|Có quy trình cấp mới, thay đổi, thu hồi; rà soát quy trình và thực hiện ít nhất hằng năm/khi đổi.|Luồng yêu cầu → chủ tài sản duyệt → IAM thực hiện → người khác kiểm tra → lưu ticket.|Phiếu cấp quyền; phê duyệt; kết quả thực hiện và rà soát.|Truy vết một nhân sự vào/chuyển/nghỉ việc qua tất cả hệ thống.
''')
add('6.7','SecOps và Platform', '''
6.7.1; 6.7.2.1|67|Quản lý lỗ hổng|Theo dõi mối đe dọa; scan toàn hệ thống ít nhất 1 lần/6 tháng, tài sản quan trọng hằng quý; phân loại, chia sẻ, khắc phục và retest; cập nhật quy trình 6 tháng/khi đổi.|Lịch scan theo tenant/phạm vi; nguồn CVE cho upstream và fork; ưu tiên theo khả năng khai thác và tác động.|Phạm vi scan; báo cáo; ticket; SLA nội bộ; retest.|Đối chiếu CMDB với phạm vi scan và kiểm tra lỗ hổng đã đóng.
6.7.2.2|67|Quản lý bản vá|Quản lý tập trung; kiểm thử, đánh giá tác động và phương án phục hồi trước vá hệ thống quan trọng; kiểm tra/cập nhật máy người dùng ít nhất hằng tháng nếu có.|Kho vá nội bộ đã ký; staging trước production; cửa sổ thay đổi và rollback cho controller/compute.|Lịch vá; bằng chứng thử; phê duyệt; inventory phiên bản.|Kiểm tra phiên bản sau vá và một lần rollback có hồ sơ.
''')
add('6.8','SOC', '''
6.8.2.1 a|68|Phạm vi và trường nhật ký|Thu log truy cập, tiến trình, ứng dụng, dữ liệu và cảnh báo trên toàn bộ tài sản; có nguồn/đích, định danh, thời gian, hành vi và trường phù hợp từng loại.|Lập ma trận nguồn log; chuẩn hóa actor, tenant, request ID và sự kiện quản trị XOR/OpenStack.|Ma trận nguồn; mẫu từng loại log; parser.|Tạo sự kiện mẫu trên mỗi loại tài sản và tìm lại đầy đủ trường.
6.8.2.1 a|68|Đồng bộ và tập trung log|Đồng bộ thời gian; SIEM hoặc tương đương; chuyển log về hệ thống tập trung.|NTP nội bộ dự phòng; agent/collector TLS; queue đệm và cảnh báo mất nguồn.|Cấu hình NTP; pipeline; chứng thư; dashboard nguồn.|So thời gian và mô phỏng gián đoạn collector để kiểm tra mất log.
6.8.2.1 a b|68|Lưu giữ và rà soát log|Dung lượng lưu tối thiểu 6 tháng; theo dõi đầy kho; rà soát nhật ký ít nhất hằng tháng; cập nhật quy trình hằng năm/khi đổi.|Chính sách retention theo tháng lịch và dung lượng đo thực; quy trình rà soát SOC.|Cấu hình retention; truy vấn log cũ; số đo EPS; báo cáo tháng.|Truy vấn mốc lưu giữ, kiểm tra cảnh báo đầy kho; không coi 180 ngày luôn bằng 6 tháng.
6.8.2.2|69|Log nhà cung cấp|Thu nhật ký an ninh của các dịch vụ nhà cung cấp có kết nối/sử dụng.|Thỏa thuận với IDC, ISP, SOC và dịch vụ dùng chung về log, phạm vi và truy xuất.|Hợp đồng; log nhận; biên bản đối soát.|Kiểm tra truy xuất một sự kiện của bên cung cấp trong phạm vi.
6.8.2.3|69|Bảo vệ nhật ký|Kiểm soát và ghi lịch sử truy cập; chống sửa/xóa; kho log ở hệ thống và vùng mạng riêng; mã hóa log quan trọng nếu có.|Z08 riêng; quyền lưu/xóa tách cloud admin; bất biến hoặc cơ chế toàn vẹn tương đương.|ACL; sơ đồ; retention lock; log thao tác kho.|Thử sửa/xóa bằng quyền cloud admin và xác minh bị ngăn hoặc cơ chế bảo vệ theo thiết kế.
''')
add('6.9','IT và SOC', '''
6.9.2.1|69|Trình duyệt và email|Danh mục được phép, còn hỗ trợ, vá thường xuyên hoặc kiểm soát tương đương; bảo vệ thư điện tử.|Áp dụng cho máy trạm và email vận hành trong phạm vi; quản lý tập trung phiên bản.|Danh mục; policy; phiên bản; giải pháp email.|Kiểm tra trình duyệt trên PAW và dịch vụ email vận hành.
6.9.2.2|69|Lọc tên miền|Chặn tên miền độc hại và giả mạo bằng dịch vụ lọc tên miền.|Resolver có threat feed và log về SOC.|Cấu hình; feed; log thử.|Thử tên miền kiểm thử an toàn do công cụ cung cấp.
6.9.2.3|69|Lọc URL|Cập nhật bộ lọc URL, hạn chế kết nối tới web độc hại/không được phép.|Proxy/secure gateway cho máy trạm được phép ra ngoài; quản trị core không ra Internet.|Policy URL; lịch cập nhật; log.|Thử URL thuộc nhóm chặn và kiểm tra cảnh báo.
6.9.2.4|69|Tiện ích mở rộng|Danh sách được phép; kiểm soát cài đặt, gỡ/vô hiệu tiện ích trái phép.|Quản lý extension trình duyệt/email theo allowlist.|Allowlist; policy; inventory extension.|Thử cài extension không được phép trên máy thử.
6.9.2.5|70|Xác thực email|Áp dụng DMARC để hạn chế giả mạo tên miền tổ chức.|Thiết lập SPF/DKIM/DMARC theo dịch vụ email thực tế, theo dõi báo cáo.|DNS record; cấu hình mail; báo cáo DMARC.|Xác minh alignment và xử lý thư giả mạo trong môi trường thử.
6.9.2.6|70|Tệp đính kèm|Quy định loại tệp được phép; chặn ngoài danh mục và kiểm soát thư có tệp đính kèm.|Mail gateway kiểm tra tệp theo chính sách.|Danh sách; cấu hình; log thử.|Gửi tệp thử được phép và bị cấm tới hộp thử.
''')
add('6.10','SecOps', '''
6.10.1; 6.10.2.1|70|Bảo vệ mã độc|Có quy định chống mã độc; bảo vệ tài sản và điểm kết nối; máy chủ/máy người dùng có bảo vệ thời gian thực, hành vi, cập nhật tự động hoặc tương đương.|EDR tương thích KVM/controller/storage; ghi nhận ngoại lệ kỹ thuật và bù trừ.|Policy; độ phủ; phiên bản agent; ngoại lệ.|So CMDB với console EDR và dùng mẫu thử an toàn.
6.10.2.2|70|Thiết bị lưu trữ ngoài|Quét media di động và vô hiệu tự thực thi.|Kiểm soát USB trên PAW và máy vận hành.|Policy; log cắm thiết bị và scan.|Thử USB mẫu trên thiết bị được duyệt.
6.10.2.3|70|Quản lý chống mã độc tập trung|Quản lý cập nhật, cảnh báo và cấu hình tập trung.|Console SecOps độc lập quyền cloud admin; cảnh báo agent mất liên lạc.|Console; chính sách; log cập nhật.|Tạm dừng agent thử và kiểm tra cảnh báo.
6.10.2.4|70|Chống khai thác|Bật khả năng chống khai thác lỗ hổng trên tài sản nếu có.|Bật tính năng tương thích và đánh giá tác động hiệu năng.|Cấu hình; ma trận tương thích; thử nghiệm.|Đối chiếu trạng thái bật và ngoại lệ được duyệt.
6.10.2.5|71|Phát hiện hành vi|EDR hoặc tương đương trên máy chủ/máy người dùng, gửi SIEM và cảnh báo thời gian thực.|Luồng agent → console → SIEM; playbook cô lập có kiểm soát.|Mẫu sự kiện; rule; ticket phản ứng.|Dùng mô phỏng an toàn để đo phát hiện và tạo ticket.
''')
add('6.11','Backup và Platform', '''
6.11.2.1|71|Quy trình sao lưu|Định nghĩa dữ liệu, tần suất, phương pháp, kho, thử khôi phục; gồm cấu hình, ảnh OS, DB và nghiệp vụ; sẵn sàng cao; rà soát hằng năm/khi đổi.|Backup cả control plane, cấu hình SDN, image, dữ liệu dịch vụ và khóa phục hồi; chốt RPO/RTO qua BIA.|Policy; catalog job; bản đồ phụ thuộc; BIA.|Đối chiếu một dịch vụ có đủ dữ liệu và bí mật để dựng lại.
6.11.2.2|71|Sao lưu tự động|Phân loại lịch và tự động sao lưu theo từng loại dữ liệu.|Job có giám sát lỗi, dung lượng và lần thành công gần nhất.|Lịch job; log; cảnh báo thất bại.|Thử một job thất bại và kiểm tra phát hiện/chạy bù.
6.11.2.3|71–72|Bảo vệ bản sao|Áp dụng 3-2-1 hoặc tương đương; mã hóa bản sao dữ liệu quan trọng, nhạy cảm.|Bản sao độc lập, có bản ngoài miền lỗi chung; tài khoản/khóa sao lưu riêng.|Sơ đồ bản sao; quyền; cấu hình mã hóa; đánh giá tương đương.|Kiểm tra khả năng truy cập/khôi phục khi nguồn sản xuất bị mất.
6.11.2.4|72|Kho sao lưu tách biệt|Định danh, quản lý phiên bản và lưu trên hạ tầng độc lập với môi trường vận hành.|Z09 riêng; không chỉ giữ snapshot trên cùng cụm sản xuất; khóa và quyền xóa riêng.|Inventory repository; sơ đồ; versioning; ACL.|Kiểm tra cloud admin không xóa được toàn bộ bản sao độc lập.
6.11.2.5|72|Kiểm thử khôi phục|Có phương án toàn vẹn; kiểm tra phục hồi bản sao ít nhất 1 lần/6 tháng.|Restore vào vùng cô lập; kiểm tra dữ liệu, ứng dụng và phụ thuộc khóa; lưu số đo.|Biên bản restore; checksum; log và thời gian.|Khôi phục mẫu DB/VM/config/khóa và đối chiếu kết quả nghiệp vụ.
''')
add('6.12','Network và Platform', '''
6.12.2.1|72|Hồ sơ kiến trúc mạng|Có thiết kế tổng thể, chi tiết, phương án bảo vệ; chuyên môn đánh giá trước triển khai; phân vùng, quyền tối thiểu, HA, phân đoạn vi mô hoặc tương đương; rà soát 6 tháng/khi đổi.|Duy trì HLD/LLD 12 vùng; quản lý phiên bản và quyền đọc tài liệu; kiểm tra route thực tế.|As-built; sơ đồ vật lý/lô-gic; review; ma trận kết nối.|Đi từ sơ đồ tới cấu hình trên mẫu thiết bị của cả DC/DR.
6.12.2.2 a|73|Dự phòng mạng và Internet|Dự phòng kết nối máy chủ, cân bằng tải và dự phòng nóng thiết bị chính; nếu cần Internet, ít nhất hai luồng quốc tế từ ISP trong nước có hạ tầng khác nhau.|Dual NIC/fabric, FW/LB HA, hai ISP; xác minh tuyến cáp và miền lỗi.|Hợp đồng; topology; cấu hình HA; biên bản failover.|Ngắt từng thành phần trong cửa sổ thử; đo gián đoạn theo mục tiêu đã chốt.
6.12.2.2 a|73|Tường lửa và IPS|FW có chống xâm nhập hoặc tương đương giữa các vùng; kiểm soát mã độc trên môi trường mạng.|NGFW/IPS tại Z01 và ranh giới phù hợp; cập nhật chữ ký, giám sát tải.|Rule; signature; log; capacity.|Thử luồng được phép, bị chặn và mẫu phát hiện an toàn.
6.12.2.2 a|73|Bảo vệ CSDL|DBF hoặc phương án tương đương cho CSDL tập trung.|Kiểm soát truy vấn, audit, quyền và phát hiện bất thường với DB nền tảng/DBaaS thuộc trách nhiệm XOR.|Thiết kế DBF/DAM/tương đương; audit; rule.|Thử truy cập/truy vấn trái quyền và chứng minh kiểm soát tương đương nếu dùng.
6.12.2.2 a|73|Kiểm soát lớp mạng|NAC hoặc tương đương quản lý thiết bị đầu cuối kết nối; giám sát tập trung.|802.1X/NAC hoặc kiểm soát cổng/thiết bị theo rủi ro; monitoring tập trung.|Policy; danh sách thiết bị; log; sơ đồ.|Thử thiết bị lạ và kiểm tra tình trạng kết nối.
6.12.2.2 a|73|WAF và chống DDoS|Bảo vệ ứng dụng web nếu có; chống từ chối dịch vụ bằng dịch vụ/giải pháp hoặc tương đương.|Bảo vệ portal/API công khai tại DMZ; chỉ nhận origin qua WAF; phối hợp ISP chống DDoS.|Policy; origin ACL; hợp đồng; kịch bản thử.|Thử bypass origin và kịch bản chống DDoS trong phạm vi cho phép.
6.12.2.2 a|73|Biên vùng lõi ít tin cậy|Datadiode/USG/BSG hoặc kiểm soát rủi ro tương đương cho vùng lõi/OT với vùng ít tin cậy.|Lập hồ sơ luồng một chiều/hai chiều, giới hạn giao thức và xác minh phương án tương đương.|DFD; đánh giá rủi ro; thiết kế cổng; kết quả thử.|Kiểm tra không có đường vòng qua cổng và kiểm tra luồng ngoài danh sách.
6.12.2.2 a|73|Duy trì hạ tầng mạng|Cập nhật phát hiện tấn công; quản lý thay đổi/kết nối/gỡ thiết bị; theo dõi hiệu năng; bảo vệ Wi-Fi nếu có.|Thay đổi qua ticket, cập nhật rule, giám sát CPU/RAM/băng thông; tách Wi-Fi nếu tồn tại.|Ticket; báo cáo capacity; chính sách Wi-Fi; cập nhật rule.|Chọn một thay đổi và đối chiếu phê duyệt, cấu hình, rollback.
6.12.2.2 b|73–74|Phân vùng theo chức năng|Tách nội bộ, biên, máy chủ nội bộ, DMZ, CSDL, quản trị thiết bị và quản trị; WAN/Wi-Fi nếu có.|Ánh xạ Z01–Z12; phân khu storage, API, DB, queue và OOB; không coi một VPC là đủ.|VLAN/VRF/VXLAN; SG; route; sơ đồ.|Thử truy cập liên vùng và chéo tenant ngoài ma trận.
6.12.2.3|74|Giao thức an toàn|Chỉ sử dụng giao thức truyền thông và quản trị an toàn theo điều khoản.|Chốt phiên bản TLS/SSH và bộ mật mã phù hợp bản dựng; tắt giao thức yếu.|Cấu hình; báo cáo kiểm tra TLS/SSH.|Kiểm tra endpoint và xác minh giao thức yếu bị từ chối.
6.12.2.4|74|Quy tắc truy cập mạng|Xác thực, kết nối an toàn, allowlist vào/ra theo dịch vụ; timeout, giới hạn kết nối theo năng lực, kiểm soát nội bộ và egress máy chủ.|Default deny; rule có owner, ticket và thời hạn; egress qua điểm kiểm soát.|Ma trận luồng; rule export; cấu hình timeout/rate.|Thử cả cho phép và từ chối; kiểm tra cổng không cung cấp bị chặn.
6.12.2.5|74–75|Quản trị từ xa|VPN/ZTNA hoặc tương đương; MFA và xác thực bổ sung; giới hạn nguồn/thiết bị; quản trị gián tiếp và endpoint được bảo vệ.|PAW → gateway Z01 → PAM Z06 → đích được duyệt; không route toàn mạng.|Policy; cấu hình; log PAM; trạng thái EDR.|Thử thiếu MFA, máy lạ, bỏ qua PAM và quyền hết hạn.
6.12.2.6|75|Mạng quản trị chuyên dụng|Tài nguyên quản trị tách vật lý/lô-gic với mạng chính và không kết nối Internet.|Z06/Z10 riêng; không egress Internet; bản vá nhập qua kho trung chuyển kiểm tra.|Route; ACL; topology; quy trình nhập gói.|Thử Internet từ mạng quản trị và truy cập OOB từ tenant.
6.12.2.7|75|Kiểm thử và nghiệm thu|Có kế hoạch, thử trước bàn giao/vận hành, giám sát độc lập; báo cáo được chuyên trách xác nhận và chủ quản duyệt.|Tổ chức T01–T12; bằng chứng cấu hình và retest kèm biên bản.|Kế hoạch; phân công độc lập; biên bản; phê duyệt.|Kiểm tra phép thử thực tế gắn đúng bản dựng và ngày nghiệm thu.
''')
add('6.13','SOC', '''
6.13.2.1|75|Giám sát tập trung 24 trên 7|Giám sát thiết bị, máy chủ, ứng dụng, dịch vụ; liên kết sự kiện bằng SIEM; bố trí nguồn lực 24/7.|SOC có ca trực, escalation, người thay ca và phạm vi nguồn log hai IDC.|Lịch trực; SLA; use case; ticket; log bàn giao.|Kiểm tra cảnh báo ngoài giờ được tiếp nhận và xử lý.
6.13.2.2|75|Tính năng phòng vệ hệ thống|Bật firewall/phát hiện/ngăn chặn xâm nhập của OS/hệ thống nếu có.|Host firewall, agent và FIM theo baseline đã kiểm thử tương thích.|Baseline; agent state; log.|Đối chiếu host mẫu với baseline và console giám sát.
6.13.2.3|76|Cổng kết nối và quản trị|Kiểm soát cổng thiết bị nếu hỗ trợ; tách cổng quản trị ứng dụng với cổng dịch vụ.|Admin endpoint riêng, ACL qua PAM; port security trên switch/SDN.|Port map; cấu hình; endpoint catalog.|Thử từ mạng người dùng không tới endpoint quản trị.
6.13.2.4|76|Dữ liệu mạng|Thu flow log và/hoặc lưu lượng để rà soát, cảnh báo.|Thu NetFlow/IPFIX/SDN flow hoặc cảm biến phù hợp; bảo vệ dữ liệu thu.|Cấu hình exporter; mẫu flow; rule.|Tạo luồng thử và truy vết từ nguồn tới đích.
6.13.2.5|76|Điều chỉnh cảnh báo|Rà soát ngưỡng cảnh báo ít nhất hằng quý.|SOC đánh giá false positive và ca bỏ sót, có phê duyệt thay đổi rule.|Biên bản quý; phiên bản rule; kết quả thử.|Đối chiếu rule thay đổi với số liệu và retest.
''')
add('6.14','Nhân sự và chủ quản', '''
6.14.1; 6.14.2.1|76|Tổ chức và độc lập chuyên môn|Có bộ phận vận hành, quản trị và bảo vệ an ninh riêng; độc lập chuyên môn; nhân sự đủ năng lực.|Quyết định giao nhiệm vụ và RACI; kiểm soát xung đột quyền.|Sơ đồ tổ chức; quyết định; hồ sơ năng lực; ma trận quyền.|Đối chiếu người thực hiện, người duyệt và người kiểm tra một thay đổi.
6.14.2.2|76|Nhận thức và nghỉ việc|Đào tạo toàn bộ người dùng ít nhất hằng năm; khi đổi/nghỉ việc thu hồi tài sản, quyền vật lý/lô-gic, có cam kết bảo mật.|Onboarding/offboarding nối HR với IAM/IDC/IT; đào tạo nhận thức và kiểm tra.|Danh sách học; kết quả; NDA; phiếu thu hồi.|Theo dõi một nhân sự nghỉ việc qua thẻ IDC, VPN, PAM và dịch vụ.
6.14.2.3|77|Đào tạo theo vai trò|Đào tạo chuyên môn và trách nhiệm pháp lý ít nhất hằng năm hoặc khi thay đổi nhân sự liên quan.|Chương trình riêng Platform, Network, SOC, phát triển và quản trị khóa.|Kế hoạch; tài liệu; điểm kiểm tra; hồ sơ năng lực.|Kiểm tra người trực và người quản trị đã hoàn thành nội dung phù hợp.
''')
add('6.15','Mua sắm và GRC', '''
6.15.1; 6.15.2.1|77|Danh mục nhà cung cấp|Kiểm kê/phân loại, ranh giới trách nhiệm; nhà cung cấp ANM đủ điều kiện theo quy định; rà soát hằng năm/khi đổi.|Danh mục IDC, ISP, SOC, phần mềm và hỗ trợ; kiểm tra pháp lý theo dịch vụ thực tế.|Danh mục; hợp đồng; giấy tờ năng lực/điều kiện khi áp dụng.|Chọn nhà cung cấp trọng yếu và đối chiếu phạm vi được cung cấp.
6.15.2.2|77|Quy định nhà cung cấp|Có quy định quản lý; rà soát hằng năm/khi đổi.|Quy định lựa chọn, đánh giá, truy cập, giám sát và kết thúc dịch vụ.|Quy định; biên bản rà soát.|Đối chiếu một nhà cung cấp mới với quy trình.
6.15.2.3|77|Điều khoản bảo mật|Hợp đồng có yêu cầu bảo mật; rà soát khi gia hạn.|Thỏa thuận quyền truy cập, dữ liệu/log, sự cố, khôi phục, kiểm tra và chấm dứt.|Hợp đồng/SLA/phụ lục; review pháp chế.|Kiểm tra trách nhiệm IDC và XOR được phân định bằng văn bản.
6.15.2.4|77|Theo dõi nhà cung cấp|Giám sát việc thực hiện yêu cầu cung cấp dịch vụ.|Đối soát SLA, quyền truy cập, sự cố và bằng chứng định kỳ.|Báo cáo SLA; biên bản đánh giá; ticket.|Kiểm tra một vi phạm SLA đã có hành động.
6.15.2.5|77|Kết thúc hợp đồng|Rà soát an ninh khi chấm dứt.|Thu hồi quyền, nhận dữ liệu và log, xác nhận xóa/hoàn trả theo hợp đồng.|Checklist kết thúc; biên bản; log thu hồi.|Kiểm tra tài khoản đối tác đã khóa và dữ liệu đã bàn giao.
''')
add('6.16','DevSecOps', '''
6.16.2.1|78|Quy trình phát triển|Có SSDLC, rà soát hằng năm/khi đổi; phần thuê ngoài có cam kết, mã nguồn hoặc biện pháp thay thế theo điều khoản; thử và đánh giá trước dùng/khi đổi kiến trúc.|Áp dụng cho bản fork XOR, portal và API; yêu cầu release qua review, staging và phê duyệt.|SSDLC; hợp đồng; review; release checklist; báo cáo thử.|Chọn một release XOR và truy vết từ yêu cầu đến triển khai.
6.16.2.2|78|Tiếp nhận lỗ hổng phần mềm|Có kênh bên ngoài báo cáo và quy trình xử lý; rà soát hằng năm/khi đổi.|Đầu mối PSIRT/XOR tiếp nhận, phân loại, khắc phục, phản hồi.|Quy trình; kênh liên hệ; ticket đã che dữ liệu.|Gửi báo cáo thử được duyệt và kiểm tra tiếp nhận.
6.16.2.3|78|Nguyên nhân lỗ hổng|Phân tích nguyên nhân gốc của lỗ hổng.|Gắn RCA với defect và cập nhật rule/test để tránh tái diễn.|RCA; ticket; thay đổi test/code.|Chọn lỗi đã đóng và kiểm tra biện pháp chống tái diễn.
6.16.2.4|78–79|Thành phần bên thứ ba|Quản lý danh sách thành phần hiện tại/dự kiến và rủi ro; cập nhật ít nhất hằng quý.|SBOM theo release, nguồn gói, giấy phép, CVE và bản vá upstream.|SBOM; SCA; catalog dependency; review quý.|So image đang chạy với SBOM và kết quả SCA.
6.16.2.5|79|Tách môi trường|Tách dev/test/production; không lưu bí mật trong mã nguồn.|Project/credential/runner riêng; secret manager và dữ liệu thử đã xử lý.|Sơ đồ; quyền CI; secret scan.|Thử runner dev không triển khai hoặc đọc bí mật production.
6.16.2.6|79|Đào tạo lập trình|Đào tạo phát triển an toàn phù hợp môi trường ít nhất hằng năm.|Chương trình cho Python/API/IaC/container và phần tùy biến XOR.|Danh sách học; nội dung; bài kiểm tra.|Đối chiếu toàn bộ developer/reviewer với lịch đào tạo.
6.16.2.7|79|Kiến trúc ứng dụng an toàn|Kiểm tra đầu vào/ra; chống tấn công phổ biến; xử lý lỗi; quản lý phiên; không hardcode bí mật.|Threat model portal/API; validation, encoding, session và error handling theo thiết kế.|Threat model; code review; test; secret scan.|Thử đầu vào bất thường, phân quyền, phiên và thông báo lỗi.
6.16.2.8|79|Thành phần bảo mật tin cậy|Dùng mô-đun được kiểm chứng, mật mã mạnh và log hành vi người dùng.|Thư viện xác thực/mật mã có quản lý vòng đời; audit API theo request ID.|Danh mục thư viện; review; mẫu audit.|Kiểm tra thuật toán, dependency và khả năng truy vết thao tác.
6.16.2.9|79|Kiểm tra trước phát hành|Kiểm tra mã nguồn/dependency; pentest và xử lý lỗ hổng trước production.|SAST/SCA/secret scan/DAST và pentest theo phạm vi; gate phát hành, retest.|Báo cáo; waiver có hạn; phê duyệt release.|Chọn release và xác minh không bỏ qua điều kiện phát hành.
''')
add('6.17','CSIRT và SOC', '''
6.17.2.1|80|Lực lượng ứng phó|Có đầu mối chính và ít nhất một dự phòng, vai trò phối hợp; xác minh liên hệ hằng năm.|Chỉ định chỉ huy, kỹ thuật, pháp chế, truyền thông và đầu mối IDC/ISP.|Quyết định; danh bạ; lịch trực; xác minh liên hệ.|Thử gọi theo kịch bản và kiểm tra người dự phòng.
6.17.2.2|80|Báo cáo sự cố|Có quy trình nội bộ, phân nhóm; rà soát hằng năm/khi đổi.|SOC phân loại, mở hồ sơ, báo cáo chỉ huy và chuyển tuyến theo nghĩa vụ áp dụng.|Quy trình; mẫu báo cáo; ticket.|Đi qua một sự cố giả lập từ phát hiện đến báo cáo.
6.17.2.3|80|Quy trình ứng phó|Có quy trình phối hợp cơ quan chức năng, chuyên gia, nhà cung cấp; rà soát hằng năm/khi đổi.|Playbook lộ khóa, ransomware, truy cập chéo tenant, mất DC và DDoS.|Playbook; danh sách phối hợp; biên bản.|Diễn tập cô lập, bảo toàn chứng cứ, khôi phục theo quyền hạn.
6.17.2.4|80|Kênh liên lạc dự phòng|Có kênh chính/phụ; rà soát hằng năm/khi đổi.|Danh bạ và kênh ngoài nền tảng vẫn dùng được khi IAM/cloud dừng.|Danh bạ ngoại tuyến được bảo vệ; biên bản thử.|Thử liên lạc khi kênh chính không hoạt động.
6.17.2.5|80|Đánh giá sau sự cố|Thực hiện đánh giá sau sự cố.|Lập timeline, nguyên nhân, tác động và hành động có owner/hạn.|Báo cáo hậu kiểm; ticket cải tiến.|Kiểm tra hành động hậu kiểm đã có retest hoặc tiến độ.
6.17.2.6|80|Diễn tập|Có kế hoạch và diễn tập ít nhất hằng năm.|Kết hợp tabletop và thử kỹ thuật theo phạm vi đã duyệt.|Kế hoạch; biên bản; bài học; danh sách tham dự.|Đối chiếu thời gian, kịch bản, kết quả và hành động sau diễn tập.
6.17.2.7|80|Ngưỡng sự cố|Thiết lập, duy trì ngưỡng và cập nhật hằng năm/khi đổi.|Định nghĩa mức nghiêm trọng theo phạm vi dữ liệu, số tenant, thời gian gián đoạn và tác động xã hội.|Ma trận phân loại; phê duyệt; lịch sử sửa.|Thử phân loại một tình huống ở hai mức lân cận.
''')
add('6.18','Đánh giá độc lập và GRC', '''
6.18.2.1|81|Chương trình pentest|Phê duyệt phạm vi, thời gian, cách thử, đầu mối, giới hạn, bảo vệ dữ liệu và vận hành; ưu tiên môi trường phát triển/cửa sổ được duyệt.|ROE riêng cho portal/API, nội bộ, tenant isolation và đặc quyền; có dừng khẩn cấp.|ROE; phê duyệt; danh sách mục tiêu; cam kết bảo mật.|Kiểm tra phép thử chỉ nằm trong danh sách và có người phối hợp.
6.18.2.2|81|Pentest bên ngoài|Kiểm thử ứng dụng/dịch vụ công khai ít nhất hằng năm.|Pentest endpoint Internet của XOR theo FQDN/IP đã chốt.|Báo cáo; phạm vi; ngày; retest.|Đối chiếu toàn bộ dịch vụ công khai với phạm vi báo cáo.
6.18.2.3|81|Khắc phục sau pentest|Xử lý tồn tại theo phạm vi và mức ưu tiên của tổ chức.|Gắn phát hiện với ticket, SLA nội bộ, chủ sở hữu và phép thử lại.|Danh sách phát hiện; ticket; retest.|Kiểm tra lỗi đã đóng bằng kết quả thử, không chỉ bằng cam kết.
6.18.2.4|81|Hiệu lực kiểm soát|Đánh giá lại hiệu quả biện pháp sau mỗi đợt pentest.|SOC/Platform cập nhật rule, baseline và playbook theo bài học.|Biên bản review; rule/test bổ sung.|Đối chiếu một phát hiện với thay đổi kiểm soát.
6.18.2.5|81|Pentest bên trong|Kiểm thử tài nguyên nội bộ ít nhất hằng năm.|Đánh giá ranh giới quản trị, tenant, storage và dịch vụ nền trong phạm vi duyệt.|Báo cáo nội bộ; ROE; retest.|Kiểm tra thử từ các vùng tin cậy khác nhau và giới hạn đã nêu.
''')
add('A.4','IDC và Hạ tầng XOR', '''
A.4.1|109|Vị trí phòng máy|Vị trí tránh tầng cao, tầng hầm, nơi chứa nước và vùng dễ cháy/nhiễu mạnh theo điều khoản.|Khảo sát riêng IDC Cầu Giấy và IDC Nam Thăng Long; ghi vị trí thực, rủi ro và xử lý.|Bản vẽ vị trí; biên bản khảo sát; xác nhận IDC.|Quan sát tại chỗ/đối chiếu bản vẽ; không dùng chứng chỉ IDC để thay bằng chứng vị trí.
A.4.2|109|Ra vào và camera|Cổng điện tử; camera tập trung 24/7, lưu tối thiểu 6 tháng; vành đai và bảo vệ vùng thiết bị quan trọng.|Kiểm soát thẻ, khách thăm, rack và camera tại cả hai IDC.|Quy chế; access log; mẫu camera đủ mốc; hợp đồng.|Thử truy xuất dữ liệu và đối soát một lần ra vào được duyệt.
A.4.3|109|Chống trộm phá hoại|Rack cố định, nhãn, cáp đi ngầm có bảo vệ, báo động chống trộm tự động hoặc tương đương.|Khóa rack, quản lý chìa, giám sát cửa và tuyến cáp.|Ảnh hiện trạng; danh mục rack; biên bản thử báo động.|Khảo sát rack và thử cảnh báo theo lịch IDC cho phép.
A.4.4|110|Chống sét|Chống sét tòa nhà được nghiệm thu/kiểm tra; bảo vệ lan truyền điện và kết nối.|Thu hồ sơ chống sét, tiếp địa và kiểm tra định kỳ từ IDC.|Nghiệm thu; bản vẽ; đo kiểm; bảo trì.|Đối chiếu phạm vi hồ sơ có bao phủ phòng/rack XOR.
A.4.5|110|Phòng cháy|Báo/chữa cháy tự động, tín hiệu cảnh báo, vật liệu chịu lửa và cách ly vùng quan trọng.|Xác minh hệ thống PCCC và phương án phối hợp tại từng IDC.|Hồ sơ nghiệm thu; bảo trì; sơ đồ; diễn tập.|Quan sát và kiểm tra hồ sơ thử theo thẩm quyền IDC.
A.4.6|110|Chống nước|Bảo vệ thoát nước, trần/cửa và chống tích tụ, thấm nước vào phòng máy.|Kiểm tra đường ống, cảm biến rò và xử lý sự cố nước tại IDC.|Bản vẽ; biên bản khảo sát; log/cảnh báo nếu có.|Kiểm tra vị trí ống, lối thoát, dấu hiệu thấm và biện pháp ngăn nước.
A.4.7|110|Chống tĩnh điện|Biện pháp chống tĩnh điện và sàn chống tĩnh điện.|Quy trình thao tác phần cứng và bảo trì sàn tại IDC.|Hồ sơ vật liệu; kiểm tra; quy trình bảo trì.|Quan sát và đối chiếu bằng chứng kiểm tra phù hợp.
A.4.8|110|Nhiệt độ độ ẩm|Điều hòa phòng máy riêng, duy trì ổn định; đo/cảnh báo độ ẩm và hút ẩm.|Giám sát môi trường 24/7, giới hạn theo thiết bị và quy trình phản ứng.|Sơ đồ điều hòa; log nhiệt/ẩm; cảnh báo; bảo trì.|Thử cảnh báo an toàn và kiểm tra dữ liệu môi trường theo thời gian.
A.4.9|110–111|Nguồn điện|Nguồn ổn định có chống quá tải; hai nguồn từ hai trạm điện khác nhau; UPS liên tục.|Xác minh đường cấp điện, trạm nguồn, UPS và đấu A/B cho rack XOR.|Sơ đồ một sợi; xác nhận nguồn; log UPS; biên bản chuyển nguồn.|Đối chiếu nguồn thực tế; hai PDU cùng một trạm không tự đáp ứng yêu cầu hai trạm.
A.4.10|111|Bảo vệ điện từ|Tách điện và tín hiệu, che nguồn nhiễu; tấm chắn điện từ vùng máy chủ quan trọng/thiết bị mạng chính.|Khảo sát tuyến cáp, thiết bị gây nhiễu và che chắn khu vực tương ứng.|Bản vẽ; ảnh; hồ sơ vật liệu; kiểm tra của IDC.|Quan sát vùng quan trọng và đối chiếu phương án che chắn đã thực hiện.
''')

EXPECTED={1:6,2:5,3:4,4:10,5:6,6:5,7:2,8:3,9:6,10:5,11:5,12:7,13:5,14:3,15:5,16:9,17:7,18:5}
for g,n in EXPECTED.items():
 for k in range(1,n+1):
  clause=f'6.{g}.2.{k}'
  assert any(clause in x['clause'].split('; ') or x['clause'].startswith(clause+' ') or x['clause']==clause for x in CONTROLS),clause
for k in range(1,11):assert any(x['clause']==f'A.4.{k}' for x in CONTROLS)

SOURCES=[
 ['S1','Nghị định 331/2026/NĐ-CP','Điều 14, 18, 20–24; Phụ lục Mẫu 02, 03, 05, 06; PDF tr.9,11–17,32–40',URL,'Hiệu lực 19/8/2026; xác minh nguồn chính thức ngày 17/10/2026.'],
 ['S2','TCVN 14423:2026','Điều 6 tr.58–81; A.4 tr.109–111','Bản được cấp phép nội bộ','SHA-256 76c6c11eadf8aec7f0b95940463ac715df50c6356e234492e54d6e9f78c8647c; đã xem ảnh trang gốc.'],
 ['S3','Dự thảo TCVN Cloud năm 2026','Điều 4, 5; phần tham khảo bổ sung','Bản dự thảo 153 trang','Chưa có số tiêu chuẩn; không dùng làm căn cứ pháp lý bắt buộc hoặc kết luận chứng nhận.'],
 ['S4','Thông tin người dùng','Ngày 17/10/2026','Xác nhận trực tiếp','XOR STACK dựa OpenStack; toàn nền tảng; DC Cầu Giấy, DR Nam Thăng Long; hồ sơ lần đầu.'],
 ['S5','Nghị định 30/2020/NĐ-CP','Tham khảo thể thức văn bản hành chính','https://chinhphu.vn/default.aspx?docid=199378&pageid=27160','Áp dụng hình thức soạn thảo phù hợp tài liệu trình cơ quan; không thay căn cứ thẩm định cấp độ.']]

EXTRA=[]
def extra(text):
 for line in text.strip().splitlines():
  ident,title,ref,req,test,evidence,owner=line.split('|')
  EXTRA.append(dict(id=ident,group='Cloud và OpenStack',title=title,clause=ref,page='',requirement=req,test=test,evidence=evidence,plan=req,owner=owner,source='Thiết kế XOR hoặc dự thảo được ghi riêng'))
extra('''
CL-01|Bản dựng XOR|Thiết kế XOR; TCVN 6.3, 6.16|Gắn phiên bản XOR, commit, OpenStack upstream và danh mục khác biệt; không suy ra tính năng từ tên OpenStack.|Đối chiếu image đang chạy với release manifest và SBOM.|Manifest, digest, SBOM, bản vá, ma trận hỗ trợ.|DevSecOps
CL-02|Quorum mỗi site|Thiết kế XOR; TCVN 6.12|Controller/DB/queue có quorum trong từng site; thiết kế và thử độc lập DC/DR; không mặc định kéo cụm qua hai site.|Thử mất node và mất kênh liên site theo kế hoạch.|Cluster config, log failover, số đo gián đoạn.|Platform
CL-03|Cách ly mạng tenant|Thiết kế XOR; TCVN 6.12|Project, SDN, anti-spoofing, SG và routing giới hạn theo tenant; chặn tenant tới quản trị/underlay/storage backend.|Thử A truy cập B, giả mạo địa chỉ và endpoint nội bộ trên tài nguyên thử.|SG/route/port security, log thử.|Network
CL-04|Metadata và console|Thiết kế XOR; TCVN 6.6, 6.12|Bảo vệ metadata, console, token và URL console theo project; token có hạn; quản lý endpoint proxy.|Thử token sai/hết hạn và truy cập console/metadata của tenant khác.|Cấu hình, test IDOR, log API.|Platform
CL-05|Cách ly volume và object|Thiết kế XOR; TCVN 6.4|Kiểm tra attach/detach, snapshot, restore, image import, object ACL và tái cấp phát không lộ dữ liệu.|Thử chéo tenant và dữ liệu dư trên tài nguyên thử đã thu hồi.|RBAC, backend ACL, biên bản sanitize.|Storage
CL-06|Kubernetes quản lý|Thiết kế XOR; nếu cung cấp dịch vụ|RBAC, NetworkPolicy, hạn chế đặc quyền pod, bảo vệ secrets và audit; chặn workload tới API nội bộ không được phép.|Thử quyền cluster, pod đặc quyền và lưu lượng chéo namespace/tenant.|Version, policy, audit, admission logs.|Kubernetes
CL-07|CI CD và nguồn cung|Thiết kế XOR; TCVN 6.16|Ký artifact, kiểm tra digest, quyền runner hẹp, secret ngắn hạn, tách dev/test/prod và có rollback.|Thử phát hành image sai chữ ký/digest hoặc thiếu gate.|Pipeline, kết quả scan, approval, log rollback.|DevSecOps
CL-08|Sự cố đồng thời hai IDC|Thiết kế XOR và BIA|Đánh giá điện, cáp, ISP, nhân sự và rủi ro khu vực chung; bản sao ngoài miền lỗi chung nếu cần theo BIA.|Đối chiếu tuyến/nguồn thực tế và giả lập mất cả hai site trên bàn.|BIA, sơ đồ điện/cáp, quyết định xử lý rủi ro.|Hạ tầng
CL-09|Tuyến áp dụng Cloud|Dự thảo 5.1 tr.84–87|Xác nhận có áp dụng tham khảo; mô hình MH, mức và hạng phần mềm tách nhau; giả định MH3/Mức 4/Hạng B chưa phải kết quả đánh giá.|Chốt đối tượng phục vụ, cấp cao nhất và phạm vi tự nguyện.|Phiếu phạm vi, danh mục tenant, quyết định áp dụng tham khảo.|GRC
CL-10|Dịch vụ nền độc lập|Dự thảo 5.3.6 tr.92|Rà dự phòng máy chủ, mạng, lưu trữ, điện, DNS, IAM, DHCP và hàng đợi; DNS nội bộ không phụ thuộc DNS công cộng.|Dừng từng dịch vụ nền trong môi trường thử và đối chiếu hành vi.|Dependency map, cấu hình dự phòng, kết quả thử.|Platform
CL-11|Khởi động nguội|Dự thảo 5.3.9–5.3.10 tr.92|Đồ thị phụ thuộc không vòng; bí mật khẩn cấp ngoài nền tảng; diễn tập khởi động từ trạng thái dừng.|Khôi phục mạng, thời gian, IAM/khóa, lưu trữ, DB/queue, API và workload theo runbook.|Runbook, biên bản cold start, nhật ký truy cập bí mật.|Platform
CL-12|HSM và khóa chủ|Dự thảo 5.4.5.3–5.4.5.4 tr.93–94|Nếu áp dụng Mức 4 của dự thảo, khóa chủ ở HSM; người quản trị khóa không đồng thời quản trị hạ tầng; kiểm tra pháp luật mật mã tương ứng.|Thử quyền quản trị, backup/restore và mất HSM; không coi Barbican là bằng chứng HSM.|Sơ đồ khóa, cấu hình tích hợp, phân quyền, hồ sơ thiết bị.|Quản trị khóa
CL-13|Mã hóa mặc định|Dự thảo 5.4.8 tr.94–95|Nếu áp dụng dự thảo Mức 4, duy trì mã hóa lưu trữ mặc định; mô tả quyền tắt theo từng đối tượng thuộc bên sử dụng.|Tạo mới volume/object theo dịch vụ rồi kiểm tra trạng thái thực.|Cấu hình default, API result, key reference.|Storage
CL-14|MFA phần cứng|Dự thảo 5.5.2.3 tr.95|Nếu áp dụng dự thảo Mức 4, yếu tố thứ hai đặc quyền dựa phần cứng chống sao chép.|Thử đủ/thiếu thiết bị, thu hồi thiết bị và khôi phục có kiểm soát.|Policy, danh mục token, log xác thực.|IAM
CL-15|Chống lạm quyền nội bộ|Dự thảo 5.6 tr.96–99|Rà tách hạ tầng, bảo mật và kiểm toán; hành động nhạy cảm cần cơ chế phê duyệt; kiểm tra quyền truy cập dữ liệu khi đã giải mã.|Thử cloud admin xuất snapshot, đổi quyền khóa hoặc xóa dấu vết trong phạm vi thử được duyệt.|RBAC, phê duyệt, log bất biến, báo cáo thử đối kháng nội bộ.|CISO
CL-16|Chứng thư và thời gian|Dự thảo 5.4.6–5.4.7 tr.94|Kiểm kê chứng thư, cảnh báo hạn và thay CA; hai nguồn thời gian độc lập; phát hiện lệch giờ.|Thử đổi chứng thư, cảnh báo hết hạn và mất một nguồn giờ.|Inventory PKI, config NTP, kết quả thử.|Platform
CL-17|Nhật ký theo tenant|Dự thảo 5.9 tr.103–105|Kiểm tra phân quyền log và khả năng truy vết riêng từng tenant; bảo vệ độc lập quyền vận hành cloud.|Thử tenant A đọc log B và quyền quản trị sửa log.|Log schema, ACL, audit và kết quả thử.|SOC
CL-18|Backup bất biến và DR|Dự thảo 5.10 tr.105–106; thiết kế XOR|Rà bản sao bất biến control plane và dữ liệu tenant trong trách nhiệm; DR có đủ dịch vụ nền; RPO/RTO do BIA quyết định.|Thử xóa bản bất biến, restore, failover có fencing và failback.|Lock policy, runbook, số đo RPO/RTO, biên bản.|Backup
''')

DOSSIER=[
 ('HS01','Tổng quan HTTT','Điều 21.1 và 22.3','01 Thuyết minh, Phần I','Pháp nhân, chức năng, chủ quản, vận hành, người đại diện/liên hệ, phạm vi, quy mô, người dùng và dịch vụ.','GRC và chủ quản'),
 ('HS02','Thiết kế hệ thống đang vận hành','Điều 21.2 b; 22.3 d','01 Thuyết minh, Phần II và hồ sơ as-built','Thiết kế thi công đã được phê duyệt hoặc tài liệu tương đương; mô hình vật lý/lô-gic; tài sản, ứng dụng, OS, vị trí, IP và vùng mạng.','Kiến trúc và Platform'),
 ('HS03','Căn cứ đề xuất cấp độ','Điều 14; 21.3; 22.4–5','01 Thuyết minh, Phần III','Chọn tiêu chí Điều 14 có bằng chứng; loại dữ liệu, đối tượng phục vụ, ảnh hưởng và báo cáo rủi ro chi tiết.','GRC và pháp chế'),
 ('HS04','Phương án bảo đảm an ninh mạng','Điều 21.4; 22.6','01 Phần IV, 02 Phụ lục, 03 Quy chế','Biện pháp quản lý, kỹ thuật, vật lý cho từng yêu cầu; chỉ rõ hiện trạng, thiếu sót và kế hoạch.','CISO và kỹ thuật'),
 ('HS05','Ý kiến chuyên môn của đơn vị chuyên trách','Điều 21.5; 20.1 d','04 Công văn và 08 mục A','Văn bản thật của đơn vị chuyên trách thuộc chủ quản; người ký đúng thẩm quyền, kết luận và tồn tại.','Đơn vị chuyên trách ANM'),
 ('HS06','Công văn đề nghị thẩm định','Điều 20; Mẫu 02','05 Công văn đề nghị thẩm định','Chủ quản gửi cơ quan thẩm định đúng thẩm quyền; kèm HS01–HS05 và danh mục phiên bản.','Văn thư và chủ quản'),
 ('HS07','Ý kiến thẩm định','Điều 18; 23; Mẫu 04','Tài liệu tiếp nhận từ cơ quan thẩm định','Văn bản do cơ quan thẩm định ban hành; không tự lập thay hoặc điền sẵn đạt.','Chủ quản'),
 ('HS08','Tờ trình phê duyệt','Điều 24; Mẫu 05','06 Tờ trình','Hồ sơ đề xuất, ý kiến thẩm định và bản giải trình/khắc phục nếu có.','Đơn vị vận hành'),
 ('HS09','Quyết định phê duyệt cấp độ','Điều 18.3 d; Mẫu 06','07 Dự thảo quyết định','Chỉ ban hành sau quy trình thẩm định; ký bởi chủ quản; số, ngày và bản kèm theo khớp.','Chủ quản'),
 ('HS10','Quy chế và phân công','TCVN 6.1, 6.14, 6.17','03 Quy chế và quyết định ban hành thực tế','Bản đã ký, người phụ trách, lịch trực, RACI và đầu mối chính/dự phòng.','Chủ quản và HR'),
 ('HS11','Danh mục tài sản và dữ liệu','TCVN 6.2–6.4','Excel Tài sản, BIA và hồ sơ quản lý thực tế','CMDB phần cứng/phần mềm, danh mục dữ liệu, chủ sở hữu, phân loại và vòng đời.','Platform'),
 ('HS12','Cấu hình và kiểm soát truy cập','TCVN 6.5, 6.6, 6.12','Kho bằng chứng cấu hình','Baseline, ma trận quyền, MFA/PAM, firewall/SG, IP/route, khóa và bí mật đã che.','IAM và Network'),
 ('HS13','Bằng chứng giám sát','TCVN 6.8, 6.10, 6.13','Kho log và báo cáo SOC','Độ phủ, mẫu sự kiện, retention, bảo vệ log, lịch trực, ticket và xử lý ngoài giờ.','SOC'),
 ('HS14','Sao lưu và khôi phục','TCVN 6.11; BIA','Kho biên bản T08–T10','Lịch backup, bản sao độc lập, restore, failover, failback, cold start và RPO/RTO đo được.','Backup'),
 ('HS15','Báo cáo kiểm tra độc lập','TCVN 6.12.2.7; 6.18','08 mục B và báo cáo bên đánh giá','ROE, báo cáo pentest trong/ngoài, nghiệm thu và retest; bằng chứng phải gắn phiên bản.','Đánh giá độc lập'),
 ('HS16','Hồ sơ vật lý và nhà cung cấp','TCVN A.4; 6.15','Hồ sơ riêng hai IDC','Hợp đồng, SLA, trách nhiệm, điện/UPS/PCCC/ra vào/camera; xác minh phạm vi chứng chỉ.','IDC và mua sắm'),
 ('HS17','Công bố thông tin sau phê duyệt','Mẫu quản trị nội bộ','09 mục A','Chỉ công bố đúng quyết định, phạm vi và kết quả; rà thông tin nhạy cảm trước phát hành.','Chủ quản và pháp chế'),
 ('HS18','Đề nghị đánh giá sự phù hợp nếu có nhu cầu','Tuyến đánh giá riêng cần xác nhận','09 mục B','Chốt tiêu chuẩn/phiên bản, đối tượng, phạm vi, phương thức và thẩm quyền tổ chức đánh giá; không gọi là thủ tục cấp độ tự động.','GRC')]

TESTS=[
 ('T01','Phân vùng và công khai dịch vụ','Network','6.12.2.2–6.12.2.6','Danh mục IP/FQDN, luồng và cửa sổ thử đã duyệt.','Kiểm kê endpoint từ ngoài và từ tenant; thử luồng được phép, luồng cấm, origin bypass WAF và Internet từ mạng quản trị.','Chỉ có endpoint/luồng được duyệt; quản trị, DB, OOB không lộ; chặn truy cập sai vùng.','Rule export; log cho phép/từ chối; ảnh kết quả; phạm vi thử.'),
 ('T02','Cách ly tenant','Platform và Network','6.4.2.3; 6.12','Hai project và dữ liệu giả lập, tài khoản phân quyền rõ.','Thử API/list/read/write, metadata, console, attach/snapshot/restore, object ACL và traffic từ A tới B; ghi từng trường hợp.','Không đọc, sửa hoặc quản trị chéo tenant; không thấy dữ liệu dư khi cấp lại tài nguyên.','Request ID; log; cấu hình; biên bản từng bề mặt.'),
 ('T03','MFA và đặc quyền','IAM','6.6; 6.12.2.5','Tài khoản thử, ticket và tài khoản khẩn cấp trong phạm vi.','Thử thiếu MFA, thiết bị lạ, quyền hết hạn, bỏ qua PAM; thử cấp/thu hồi; kiểm tra một phiên khẩn cấp.','Đúng người/đích/thời hạn; phiên truy vết được; các đường bị cấm bị chặn; khẩn cấp được hậu kiểm.','Policy; log IdP/VPN/PAM; ticket; bản ghi phiên.'),
 ('T04','Dữ liệu và khóa','Quản trị khóa','6.4.2.4–6.4.2.10','Dữ liệu thử, bản sao khóa và phương án quay lại được duyệt.','Kiểm tra mã hóa lưu/truyền; hai lớp hoặc tương đương; thử sai quyền giải mã, luân chuyển/thu hồi/restore khóa và xác minh chữ ký.','Dữ liệu và khóa được bảo vệ theo phân loại; không có quyền giải mã ngoài ma trận; khôi phục không mất khả năng đọc.','Cấu hình; log KMS; biên bản kiểm tra; không chụp khóa/bí mật.'),
 ('T05','Nhật ký và cảnh báo','SOC','6.8; 6.13','Ma trận nguồn log, tài khoản thử, truy cập kho theo quyền.','Tạo mỗi loại sự kiện; tìm actor/tenant/thời gian; ngắt nguồn thử; kiểm tra lưu giữ đủ 6 tháng và thử sửa/xóa log bằng quyền cloud admin.','Đủ trường và nguồn; có cảnh báo mất nguồn; kho tách vùng; bảo vệ sửa/xóa hoạt động; retention được chứng minh.','Mẫu log đã che dữ liệu; truy vấn theo mốc; ticket ngoài giờ.'),
 ('T06','EDR và DLP','SecOps','6.4.2.8; 6.10','Mẫu thử an toàn của sản phẩm; máy/tệp giả lập.','Thử phát hiện hành vi và kênh thất thoát áp dụng; kiểm tra gửi SIEM, cô lập, hoàn tác và tương thích ứng dụng.','Phát hiện/chặn theo chính sách; có người xử lý; không gây tác động ngoài phạm vi.','Agent state; cảnh báo; ticket; biên bản xử lý.'),
 ('T07','Lỗi thành phần HA','Hạ tầng và Platform','6.12.2.2','Kế hoạch bảo trì, ngưỡng chấp nhận, tải thử và rollback.','Lần lượt thử mất controller, compute, storage node, NIC, FW/LB, ISP theo thiết kế; đo và xác minh dữ liệu.','Đạt ngưỡng đã phê duyệt; không mất nhất quán; đủ năng lực còn lại và không phát sinh điểm lỗi đơn chưa kiểm soát.','Timeline; metrics; cluster log; kiểm tra dữ liệu.'),
 ('T08','Sao lưu và restore','Backup','6.11.2.1–6.11.2.5','Kho restore cô lập, catalog dữ liệu và khóa cần thiết.','Chọn bản sao VM/DB/config/khóa; thử truy cập/xóa theo vai trò; restore và kiểm tra checksum, đăng nhập, dữ liệu nghiệp vụ.','Bản sao độc lập khôi phục được; kiểm tra bất biến nếu thiết kế dùng; thời gian và dữ liệu mất nằm trong chỉ tiêu đã chốt.','Job ID; bản sao được chọn; log; checksum; số đo.'),
 ('T09','Mất DC và chuyển về','Chỉ huy DR','BIA; 6.11; 6.12','BIA/RPO/RTO đã duyệt, cửa sổ thử, kênh phối hợp và rollback.','Xác nhận replica; cô lập nguồn ghi DC; kích hoạt DR cùng IAM/DNS/KMS; thử nghiệp vụ; đồng bộ và chuyển về theo runbook.','Đạt RPO/RTO từng dịch vụ; không dual writer; đủ công suất; failback được kiểm chứng.','Timeline; fencing log; lag; đối soát DB; phê duyệt chuyển đổi.'),
 ('T10','Khởi động nguội','Platform','Thiết kế XOR; tham khảo dự thảo 5.3.9','Môi trường khôi phục riêng; tài liệu và bí mật khẩn cấp có thể tiếp cận.','Giả lập dừng toàn nền tảng; lần lượt dựng dịch vụ theo dependency; không dùng bí mật chỉ nằm trên hệ thống đang dừng.','Dựng lại được control plane và dịch vụ mẫu; phát hiện/xử lý mọi vòng phụ thuộc.','Dependency map; thứ tự bước; log; biên bản truy cập khẩn cấp.'),
 ('T11','Phát hành an toàn','DevSecOps','6.16','Pipeline thử, artifact đúng/sai chữ ký và bản rollback.','Thử image chưa duyệt/sai digest, secret scan, quyền runner dev; phát hành bản hợp lệ rồi hoàn tác.','Gate từ chối bản không đạt; bản được duyệt truy nguyên được; rollback thành công.','Pipeline run; review; SAST/SCA; digest; biên bản rollback.'),
 ('T12','Pentest và đánh giá độc lập','Đơn vị đánh giá','6.18; 6.12.2.7','ROE ký, phạm vi IP/tenant, lịch, dữ liệu và điều kiện dừng.','Kiểm thử từ ngoài và trong; kiểm tra quyền nội bộ/cách ly; lập phát hiện; xử lý và retest; ghi giới hạn phương pháp.','Kết luận theo tiêu chí và phạm vi đã phê duyệt; phát hiện được xử lý hoặc quản lý đúng thẩm quyền; không tự đánh dấu đạt khi thiếu retest.','Báo cáo ký; ROE; ticket; retest; ý kiến nghiệm thu.')]

RISKS=[
 ('RR01','Tài khoản cloud admin bị chiếm hoặc lạm dụng','PAM, MFA, tách quyền, log độc lập','Lộ/sửa dữ liệu nhiều tenant; ảnh hưởng dịch vụ diện rộng','CISO','T03/T04/T05'),
 ('RR02','Vượt ranh giới tenant qua API hoặc SDN','RBAC, SG, kiểm tra sở hữu và cách ly','Lộ dữ liệu, thay đổi trái phép tài nguyên khách hàng','Platform','T02'),
 ('RR03','Ransomware phá cả bản chính và bản sao','Kho độc lập, bất biến, tách quyền và restore','Không khôi phục được dịch vụ và dữ liệu','Backup','T08'),
 ('RR04','Mất toàn bộ IDC Cầu Giấy','DR độc lập, replica, fencing, capacity','Gián đoạn đồng thời nhiều dịch vụ khách hàng','Hạ tầng','T09'),
 ('RR05','Mất kênh liên site hoặc hai site ghi đồng thời','Theo dõi lag, quorum riêng, fencing và quy trình DR','Dữ liệu không nhất quán hoặc mất giao dịch','Platform','T07/T09'),
 ('RR06','Mất khóa hoặc vòng phụ thuộc phục hồi','Backup khóa, bí mật khẩn cấp và cold start','Có bản sao nhưng không giải mã/dựng được hệ thống','Quản trị khóa','T04/T10'),
 ('RR07','Lỗ hổng hoặc mã độc trong bản đóng gói XOR','SBOM, review, ký image, gate và rollback','Tấn công chuỗi cung ứng vào nhiều host/tenant','DevSecOps','T11/T12'),
 ('RR08','DDoS hoặc lỗi thiết bị mạng/ISP','Hai ISP, chống DDoS, FW/LB HA','Mất truy cập dịch vụ công khai, suy giảm khả dụng','Network','T01/T07'),
 ('RR09','SOC thiếu nguồn log hoặc mất dấu vết','Ma trận nguồn, retention, chống sửa/xóa','Không phát hiện hoặc điều tra được sự cố','SOC','T05'),
 ('RR10','Sự cố khu vực ảnh hưởng cả DC và DR','Phân tích miền lỗi chung, bản sao và kế hoạch thay thế','Hai IDC cùng gián đoạn do điện/cáp/thiên tai hoặc nhà cung cấp','Chủ quản','T09 và diễn tập bàn')]

SERVICES=[
 ('DV01','IAM và quyền quản trị','IdP, Keystone, MFA, PAM','Nền tảng và đội vận hành'),
 ('DV02','Khóa và chứng thư','KMS/HSM, PKI, bản sao khóa','Mọi dữ liệu cần giải mã'),
 ('DV03','Điều khiển cloud','API, DB trạng thái, queue, SDN controller','Tenant và quản trị'),
 ('DV04','Máy ảo và container','Compute, network, image, storage','Khách hàng theo hợp đồng'),
 ('DV05','Dữ liệu và lưu trữ','Block, object, file, DB theo dịch vụ','Khách hàng và nền tảng'),
 ('DV06','DNS và thời gian','DNS nội bộ/công khai, NTP','Toàn nền tảng'),
 ('DV07','SOC và nhật ký','Collector, SIEM, kho log','Bảo vệ và điều tra'),
 ('DV08','Sao lưu và DR','Repository, replication, runbook','Khôi phục nền tảng và khách hàng'),
 ('DV09','Phát hành XOR','Git, CI/CD, registry, signing','Bản vá và nâng cấp nền tảng')]

if __name__=='__main__':
 TMP.mkdir(parents=True,exist_ok=True)
 (TMP/'controls.json').write_text(json.dumps(CONTROLS,ensure_ascii=False,indent=2),encoding='utf-8')
 (TMP/'data.json').write_text(json.dumps(dict(controls=CONTROLS,extra=EXTRA,dossier=DOSSIER,tests=TESTS,risks=RISKS,services=SERVICES,sources=SOURCES),ensure_ascii=False,indent=2),encoding='utf-8')
 print('Số điểm kiểm tra TCVN:',len(CONTROLS))
