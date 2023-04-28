from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
import csv
import time

driver = webdriver.Chrome()

url = 'https://academie-plus.com/Liste-des-ecoles-du-senegal'
driver.get(url)

html_source = driver.page_source
html = driver.page_source

etabs = re.findall(
    r'<div class="container-fluid etab-box.*?<!-- Fin details Etab -->', html, re.DOTALL)

etab_list = []

for etab in etabs:
    name = re.search(
        r'<strong class="etab-nom">(.*?)</strong>', etab, re.DOTALL)
    name = name.group(1).strip() if name else 'NA'

    phone = re.search(
        r'<span class="etab-phone.*?>(.*?)</span>', etab, re.DOTALL)
    phone = phone.group(1).strip() if phone else 'NA'
    phone = phone.split('>')[1].strip() if '>' in phone else phone

    email = re.search(r'<a href="mailto:(.*?)"', etab, re.DOTALL)
    email = email.group(1).strip() if email else 'NA'

    address = re.search(
        r'<p class="etab-adress">.*?<span>(.*?)</span>', etab, re.DOTALL)
    address = address.group(1).strip() if address else 'NA'
    address = re.sub(r'<span.*?>|</span>', '', address)

    type_ens = ''
    type_ens_span = re.findall(
        r'>Type.*?</strong>', etab, re.DOTALL)
    if type_ens_span:
        type_ens = ','.join(re.findall(
            r'<span.*?>(.*?)</span>', type_ens_span[0], re.DOTALL))

    etab_list.append({
        'Nom': name,
        'Téléphone': phone,
        'Email': email,
        'Adresse': address,
        'Type': type_ens
    })


# Save the extracted information as a CSV file
with open('etabs.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(
        file, fieldnames=['Nom', 'Téléphone', 'Email', 'Adresse', 'Type'])
    writer.writeheader()
    for school in etab_list:
        writer.writerow(school)

for etab in etab_list:
    time.sleep(0.5)
    for key, value in etab.items():
        print(f"{key} : {value}")
    print("-"*50)


# Quit the webdriver
driver.quit()
