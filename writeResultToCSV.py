import csv

def write_result_to_csv(customer_id, raw_domain, search_domain, result, 
                        OUTPUT_CSV_FILE, SEARCH_ORGS_ID_COL_HEADER, SEARCH_DOMAIN_COL_HEADER):
    with open(OUTPUT_CSV_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[SEARCH_ORGS_ID_COL_HEADER,SEARCH_DOMAIN_COL_HEADER, "domain", "ein"])

        # Only write header if file is empty
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow({
            SEARCH_ORGS_ID_COL_HEADER: customer_id,
            SEARCH_DOMAIN_COL_HEADER: raw_domain, 
            "domain": search_domain,
            "ein": result
        })