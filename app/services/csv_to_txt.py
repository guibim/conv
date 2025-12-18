from app.services.utils.csv_reader import read_csv_with_fallback


def convert_csv_to_txt(input_path, output_path):
    rows = read_csv_with_fallback(input_path)

    with open(output_path, "w", encoding="utf-8") as txtfile:
        for row in rows:
            txtfile.write(" | ".join(row) + "\n")
