# causeIQAPIcustomerDomainListSearch
Created this program to allow attempted filling of EIN (TaxID) for a list of Organizations based on "domain".  The results are tabulated in a "results.csv" file produced, with an "id", the original domain, the "cleaned" domain, and the search result, which will be:
1. "none" if no matches were found
2. "multiple" if >1 match was found
3. the EIN of the matched Org if exactly one was found

The input/source data should be in a .CSV with an "id" column (to be able to tie results to inputs) and a "search_domain" column.

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
