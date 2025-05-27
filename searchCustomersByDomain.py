import os
import requests
from dotenv import load_dotenv
from readCustomerDomainsFromSheet import read_customer_domains
from extractDomains import extract_domain
from writeResultToCSV import write_result_to_csv

SEARCH_ORGS_CSV_FILE = "matchedLeadsRequery.csv"
SEARCH_ORGS_ID_COL_HEADER = "id"
SEARCH_DOMAIN_COL_HEADER = "search_domain"
CAUSE_IQ_ORGSEARCH_ENDPOINT = "https://www.causeiq.com/api/organizations"
OUTPUT_CSV_FILE = "leadRequeryMay27.csv"
# List of generic email domains - feel free to add here if more discovered.  We won't even attempt a causeIQ search for these domains
GENERIC_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "aol.com", "outlook.com",
    "icloud.com", "msn.com", "live.com", "comcast.net", "me.com",
    "mac.com", "att.net", "verizon.net", "mail.com", "yandex.com",
    "protonmail.com", "zoho.com", "gmx.com", "ymail.com", "cox.net",
    "rocketmail.com", "inbox.com"
}

# Load environment variables from .env file to get auth token
load_dotenv()
if not os.getenv("AUTH_TOKEN"):
    raise ValueError("AUTH_TOKEN is not set in the environment variables")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")


# get map from customer id to "unclean" domain
raw_domain_from_customer_id = read_customer_domains(SEARCH_ORGS_CSV_FILE, SEARCH_ORGS_ID_COL_HEADER, SEARCH_DOMAIN_COL_HEADER) 

# map from raw domain to "cleaned" domain
clean_domain_from_raw_domain = dict()
for raw_domain in raw_domain_from_customer_id.values():
    # Extract domain from the customer ID
    print(f"Extracting domain from: {raw_domain}")
    clean_domain = extract_domain(raw_domain)
    print(f"Extracted domain: {clean_domain}")
    clean_domain_from_raw_domain[raw_domain] = clean_domain

# map from "cleaned" domain to search result
search_result_from_clean_domain = dict()

# Function to search for a customer by domain, IF we didn't already search this domain
def search_customer(customer_id):

    # get the domain from the customer id
    raw_domain = raw_domain_from_customer_id[customer_id]
    print(f"Raw domain: {raw_domain}")
    # get clean domain from the customer id
    search_domain = clean_domain_from_raw_domain[raw_domain]
    
    # if we already searched this domain, use result we got before, and add to sheet
    if search_domain in search_result_from_clean_domain:
        print(f"Already searched {search_domain}, result is {search_result_from_clean_domain[search_domain]["value"]}")
        # append/write output to CSV file
        write_result_to_csv(customer_id, raw_domain, search_domain, 
                            search_result_from_clean_domain[search_domain]["value"],
                            search_result_from_clean_domain[search_domain]["org_name"],
                            search_result_from_clean_domain[search_domain]["address"],
                            OUTPUT_CSV_FILE, SEARCH_ORGS_ID_COL_HEADER, SEARCH_DOMAIN_COL_HEADER)
        return
    elif search_domain in GENERIC_DOMAINS:
        print(f"Domain {search_domain} is a generic domain, skipping search")
        # append/write output to CSV file
        write_result_to_csv(customer_id, raw_domain, search_domain, 
                            "generic","","",
                            OUTPUT_CSV_FILE, SEARCH_ORGS_ID_COL_HEADER, SEARCH_DOMAIN_COL_HEADER)
        return
    else:
        print(f"Searching for {search_domain}...")

        url = f"{CAUSE_IQ_ORGSEARCH_ENDPOINT}"
        headers = {
            "Authorization": f"Token {AUTH_TOKEN}"
        }  
        params = {
            "website_domain": search_domain
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:       
            data = response.json()
            if not data["results"]:
                print(f"No results found for {search_domain}")
                search_result_from_clean_domain[search_domain] = {
                    "value": "none",
                    "org_name": "",
                    "address": ""
                }
                # append/write output to CSV file
                write_result_to_csv(customer_id, raw_domain, search_domain, 
                                    "none","","",
                                    OUTPUT_CSV_FILE, SEARCH_ORGS_ID_COL_HEADER, SEARCH_DOMAIN_COL_HEADER)
                return
            else:
                # only keep result if there is one
                print(f"Results found for {search_domain}:")
                
                number_of_matches = data["total"]
                print(f"number of matches: {number_of_matches}")
                if number_of_matches > 1:
                    print("multiple matches found, not adding an EIN to results")
                    search_result_from_clean_domain[search_domain] = {
                        "value": "multiple",
                        "org_name": "",
                        "address": ""
                    }
                    # append/write output to CSV file
                    write_result_to_csv(customer_id, raw_domain, search_domain, 
                                        "multiple","","",
                                        OUTPUT_CSV_FILE, SEARCH_ORGS_ID_COL_HEADER, SEARCH_DOMAIN_COL_HEADER)                    
                else: 
                    ein = data["results"][0]["ein"]
                    org_name = data["results"][0]["name"]
                    address = data["results"][0]["address"]
                    search_result_from_clean_domain[search_domain] = {
                        "value": ein,
                        "org_name": org_name,
                        "address": address
                    }
                    print(ein)
                    # append/write output to CSV file
                    write_result_to_csv(customer_id, raw_domain, search_domain, 
                                        ein, org_name, address, 
                                        OUTPUT_CSV_FILE, SEARCH_ORGS_ID_COL_HEADER, SEARCH_DOMAIN_COL_HEADER)

        else:
            print(f"Error ({response.status_code}): {response.text}")

# loop through each id in the list and search it
for id in raw_domain_from_customer_id.keys():
    print(f"Searching for customer: {id}")
    search_customer(id)