import os
import requests
import base64
import csv
from dotenv import load_dotenv
from readCustomerDomainsFromSheet import read_customer_domains
from extractDomains import extract_domain

SEARCH_ORGS_CSV_FILE = "someOrgsToSearch.csv"
SEARCH_ORGS_ID_COL_HEADER = "id"
SEARCH_DOMAIN_COL_HEADER = "search_domain"
CAUSE_IQ_ORGSEARCH_ENDPOINT = "https://www.causeiq.com/api/organizations"
OUTPUT_CSV_FILE = "results.csv"

# Load environment variables from .env file to get auth token
load_dotenv()
if not os.getenv("AUTH_TOKEN"):
    raise ValueError("AUTH_TOKEN is not set in the environment variables")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# get map from customer id to "unclean" domain
raw_domain_from_customer_id = read_customer_domains(SEARCH_ORGS_CSV_FILE, SEARCH_DOMAIN_COL_HEADER) 

# map from raw domain to "cleaned" domain
clean_domain_from_raw_domain = dict()
for raw_domain in raw_domain_from_customer_id.keys():
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
    # get clean domain from the customer id
    search_domain = clean_domain_from_raw_domain[raw_domain]
    
    # adjustment to make - if we already searched this domain, use result we got before, and add to sheet
    if search_domain in search_result_from_clean_domain:
        print(f"Already searched {search_domain}, result is {search_result_from_clean_domain[search_domain]}")
        # append/write output to CSV file
        with open(OUTPUT_CSV_FILE, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["domain", "ein"])
            
            # Only write header if file is empty
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                "domain": search_domain,
                "ein": search_result_from_clean_domain[search_domain]
            })
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
                search_result_from_clean_domain[search_domain] = None
                return
            else:
                print(f"Results found for {search_domain}:")
                ein = data["results"][0]["ein"]
                search_result_from_clean_domain[search_domain] = ein
                print(ein)

                # append/write output to CSV file
                with open(OUTPUT_CSV_FILE, mode="a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["domain", "ein"])
                    
                    # Only write header if file is empty
                    if file.tell() == 0:
                        writer.writeheader()

                    writer.writerow({
                        "domain": search_domain,
                        "ein": ein
                    })

        else:
            print(f"Error ({response.status_code}): {response.text}")

# loop through each id in the list and search it
for id in raw_domain_from_customer_id.keys():
    print(f"Searching for customer: {id}")
    search_customer(id)