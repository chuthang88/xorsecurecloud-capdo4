from pathlib import Path
import json,shutil,zipfile,hashlib
root=Path('/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud')
tmp=Path(__file__).parent
out=root/'output/XOR-Ho-so-CD4-v2.3'
qa=json.loads((tmp/'final-qa.json').read_text())
assert qa['totalPages']==110
text=(root/'output/XOR-Ho-so-CD4-v2.2/Bo-1-Ky-thuat/DOC_TRUOC_KHI_SU_DUNG.txt').read_text()
text=text.replace('Phiên bản bộ hồ sơ 2.2','Phiên bản bộ hồ sơ 2.3').replace('13 trang, phân công','14 trang, phân công').replace('5 trang; BOM','6 trang; BOM').replace('tổng cộng 84 trang','tổng cộng 90 trang')
text=text.replace('Nội dung workbook này giữ nguyên bản đã kiểm tra trước; dùng làm bảng yêu cầu chính.','Giữ nguyên các yêu cầu và công thức; dùng làm bảng yêu cầu chính. Ô nền xám nhạt là nơi nhập dữ liệu.')
text=text.replace('\nBỘ 1 KỸ THUẬT','\nTRÌNH BÀY PHIÊN BẢN 2.3\nÁp dụng phong cách từ mẫu De an_xCommandCenter_v2 (1).pdf: Times New Roman, A4, bìa căn giữa, thân bài căn đều và thụt đầu dòng; tiêu đề đen đậm; bảng viền mảnh; chú thích hình in nghiêng; số trang ở giữa chân trang. Sơ đồ dùng khối trắng, nét và mũi tên đen, khung kép cho thành phần trọng tâm. Excel dùng Times New Roman, bảng đen trắng và ô nhập nền xám nhạt.\nNội dung mẫu xCommandCenter không được đưa vào hồ sơ XOR. Bản Word v0.9.4 vẫn là tài liệu tham khảo nội dung. Giữ các mục cần xác minh và không chuyển trạng thái lịch sử thành kết quả hiện tại.\n13 tài liệu Word, tổng cộng 110 trang; 2 workbook, tổng cộng 12 trang tính.\n\nBỘ 1 KỸ THUẬT')
for folder in [out,out/'Bo-1-Ky-thuat',out/'Bo-2-Hanh-chinh']:
 (folder/'DOC_TRUOC_KHI_SU_DUNG.txt').write_text(text)
for p in out.rglob('*.inspect.ndjson'):shutil.move(str(p),str(tmp/p.name))
archives=[]
for name,count in [('Bo-1-Ky-thuat',7),('Bo-2-Hanh-chinh',14)]:
 folder=out/name;files=sorted(p for p in folder.iterdir() if p.is_file());assert len(files)==count,(name,len(files))
 archive=out/f'{name}-XOR-CD4-v2.3.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in files:
   if p.suffix in ['.docx','.xlsx']:
    with zipfile.ZipFile(p) as inner:assert inner.testzip() is None,p
   z.write(p,str(p.relative_to(out)))
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 archives.append({'path':str(archive),'files':len(files),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
qa['archives']=archives
(tmp/'final-qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
print(json.dumps(archives,ensure_ascii=False,indent=2))
