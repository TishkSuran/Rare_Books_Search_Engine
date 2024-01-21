import requests
from bs4 import BeautifulSoup
import csv
import re

csv_file_name = 'book_data.csv'
with open(csv_file_name, 'a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Book Name', 'Book Author', 'Price', 'URL'])

    for i in range(1, 5201):
        url = f'http://www.peterharrington.co.uk/books?p={i}&product_list_order=high_to_low'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        with requests.Session() as session:
            response = session.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            product_links = soup.find_all('a', class_="product-item-link")
            price_spans = soup.find_all('span', class_="price")
            product_divs = soup.find_all('div', class_="product description product-item-description")
            p_elements = soup.find_all('li', class_='item product product-item')
            strong_class = soup.find_all('b')
            
            book_names = soup.find_all('strong', class_="product name product-item-name")

            for book_name, price, description, p_element, author in zip(book_names, price_spans, product_divs, p_elements, strong_class):
                book_author = author.text.strip()
                book_link = book_name.find('a')
                book_link = book_link.text.strip()
                book_price = price.text.strip()
                
                book_description = description.text.strip()
                if "Learn More" in book_description:
                    book_description = book_description.split("Learn More")[0].strip()
                
                book_p_content = re.sub(r'\s+', ' ', p_element.find('p').text.strip())

                city_year_match = re.match(r'(.*?) : (\d{4})$', book_p_content)
                if city_year_match:
                    city_of_origin, year_written = city_year_match.groups()
                else:
                    continue

                learn_more_link = description.find('a', class_='action more')
                if learn_more_link:
                    learn_more_link = learn_more_link['href']
                    full_description_response = requests.get(learn_more_link)
                    full_description_soup = BeautifulSoup(full_description_response.text, 'html.parser')

                    paragraphs = full_description_soup.find_all('p', class_="contentFull")
                    
                    for paragraph in paragraphs:
                        book_full_description = paragraph.text.strip()

                print(f"{book_link} has been added to {csv_file_name}")
                print()

                csv_writer.writerow([book_link, book_author, book_price, learn_more_link])
