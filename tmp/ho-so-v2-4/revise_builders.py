from pathlib import Path
import shutil
P=Path(__file__).parent
old=P.parent/'ho-so-v2-3'
for name in ['content.py','build_docs.py','doc_style.py','supplement.py']:
 s=(old/name).read_text().replace('XOR-Ho-so-CD4-v2.3','XOR-Ho-so-CD4-v2.4').replace('ho-so-v2-3','ho-so-v2-4').replace('bản dự thảo 2.3','phiên bản 2.4').replace('Bản dự thảo 2.3','Phiên bản 2.4')
 (P/name).write_text(s)
shutil.copy2(old/'source-controls.json',P/'source-controls.json')
# Reference typography; remove drafting labels and generic signing directions.
p=P/'doc_style.py';s=p.read_text();s=s.replace("h.text='DỰ THẢO CHƯA KÝ BAN HÀNH'","h.text=''")
s=s.replace("c('Nền tảng XOR STACK CLOUD dựa trên OpenStack',13,after=56)","c('Nền tảng XOR STACK CLOUD',13,after=56)")
s=s.replace("c('Phiên bản 2.4 chưa ký ban hành',12,italic=True,after=42)","c('',12,after=42)")
s=s.replace('super().letterhead(*a,**kw)',"a=list(a)\n   if len(a)>3:a[3]=None\n   kw.pop('model',None)\n   super().letterhead(*a,**kw)")
# New landscape figure section helper.
insert='''  def topology(self):
   for i,name in enumerate(['01_Topo_tong_the_DC_DR','02_Topo_phan_vung_va_luong']):
    sec=self.doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec.page_width=Cm(29.7);sec.page_height=Cm(21)
    sec.left_margin=sec.right_margin=Cm(2);sec.top_margin=sec.bottom_margin=Cm(1.5)
    sec.orientation=1
    for n in list(sec._sectPr.findall(qn('w:pgNumType'))):sec._sectPr.remove(n)
    self.h('2 '+('Phương án kiến trúc tổng thể DC–DR' if i==0 else 'Phương án phân vùng mạng và kết nối'),2)
    p=self.doc.add_paragraph();p.paragraph_format.first_line_indent=Cm(0);p.paragraph_format.line_spacing=1;p.paragraph_format.space_after=Pt(0)
    p.add_run().add_picture(str(__import__('pathlib').Path(__file__).parent/(name+'.png')),width=Cm(25.3))
    cap=self.p('Hình '+str(i+1)+'. '+('Kiến trúc tổng thể hệ thống XOR SECURE CLOUD.' if i==0 else 'Phân vùng mạng và các luồng kết nối chính.'),style='Caption')
    cap.paragraph_format.space_after=Pt(0)
   sec=self.doc.add_section(WD_SECTION_START.NEW_PAGE)
   sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.orientation=0
   sec.left_margin=Cm(3);sec.right_margin=Cm(2);sec.top_margin=sec.bottom_margin=Cm(2)
   for n in list(sec._sectPr.findall(qn('w:pgNumType'))):sec._sectPr.remove(n)
'''
s=s.replace('  def save(self,path):',insert+'  def save(self,path):')
p.write_text(s)
p=P/'build_docs.py';s=p.read_text()
s=s.replace("DRAFT='DỰ THẢO ĐỂ RÀ SOÁT VÀ HOÀN THIỆN   •   CHƯA KÝ BAN HÀNH'","DRAFT=''")
s=s.replace("Nền tảng XOR STACK CLOUD dựa trên OpenStack","Nền tảng XOR STACK CLOUD").replace("XOR STACK CLOUD do XOR CLOUD phát triển lại và đóng gói từ OpenStack.","Nền tảng XOR STACK CLOUD.")
s=s.replace("(Ký, ghi rõ họ tên và đóng dấu theo thẩm quyền)","")
s=s.replace("[Địa danh], ngày [  ] tháng [  ] năm [  ]","Hà Nội, ngày [  ] tháng [  ] năm [  ]")
a=s.index('# HƯỚNG DẪN BỘ 2');b=s.index('# THUYẾT MINH CHÍNH')
s=s[:a]+'''# DANH MỤC HỒ SƠ
d=Doc('Danh mục hồ sơ đề xuất cấp độ 4')
d.p('CÔNG TY CỔ PHẦN XOR CLOUD',True,align=WD_ALIGN_PARAGRAPH.CENTER)
d.p('DANH MỤC HỒ SƠ',True,align=WD_ALIGN_PARAGRAPH.CENTER)
d.p('Đề xuất cấp độ 4 hệ thống thông tin XOR SECURE CLOUD',True,align=WD_ALIGN_PARAGRAPH.CENTER)
d.p('Chủ quản: '+ORG+'. Đơn vị vận hành: '+OPERATOR+'.')
d.p('Mã hồ sơ: XOR-CD4. Phiên bản: 2.4. Ngày lập: [CẦN ĐIỀN].')
files=[('01','Thuyết minh hồ sơ đề xuất cấp độ 4'),('02','Phụ lục đối chiếu yêu cầu TCVN'),('03','Quy chế và quy trình bảo đảm an ninh mạng'),('04','Công văn xin ý kiến chuyên môn'),('05','Công văn đề nghị thẩm định'),('06','Tờ trình phê duyệt cấp độ'),('07','Quyết định phê duyệt cấp độ'),('08','Ý kiến chuyên môn'),('09','Báo cáo kết quả rà soát'),('10','Phụ lục thiết kế và hiện trạng'),('11','Công văn đề nghị đánh giá độc lập'),('12','Thông báo về cấp độ hệ thống thông tin')]
d.table(['STT','Tên tài liệu','Số / ngày văn bản'],[(n,t,'[CẦN ĐIỀN]') for n,t in files],[.45,2.9,1.1])
d.p('Tài liệu kèm theo: [CẦN ĐIỀN danh mục thiết kế được phê duyệt, ý kiến thẩm định, bằng chứng đánh giá và tài liệu pháp lý; số, ngày, phiên bản, số trang].')
d.p('Đầu mối: '+AUTHOR_NAME+' — '+AUTHOR_ROLE+'. Liên hệ: [CẦN ĐIỀN điện thoại, email].')
d.save(ADMIN/'00_Danh_muc_ho_so.docx')

'''+s[b:]
# Rewrite complete paragraphs by distinctive prefix; matching full literal from AST is safer than partial fragments.
import ast
replacements={
 'Hồ sơ trình bày phương án đề xuất':'Hồ sơ đề xuất cấp độ 4 đối với toàn bộ nền tảng XOR SECURE CLOUD và các dịch vụ quản trị chung, bao gồm thuyết minh hệ thống, phương án thiết kế, đánh giá rủi ro và phương án bảo đảm an ninh mạng.',
 'TCVN 14423:2026, Điều 6 và Phụ lục A.4 được':'Phương án bảo đảm an ninh mạng được đối chiếu với Điều 6 và Phụ lục A.4 TCVN 14423:2026. [S1, Điều 21–22; S2]',
 'XOR SECURE CLOUD là hệ thống cung cấp':'XOR SECURE CLOUD là hệ thống cung cấp và quản lý tài nguyên điện toán đám mây trên nền tảng XOR STACK CLOUD. Phạm vi hồ sơ gồm hạ tầng, phần mềm nền tảng và các dịch vụ quản trị chung tại Trung tâm Hạ tầng IDC Cầu Giấy (DC) và Trung tâm Hạ tầng IDC Nam Thăng Long (DR).',
 'Đối với hệ thống đang vận hành, tài liệu kèm':'Thiết kế hệ thống gồm kiến trúc tổng thể DC–DR, phân vùng mạng, các luồng kết nối, hạ tầng vật lý và các thành phần quản trị. Hồ sơ thiết kế được phê duyệt hoặc tài liệu có giá trị tương đương: [CẦN ĐIỀN tên, số, ngày, cơ quan phê duyệt và danh mục bản vẽ]. [S1, Điều 21.2 b]',
 'Trạng thái hiện tại: [CẦN ĐÍNH':'Hiện trạng triển khai: [CẦN ĐIỀN số, ngày hồ sơ kiểm kê/nghiệm thu; phiên bản cấu hình; sai khác giữa thiết kế và hiện trạng; mã tài liệu tại PL01–PL07].',
 'XOR SECURE CLOUD được đề xuất xem xét':'XOR SECURE CLOUD thuộc loại hệ thống cơ sở hạ tầng thông tin cung cấp tài nguyên điện toán đám mây. Cấp độ đề xuất: cấp độ 4. Chức năng, phạm vi phục vụ, loại thông tin và hậu quả rủi ro được thuyết minh theo Điều 14 và Điều 22 Nghị định 331/2026/NĐ-CP.',
 'Tiêu chí được chọn để trình:':'Tiêu chí đề xuất cấp độ: [CẦN ĐIỀN khoản áp dụng tại Điều 14]. Căn cứ và tài liệu chứng minh: [CẦN ĐIỀN phạm vi phục vụ, hợp đồng, BIA, kết quả đánh giá rủi ro và mã tài liệu].',
 'Phương pháp nội bộ đề xuất gồm:':'Phương pháp đánh giá rủi ro gồm xác định tài sản và dịch vụ; nhận diện mối đe dọa, điểm yếu; xác định khả năng và tác động; đánh giá hiệu lực kiểm soát; lựa chọn biện pháp xử lý; đánh giá rủi ro còn lại và phê duyệt. [CẦN ĐIỀN phương pháp, thang điểm và văn bản phê duyệt áp dụng]. [S1, Điều 22.5; S2, 6.1]',
 'Điểm, căn cứ và rủi ro còn lại:':'Kết quả đánh giá rủi ro: [CẦN ĐIỀN tài sản, mức khả năng, mức tác động, căn cứ chấm điểm, biện pháp xử lý, rủi ro còn lại, người chịu trách nhiệm, thời hạn và quyết định chấp nhận].',
 'Đối với từng dịch vụ thiết yếu, cần lượng hóa':'Phân tích tác động nghiệp vụ xác định số khách hàng và hệ thống bị ảnh hưởng; nguy cơ mất, lộ, sửa dữ liệu; thời gian gián đoạn; hậu quả tài chính, pháp lý và tác động đối với lợi ích công cộng, trật tự, an toàn xã hội, an ninh quốc gia. [CẦN ĐIỀN báo cáo BIA, số liệu, nguồn và người xác nhận]. [S1, Điều 22.5 b c]',
 'Nếu viện dẫn Điều 14 khoản 2, thuyết minh':'Yêu cầu hoạt động liên tục: [CẦN ĐIỀN nghĩa vụ 24/7; điều kiện về ngừng vận hành có kế hoạch và không có kế hoạch; bên yêu cầu, phạm vi dịch vụ, tác động và biện pháp đáp ứng]. [S1, Điều 22.5 d]',
 'Phương án đối với từng yêu cầu TCVN được':'Phương án đối với từng yêu cầu TCVN được xác định tại Phụ lục đối chiếu yêu cầu và phương án bảo đảm an ninh mạng. Quy chế và quy trình quy định trách nhiệm, trình tự thực hiện và hồ sơ lưu. Hiện trạng và kết quả kiểm tra: [CẦN ĐIỀN ngày chốt, danh mục cấu hình, văn bản ban hành, biên bản kiểm tra và mã bằng chứng]. [S1, Điều 22.6]',
 'Trường hợp tiêu chuẩn cho phép phương án tương đương,':'Giải pháp tương đương được đánh giá theo yêu cầu áp dụng, rủi ro, kiến trúc kiểm soát, khả năng bảo vệ, giới hạn, kết quả thử nghiệm và thẩm quyền chấp thuận. Hồ sơ giải pháp tương đương: [CẦN ĐIỀN mã yêu cầu, thuyết minh, kết quả kiểm chứng và văn bản chấp thuận nếu áp dụng].',
 'Các yêu cầu A.4 được kiểm tra riêng':'Phương án bảo đảm an toàn vật lý áp dụng riêng tại DC Cầu Giấy và DR Nam Thăng Long theo Phụ lục A.4. Phạm vi kiểm soát gồm phòng máy, rack thiết bị, điện/UPS, phòng cháy và chữa cháy, chống sét, chống nước, tĩnh điện, môi trường, bảo vệ điện từ, camera và kiểm soát ra vào. Hồ sơ đối chiếu của từng IDC: [CẦN ĐIỀN hợp đồng, phạm vi, thời hạn hiệu lực, biên bản kiểm tra và mã bằng chứng].',
 'Phụ lục ánh xạ 119 điểm kiểm tra':'Phụ lục đối chiếu 119 nội dung kiểm tra thuộc Điều 6.1–6.18 và Phụ lục A.4 TCVN 14423:2026 với phương án bảo đảm an ninh mạng của hệ thống XOR SECURE CLOUD.',
 'Phương án tại cột thứ ba là nội dung':'Thời điểm chốt hiện trạng: [CẦN ĐIỀN]. Hồ sơ kiểm tra và bằng chứng kèm theo: [CẦN ĐIỀN danh mục, phiên bản, người lập và người xác nhận].',
 'Danh mục tồn tại và kế hoạch khắc phục:':'Danh mục tồn tại và kế hoạch khắc phục: [CẦN ĐIỀN mã yêu cầu, nguyên nhân, mức rủi ro, biện pháp tạm thời, hành động, người chịu trách nhiệm và thời hạn].',
 '[S2] TCVN 14423:2026: Điều 6':'[S2] TCVN 14423:2026: Điều 6, trang 58–81; Phụ lục A.4, trang 109–111.',
}
# Remove drafting commentary only; retain all requirements and control rows.
remove_prefixes=['Các chỉ tiêu RPO 15 phút/RTO 4 giờ từng nêu','Ý kiến thẩm định HS07 phải do cơ quan có thẩm quyền']
lines=s.splitlines();out=[]
for line in lines:
 st=line.strip()
 if st.startswith('d.p('):
  try:node=ast.parse(st).body[0].value;v=ast.literal_eval(node.args[0])
  except Exception:v=None
  if isinstance(v,str):
   if any(v.startswith(x) for x in remove_prefixes):continue
   for pre,new in replacements.items():
    if v.startswith(pre):
     line=line.replace(repr(v),repr(new));break
 out.append(line)
