from bs4 import BeautifulSoup
import requests
import csv


for i in range(1, 250):

    csv_file_name = "World_of_Books_Data.csv"
    with open(csv_file_name, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Book Name', 'Book Author', 'Price', 'URL'])
        
        url = f"https://www.wob.com/en-gb/category/rare-books/{i}?so=price_desc"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

        with requests.Session() as session:
            response = session.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            book_titles = soup.find_all("span", class_ = "title")
            book_authors = soup.find_all("span", class_ = "author")
            book_prices = soup.find_all("div", class_ = "itemPrice")
            book_urls = soup.find_all("a", class_ = "itemImageContainer")
            
            for book_url in book_urls:
                book_url = book_url['href']
                url = f"wob.com{book_url}"
                print(url)
                
            for book_title, book_author, book_price, book_url in zip(book_titles, book_authors, book_prices, book_urls):
                book_title = book_title.text.strip()
                book_author = book_author.text.strip()
                book_price = book_price.text.strip()
                
                book_url = book_url['href']
                book_url = f"https://wob.com{book_url}"
                
                csv_writer.writerow([book_title, book_author, book_price, book_url])
                print(f"{book_title} has been added to {csv_file_name}")
            