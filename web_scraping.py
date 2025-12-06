import requests
from bs4 import BeautifulSoup
import csv

# URL of the page to scrape (replace with any e-commerce URL)
URL = "https://books.toscrape.com/catalogue/category/books_1/index.html"

# Send HTTP GET request
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Open CSV file for writing
with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product Name', 'Price', 'Rating'])

    # Find all products
    products = soup.find_all('article', class_='product_pod')
    for product in products:
        # Extract product name
        name = product.h3.a['title']

        # Extract price
        price = product.find('p', class_='price_color').text.strip()

        # Extract rating (class contains "star-rating Three" etc.)
        rating_class = product.find('p', class_='star-rating')['class']
        rating = rating_class[1] if len(rating_class) > 1 else "No rating"

        # Write row to CSV
        writer.writerow([name, price, rating])

print("Scraping complete! Data saved to products.csv")