import csv

def convert_csv_to_html(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    html = "<html><body><table border='1'>\n"

    for row in rows:
        html += "<tr>"
        for cell in row:
            html += f"<td>{cell}</td>"
        html += "</tr>\n"

    html += "</table></body></html>"

    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html)
