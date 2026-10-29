from pathlib import Path
import shutil

root=Path('/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud')
tmp=root/'tmp/ho-so-v2-3'
shutil.copy2(root/'tmp/ho-so-v2/data.json',tmp/'data.json')
for name in ['build_workbook.mjs','build_source_workbook.mjs']:
    source=root/'tmp/ho-so-v2'/name if name=='build_workbook.mjs' else tmp/name
    text=source.read_text()
    text=text.replace("tmp/ho-so-v2'","tmp/ho-so-v2-3'").replace('output/XOR-Ho-so-CD4-v2/','output/XOR-Ho-so-CD4-v2.3/')
    text=text.replace("'Arial'","'Times New Roman'")
    colors={'#203247':'#000000','#20262D':'#000000','#203E59':'#FFFFFF','#F2F5F8':'#FFFFFF','#F4F7FA':'#FFFFFF','#FFF5D6':'#F2F2F2','#FFF2CC':'#F2F2F2','#E7F0EB':'#FFFFFF','#FCE5E3':'#D9D9D9','#FFF1CF':'#ECECEC','#E9ECEF':'#F2F2F2','#FCE4D6':'#D9D9D9','#9C2727':'#000000','#9C0006':'#000000','#9C6500':'#000000'}
    for a,b in colors.items():text=text.replace(a,b)
    text=text.replace("color:'#FFFFFF'","color:'#000000'").replace("tabColor='#FFFFFF'","tabColor='#666666'")
    text=text.replace('Ô vàng','Ô nền xám nhạt')
    text=text.replace("table.showFilterButton=true;","table.showFilterButton=true;table.style='TableStyleLight1';s.getRange(`A5:${last}${end}`).format.borders={preset:'all',style:'thin',color:'#000000'};")
    text=text.replace('t.showFilterButton=true;',"t.showFilterButton=true;t.style='TableStyleLight1';s.getRange(`A8:${end}${last}`).format.borders={preset:'all',style:'thin',color:'#000000'};")
    text=text.replace('Chờ đúng tệp Word người dùng viện dẫn. Không tự suy diễn tên pháp nhân, người ký hoặc quyền ký từ thương hiệu XOR.','Thông tin pháp nhân và nhân sự tham chiếu Word v0.9.4; đơn vị vận hành theo xác nhận của chủ quản là Khối Hạ tầng & Vận hành. Mã số doanh nghiệp, hồ sơ phân công và quyền ký vẫn cần xác minh trước trình ký.')
    (tmp/name).write_text(text)
