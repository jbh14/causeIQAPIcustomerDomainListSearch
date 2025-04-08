import os
import requests
import base64
import csv
from dotenv import load_dotenv
from readCustomerIDs import read_customer_ids

CUSTOMERS_CSV_FILE = "customers.csv"
CUSTOMER_ID_COL_HEADER = "customer_id"

# Load environment variables from .env file
load_dotenv()

# get auth token from env variables
if not os.getenv("AUTH_TOKEN"):
    raise ValueError("AUTH_TOKEN is not set in the environment variables")
BASE_URL = "https://www.causeiq.com/api/organizations"
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

# TODO - load domains to search from a CSV file
# Load customer IDs from CSV
customer_ids = read_customer_ids(CUSTOMERS_CSV_FILE, CUSTOMER_ID_COL_HEADER) # 1st parameter is the CSV filename, 2nd parameter is the column header for customer IDs

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
        print(f"Success: {response.json()}")
        data = response.json()
        ein = data["results"][0]["ein"]
        print(ein)

        # write output to CSV file
        with open("output.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["domain", "ein"])
            writer.writeheader()
            writer.writerow({
                "domain": search_domain,
                "ein": ein
            })

    else:
        print(f"Error ({response.status_code}): {response.text}")

# STOPPING POINT - need to load domains from a CSV file, append EIN to the CSV file for each we found a resolt for
domains = ["lovchicago.org", "lovchicago.com", "lovchicago.net", "lovchicago.info", "lovchicago.us"]

search_customer("lovchicago.org")