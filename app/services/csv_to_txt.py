import csv

def convert_csv_to_txt(input_path, output_path):
    with open(input_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        with open(output_path, "w", encoding="utf-8") as txtfile:
            for row in reader:
                txtfile.write(" | ".join(row) + "\n")
