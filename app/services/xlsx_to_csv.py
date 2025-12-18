import zipfile
import io
import csv
from xml.etree import ElementTree as ET

def xlsx_to_csv(xlsx_bytes: bytes) -> bytes:
    with zipfile.ZipFile(io.BytesIO(xlsx_bytes)) as z:
        sheet = z.read("xl/worksheets/sheet1.xml")

    ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    root = ET.fromstring(sheet)

    output = io.StringIO()
    writer = csv.writer(output)

    for row in root.findall(".//a:row", ns):
        values = []
        for c in row.findall("a:c", ns):
            t = c.get("t")
            if t == "inlineStr":
                v = c.find(".//a:t", ns)
                values.append(v.text if v is not None else "")
            else:
                v = c.find("a:v", ns)
                values.append(v.text if v is not None else "")
        writer.writerow(values)

    return output.getvalue().encode("utf-8")
