from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import csv
import time

url = "https://www.templerarebooks.com/stock"
base_url = "https://www.templerarebooks.com"

driver = webdriver.Chrome()

driver.get(url)

for _ in range(150):  
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    driver.implicitly_wait(5)  

page_source = driver.page_source

driver.quit()

csv_file_name = "temple_rare_books_data"
with open(csv_file_name, 'a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Book Name', 'Book Author', 'Price', 'URL'])

    soup1 = BeautifulSoup(page_source, 'html.parser')

    product_divs = soup1.find_all('div', class_="artist text-decoration-none position-relative")

    for product_div in product_divs:
        time.sleep(2)
        product_link = product_div.find('a')['href']
        book_url = base_url + product_link
        
        response= requests.get(book_url)
        response.raise_for_status()
        
        soup2 = BeautifulSoup(response.text, 'html.parser')
        
        book_name = soup2.find('h1', class_='artist-header__title text-uppercase text-center text-md-left d-none d-md-block notranslate')
        book_price = soup2.find('div', class_ = "col-5 align-self-center")
        book_author = soup2.find('p', class_ = "mb-0")
        
        book_name = book_name.text.strip()
        book_price = book_price.text.strip()
        book_author = book_author.text.strip()
        
        csv_writer.writerow([book_name, book_author, book_price, book_url])
        print(f"{book_name} has been added to {csv_file_name}")
    
