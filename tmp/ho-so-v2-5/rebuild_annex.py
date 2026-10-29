from doc_base import *
from inventory_data import *
from docx.enum.section import WD_SECTION_START
exec((TMP/'build_annex.py').read_text(),globals())
