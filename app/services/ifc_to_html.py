import re

def convert_ifc_to_html(input_path: str, output_path: str):
    entity_count = {}

    with open(input_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            match = re.search(r"=IFC([A-Z0-9_]+)\(", line)
            if match:
                entity = f"IFC{match.group(1)}"
                entity_count[entity] = entity_count.get(entity, 0) + 1

    rows = "".join(
        f"<tr><td>{entity}</td><td>{count}</td></tr>"
        for entity, count in sorted(entity_count.items())
    )

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>BIM Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        table {{ border-collapse: collapse; width: 60%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Resumo do Modelo BIM</h1>
    <table>
        <tr><th>Entidade</th><th>Quantidade</th></tr>
        {rows}
    </table>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as out:
        out.write(html)
