import re

def extract_domain(entry):
    entry = entry.strip()
    
    # If it's an email address
    if "@" in entry:
        return entry.split("@")[1].lower()
    
    # Remove protocol and www
    entry = re.sub(r'^https?://', '', entry)
    entry = re.sub(r'^www\.', '', entry)
    
    # Only keep up to the first slash
    return entry.split("/")[0].lower()