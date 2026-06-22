from bs4 import BeautifulSoup
from selenium import webdriver
import re

driver = webdriver.Chrome()
driver.get('https://coinranking.com/')
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

data_retrieved = []  # stores data which will be saved to the text file

# retrieves data in each row
for row in soup.findAll(attrs={'class': 'table__row table__row--click table__row--full-width'}):
    name = row.find('a').text.strip()  # get name in the <a> element
    price = row.find('div', {'class': 'valuta valuta--light'}).text.strip()  # gets price in class: valuta valuta--light
    price = re.sub(r"[\n\t\s,]*", "", price)  # removes trailing spaces, line breaks, and commas
    data_retrieved.append(name + "," + price)  # add data to list

# if results is not empty save data to text file
# save text file as crypto.txt
if data_retrieved:
    with open('crypto.txt', 'w') as file:
        for data in data_retrieved:
            file.write(data + '\n')