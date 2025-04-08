import csv

# Function to read search domains from CSV 
def read_customer_domains(csv_filename, search_domain_file_header="search_domain") -> list:
    search_domains = []
    with open(csv_filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Reads CSV into a dictionary format
        for row in reader:
            search_domains.append(row[search_domain_file_header])  
    return search_domains