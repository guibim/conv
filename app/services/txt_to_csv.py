import csv

def convert_txt_to_csv(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as txt_file:
        lines = txt_file.readlines()

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for line in lines:
            writer.writerow([line.strip()])
