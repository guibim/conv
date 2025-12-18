import csv
import io
import zipfile
from xml.sax.saxutils import escape

def csv_to_xlsx(csv_bytes: bytes) -> bytes:
    csv_text = csv_bytes.decode("utf-8", errors="ignore")
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)

    def cell_xml(value):
        return f'<c t="inlineStr"><is><t>{escape(value)}</t></is></c>'

    sheet_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = "".join(cell_xml(col) for col in row)
        sheet_rows.append(f'<row r="{r_idx}">{cells}</row>')

    sheet_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    {''.join(sheet_rows)}
  </sheetData>
</worksheet>'''

    with io.BytesIO() as output:
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
            z.writestr("_rels/.rels", ROOT_RELS_XML)
            z.writestr("xl/workbook.xml", WORKBOOK_XML)
            z.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS_XML)
            z.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        return output.getvalue()