s='\n'.join(out)+'\n'
# Targeted wording throughout.
r={
 'Người ký dự kiến của chủ quản':'Đại diện chủ quản',
 'Phạm vi kỹ thuật dự kiến bao gồm':'Phạm vi kỹ thuật bao gồm',
 'Danh mục dịch vụ được cung cấp thực tế và các thành phần thuê ngoài được chốt tại':'Danh mục dịch vụ và các thành phần thuê ngoài được xác định tại',
 'Trường bắt buộc':'Nội dung',
 'Số liệu phải điền và tài liệu chứng minh':'Thông tin và tài liệu chứng minh',
 'Hệ thống Neutron/SDN':'Hệ thống mạng ảo hóa/SDN',
 'Không mặc định kéo dài một cụm đồng thuận hoặc miền lỗi duy nhất qua DC và DR.':'Cụm đồng thuận được thiết lập trong từng IDC; rủi ro miền lỗi chung giữa hai IDC được đánh giá trong phương án DR.',
 'Các nội dung kỹ thuật nêu trên là phương án đề xuất, cần đối chiếu bằng chứng triển khai và biên bản T07–T10.':'[CẦN ĐIỀN mã bằng chứng triển khai và biên bản kiểm thử T07–T10].',
 'Đối với cơ chế kiểm soát rủi ro tương đương phải có phân tích và bằng chứng kiểm chứng, không chỉ ghi tên giải pháp.':'Giải pháp kiểm soát tương đương được thuyết minh và kiểm chứng theo phạm vi áp dụng.',
 'Chưa có bằng chứng; không tự khai có.':'[CẦN XÁC NHẬN áp dụng và mã bằng chứng]',
 'Tiêu chí cần xem xét; chưa được xác nhận.':'[CẦN XÁC NHẬN áp dụng và mã bằng chứng]',
 'Chưa có thông tin áp dụng.':'[CẦN XÁC NHẬN áp dụng và mã bằng chứng]',
 'Chỉ viện dẫn khi có căn cứ hợp lệ.':'[CẦN ĐIỀN văn bản làm căn cứ nếu áp dụng]',
 'nếu thực tế có phục vụ.':'[CẦN ĐIỀN phạm vi phục vụ nếu áp dụng].',
 'Cần phạm vi khách hàng, nghĩa vụ dịch vụ và BIA.':'Phạm vi khách hàng, nghĩa vụ dịch vụ và BIA: [CẦN ĐIỀN].',
 'Đối chiếu PL04 và BIA để không bỏ sót các phụ thuộc IAM, DNS, khóa, ISP, IDC và nhà cung cấp.':'Các phụ thuộc IAM, DNS, khóa, ISP, IDC và nhà cung cấp được xác định tại PL04 và BIA.',
 'SSDLC cho bản fork XOR':'Phát triển an toàn phần mềm nền tảng XOR',
 'TCVN/Cloud;':'TCVN;',
 'Lập một phiếu cho từng đối tượng; bổ sung số thứ tự khi có nhiều bản ghi.':'',
 'Nội dung hiện trạng cần hoàn thiện':'Thông tin hiện trạng',
 '[OpenStack upstream; phiên bản XOR; commit/tag; digest]':'[CẦN ĐIỀN nguồn phần mềm; phiên bản XOR; commit/tag; digest]',
 '[CẦN ĐIỀN; không gộp nhiều thiết bị khác cấu hình]':'[CẦN ĐIỀN mã tài sản, loại và vai trò]',
 'Đầu mối đề xuất: ':'Đơn vị chủ trì: ',
 'Dự thảo kèm quyết định ban hành của chủ quản':'Kèm theo Quyết định số [CẦN ĐIỀN] ngày [CẦN ĐIỀN]',
 '. Quy chế chỉ có hiệu lực theo văn bản ban hành hợp lệ; nội dung dự thảo phải được rà soát phù hợp tổ chức, hợp đồng và cấu hình thực tế trước khi ký.':'.',
 'Việc mua sắm thiết bị hoặc ban hành quy trình không thay thế trách nhiệm triển khai và duy trì hiệu lực.':'Các đơn vị được giao nhiệm vụ chịu trách nhiệm triển khai và duy trì hiệu lực của biện pháp bảo vệ.',
 '[đầu mối tiếp nhận theo hướng dẫn hiện hành]':'[CẦN ĐIỀN đơn vị tiếp nhận]',
 '[CẦN ĐIỀN cụ thể, không bỏ trống hoặc ghi đã hoàn thành khi chưa có bằng chứng]':'[CẦN ĐIỀN nội dung tiếp thu, tình trạng thực hiện và mã bằng chứng]',
 'Dự thảo quyết định phê duyệt cấp độ hệ thống thông tin':'Quyết định phê duyệt cấp độ hệ thống thông tin',
 '[CẦN ĐIỀN nếu có; không tự bỏ điều kiện của cơ quan thẩm định]':'[CẦN ĐIỀN điều kiện và yêu cầu theo ý kiến thẩm định]',
 '07_Du_thao_Quyet_dinh_phe_duyet_Mau_06.docx':'07_Quyet_dinh_phe_duyet_cap_do.docx',
 '04_Cong_van_xin_y_kien_chuyen_mon_Mau_03.docx':'04_Cong_van_xin_y_kien_chuyen_mon.docx',
 '05_Cong_van_de_nghi_tham_dinh_Mau_02.docx':'05_Cong_van_de_nghi_tham_dinh.docx',
 '06_To_trinh_phe_duyet_Mau_05.docx':'06_To_trinh_phe_duyet.docx',
}
for a,b in r.items():s=s.replace(a,b)
s=s.replace(". Tư cách chủ quản, nhiệm vụ vận hành/chuyên trách và thẩm quyền ký phải kèm văn bản phân công hoặc ủy quyền phù hợp; xác nhận cơ chế kiểm tra độc lập trước khi trình.",". [CẦN ĐIỀN số, ngày văn bản xác định tư cách chủ quản, giao nhiệm vụ vận hành/chuyên trách, thẩm quyền ký và cơ chế kiểm tra độc lập].")
a=s.index("d.page('2 Sơ đồ kiến trúc tham chiếu')");b=s.index("d.page('3 Phương án phân vùng và luồng kết nối')",a)
s=s[:a]+"d.topology()\n"+s[b:].replace("d.page('3 Phương án phân vùng và luồng kết nối')","d.h('3 Phương án phân vùng và luồng kết nối',1)",1)
# Technical handbook uses the same two revised figures.
a=s.find("pic=TMP/'So_do_kien_truc_muc_tieu.png'")
if a>=0:
 b=s.index('\n',s.index("style='Caption')",a))+1
 s=s[:a]+"d.topology()\n"+s[b:]
