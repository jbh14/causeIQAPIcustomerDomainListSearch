import os
import requests
import base64
import csv
from dotenv import load_dotenv
from readCustomerDomainsFromSheet import read_customer_domains
from extractDomains import extract_domain

SEARCH_ORGS_CSV_FILE = "someOrgsToSearch.csv"
SEARCH_DOMAIN_COL_HEADER = "search_domain"
CAUSE_IQ_ORGSEARCH_ENDPOINT = "https://www.causeiq.com/api/organizations"
OUTPUT_CSV_FILE = "results.csv"

# Load environment variables from .env file to get auth token
load_dotenv()
if not os.getenv("AUTH_TOKEN"):
    raise ValueError("AUTH_TOKEN is not set in the environment variables")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# Load domains to clean and search from CSV
customer_domains = read_customer_domains(SEARCH_ORGS_CSV_FILE, SEARCH_DOMAIN_COL_HEADER) 

def search_customer(search_domain):
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
            return
        else:
            print(f"Results found for {search_domain}:")
            ein = data["results"][0]["ein"]
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

# remove repeated domains
def get_unique_items(input_list):
    return list(set(input_list))

customer_domains_unique = get_unique_items(customer_domains)

# loop through each domain in the list, clean it, and search it
for domain in customer_domains_unique:
    # Extract domain from the customer ID
    print(f"Extracting domain from: {domain}")
    domain = extract_domain(domain)
    print(f"Extracted domain: {domain}")
    print("")

    search_customer(domain)