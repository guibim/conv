import io
import zipfile
from xml.sax.saxutils import escape

from app.services.utils.csv_reader import read_csv_with_fallback

CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>"""

ROOT_RELS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

WORKBOOK_XML = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheets>
        <sheet name="Sheet1" sheetId="1" r:id="rId1" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
    </sheets>
</workbook>"""

WORKBOOK_RELS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>"""


def csv_to_xlsx(csv_bytes: bytes) -> bytes:
    rows = read_csv_with_fallback(csv_bytes)

    def cell_xml(value):
        return f'<c t="inlineStr"><is><t>{escape(value)}</t></is></c>'

    sheet_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = "".join(cell_xml(col) for col in row)
        sheet_rows.append(f'<row r="{r_idx}">{cells}</row>')

    sheet_xml = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
        "  <sheetData>"
        f"    {''.join(sheet_rows)}"
        "  </sheetData>"
        "</worksheet>"
    )

    with io.BytesIO() as output:
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
            z.writestr("_rels/.rels", ROOT_RELS_XML)
            z.writestr("xl/workbook.xml", WORKBOOK_XML)
            z.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS_XML)
            z.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        return output.getvalue()