# Split individual official texts in a separate module.
a=s.index('# Ý KIẾN CHUYÊN MÔN VÀ BÁO CÁO TỰ RÀ SOÁT');b=s.index("exec((TMP/'supplement.py')",a)
s=s[:a]+"exec((TMP/'official_forms.py').read_text(), globals())\n\n"+s[b:]
a=s.index('# Tài liệu chỉ dẫn và sơ đồ dùng chung')
s=s[:a]+'''for folder in [TECH,ADMIN]:
 for name in ['01_Topo_tong_the_DC_DR','02_Topo_phan_vung_va_luong']:
  for ext in ['svg','png']:shutil.copy2(TMP/(name+'.'+ext),folder/(name+'.'+ext))
(TMP/'doc_manifest.json').write_text(json.dumps(CREATED,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(CREATED)==15,len(CREATED)
print(json.dumps({'docx_count':len(CREATED),'files':CREATED},ensure_ascii=False,indent=2))
'''
p.write_text(s)
# Keep the technical source reconciliation intact; replace the outward appendix.
p=P/'supplement.py';s=p.read_text();a=s.index("d=Doc('Phụ lục đối chiếu thiết kế")
s=s[:a]+"exec((TMP/'formal_annex.py').read_text(), globals())\n"
s=s.replace('OpenStack API private','XOR STACK API nội bộ')
p.write_text(s)
# Primary source reference retains formal citations without editorial notes in outward docs.
p=P/'build_docs.py';s=p.read_text();s=s.replace("d.h('Nguồn tham chiếu')","d.h('Tài liệu tham chiếu')")
p.write_text(s)
