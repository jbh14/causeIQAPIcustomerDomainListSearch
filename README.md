# causeIQAPIcustomerDomainListSearch
Created this program to allow attempted filling of EIN (TaxID) for a list of Orgs that we think we might know a "domain" from.

## Available Scripts
1. Running this locally, make the CB site name and API key available to the script by listing inside an `.env` file in your project directory as such:
```
AUTH_TOKEN = "<causeiq_api_token>"
```
2. Create a CSV file for domains with EINs will be added to if found for each domain.
3. Create and activate a virtual environment:
```
python3 -m venv .venv       # Mac/Linux
python -m venv .venv        # Windows

source .venv/bin/activate   # Mac/Linux
.\venv\Scripts\activate     # Windows
```
4. Install required dependencies:
```
pip install -r requirements.txt
```
5. Run the script:
```
python3 searchCustomersByDomain.py
```
