import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the website
url = "https://books.toscrape.com/catalogue/page-1.html"

# Output CSV file
filename = "books_dataset.csv"

# Open CSV file for writing
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # Write header row
    writer.writerow(["Title", "Price", "Rating", "Link"])

    # Loop through all 50 pages
    for page in range(1, 51):
        page_url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(page_url)
        
        if response.status_code != 200:
            print(f"Failed to access page {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        # Extract details of each book
        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            rating = book.p["class"][1]  # Example: "One", "Two", "Three"...
            link = "https://books.toscrape.com/catalogue/" + book.h3.a["href"]

            # Write row into CSV
            writer.writerow([title, price, rating, link])

print(f"Scraping completed! Data saved in {filename}")
