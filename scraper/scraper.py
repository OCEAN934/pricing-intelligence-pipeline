import requests
from bs4 import BeautifulSoup
import json
import time
from utils.logger import log

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"


def scrape():
    log("Scraping started")

    results = []

    for page in range(1, 6):  # limiting pages for assignment scope
        try:
            url = BASE_URL.format(page)
            log(f"Scraping page {page}: {url}")

            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            books = soup.find_all("article", class_="product_pod")

            for book in books:
                try:
                    title = book.h3.a["title"]
                    price = book.find("p", class_="price_color").text
                    availability = book.find("p", class_="instock availability").text.strip()

                    results.append({
                        "title": title,
                        "price": price,
                        "availability": availability
                    })

                except Exception as e:
                    log(f"Error parsing book on page {page}: {e}")

            time.sleep(1)

        except Exception as e:
            log(f"Error on page {page}: {e}")

    # Save raw data
    try:
        with open("data/raw.json", "w") as f:
            json.dump(results, f, indent=4)

        log(f"Scraping completed successfully. Total records: {len(results)}")

    except Exception as e:
        log(f"Error saving raw data: {e}")


if __name__ == "__main__":
    scrape()