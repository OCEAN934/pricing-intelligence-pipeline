import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"

def scrape():
    results = []

    for page in range(1, 6):  # limit pages (time constraint)
        try:
            url = BASE_URL.format(page)
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            books = soup.find_all("article", class_="product_pod")

            for book in books:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text
                availability = book.find("p", class_="instock availability").text.strip()

                results.append({
                    "title": title,
                    "price": price,
                    "availability": availability
                })

            time.sleep(1)

        except Exception as e:
            print(f"Error on page {page}: {e}")

    with open("data/raw.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Scraping complete")

if __name__ == "__main__":
    scrape()