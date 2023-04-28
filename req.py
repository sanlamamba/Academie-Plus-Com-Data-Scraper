import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

url = 'https://academie-plus.com/Liste-des-ecoles-du-senegal'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

etab_liste_section = soup.find('section', {'id': 'etab-liste-section'})

for etab in etab_liste_section.find_all('article', class_='left-infos'):
    # Extract the school name from the title of the article
    etab_name = etab.find('h3', class_='h3-etab-nomCourt').text.strip()

    # Extract the phone number from the corresponding <span> element
    phone_number = etab.find('span', class_='etab-phone').text.strip()
    etab_phone = re.search(
        r'(\+?\d[\d\s-]+)', phone_number).group(1).replace(' ', '')
    etab_email_element = etab.find('p', class_='etab-emaail')
    etab_email = ""
    if etab_email_element:
        etab_email = str(etab_email_element)

    # Extract the address from the <p> element with class 'etab-adress'
#     etab_address_elem = etab.find('p', class_='etab-adress')
    etab_address = ""

    # Print the extracted information for this school
    print(etab_name)
    print('Phone:', etab_phone)
    print('Email:', etab_email)
    print('Address:', etab_address)
    print('-' * 50)
