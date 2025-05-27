import csv

def write_result_to_csv(customer_id, raw_domain, 
                        search_domain, ein_result, org_name_result, address_result,
                        OUTPUT_CSV_FILE, SEARCH_ORGS_ID_COL_HEADER, SEARCH_DOMAIN_COL_HEADER):
    with open(OUTPUT_CSV_FILE, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=[SEARCH_ORGS_ID_COL_HEADER,SEARCH_DOMAIN_COL_HEADER,
                                                  "search_domain", "ein", "org_name_from_search", 
                                                  "address_street_from_search", "address_city_from_search", 
                                                  "address_state_from_search", "address_zip_from_search"])

        # Only write header if file is empty
        if file.tell() == 0:
            writer.writeheader()

        # null-check org_name and address components
        if org_name_result is None:
            org_name_result = ""
        address_street = ""
        address_city = ""
        address_state = "" 
        address_zip = ""
        if address_result is not None and address_result != "" and isinstance(address_result, dict):
            address_street = address_result.get("street", "")
            address_city = address_result.get("city", "")
            address_state = address_result.get("state", "")
            address_zip = address_result.get("zip", "")

        # Write the row to the CSV file
        writer.writerow({
            # source data
            SEARCH_ORGS_ID_COL_HEADER: customer_id,
            SEARCH_DOMAIN_COL_HEADER: raw_domain, 
            
            # search results
            "search_domain": search_domain,
            "ein": f"'{ein_result}",  # fstring to ensure leading zeroes are preserved
            "org_name_from_search": org_name_result,
            "address_street_from_search": address_street,
            "address_city_from_search": address_city,
            "address_state_from_search": address_state,
            "address_zip_from_search": address_zip
        })