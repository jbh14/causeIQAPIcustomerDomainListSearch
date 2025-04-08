import os
import requests
import base64
import csv
from dotenv import load_dotenv
from readCustomerDomainsFromSheet import read_customer_domains
from extractDomains import extract_domain

CUSTOMERS_CSV_FILE = "someOrgsToSearch.csv"
CUSTOMER_ID_COL_HEADER = "search_domain"

# Load environment variables from .env file
load_dotenv()

# get auth token from env variables
if not os.getenv("AUTH_TOKEN"):
    raise ValueError("AUTH_TOKEN is not set in the environment variables")
BASE_URL = "https://www.causeiq.com/api/organizations"
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# TODO - load domains to search from a CSV file
# Load customer IDs from CSV
customer_domains = read_customer_domains(CUSTOMERS_CSV_FILE, CUSTOMER_ID_COL_HEADER) # 1st parameter is the CSV filename, 2nd parameter is the column header for customer IDs

def search_customer(search_domain):
    url = f"{BASE_URL}"
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

            # write output to CSV file
            with open("results.csv", mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["domain", "ein"])
                writer.writeheader()
                writer.writerow({
                    "domain": search_domain,
                    "ein": ein
                })

    else:
        print(f"Error ({response.status_code}): {response.text}")

for domain in customer_domains:

    # Extract domain from the customer ID
    print(f"Extracting domain from: {domain}")
    domain = extract_domain(domain)
    print(f"Extracted domain: {domain}")
    print("")

    # search_customer(domain)