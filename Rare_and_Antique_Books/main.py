from bs4 import BeautifulSoup
import requests
import csv

csv_file_name = 'Rare_and_Antique_Books_Data.csv'
with open(csv_file_name, 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Book Name', 'Book Author', 'Book Price', 'URL'])
    
    for i in range(1,32):

        url = f"https://rareandantiquebooks.com/first-edition-books/page/{i}/"

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

        with requests.Session() as session:
            response = session.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            titles_and_authors = soup.find_all("h2", class_="woocommerce-loop-product__title")
            urls = soup.find_all("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
            price = soup.find_all("span", class_ = "woocommerce-Price-amount amount") 

            for title_and_author, book_url, book_price in zip(titles_and_authors, urls, price):
                
                try:
                    title, author = map(str.strip, title_and_author.text.rsplit("by", 1))
                except:
                    continue
                
                url = book_url['href']
                book_price = book_price.text.strip()

                print(f"{title} has been added to {csv_file_name}")
            
                csv_writer.writerow([title, author, book_price, url])


