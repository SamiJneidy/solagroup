import requests
from bs4 import BeautifulSoup

def get_postal_code(lot_number):
    url = f"https://www.copart.com/lot/{lot_number}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return {"page": soup.prettify()}
        # Locate the postal code in the page source
        postal_code = None
        for div in soup.find_all("div"):
            if "Zip" in div.text:  # Copart sometimes labels the postal code as "Zip"
                postal_code = div.text.split(":")[-1].strip()
                break
        
        return postal_code if postal_code else "Postal code not found"
    
    else:
        return f"Error: {response.status_code}"

# # Example usage:
# lot_number = "41593405"
# print(get_postal_code(lot_number))
