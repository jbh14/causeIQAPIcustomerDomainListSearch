import csv

# Function to read search domains from CSV 
def read_customer_domains(csv_filename, id_file_header="id", search_domain_file_header="search_domain") -> list:
    domain_from_customer_id = dict()
    with open(csv_filename, mode="r", encoding="utf-8-sig", errors="replace") as file:
        reader = csv.DictReader(file)  # Reads CSV into a dictionary format
        for row in reader:
            print(f"Row: {row}")
            print(f"Row ID: {row[id_file_header]}")
            print(f"Row Domain: {row[search_domain_file_header]}")
            domain_from_customer_id[row[id_file_header]] = row[search_domain_file_header]
            
    return domain_from_customer_id