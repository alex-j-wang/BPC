import csv

def print_rows_with_has_box_true(csv_path):
    with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("has_box", "").strip().lower() == "true":
                print(row.get("id", ""))

# 🔧 Replace with your file path
print_rows_with_has_box_true("bph_site_team.csv")