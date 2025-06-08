import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BASE_URL = 'https://fashion-studio.dicoding.dev/?page={}'

def extract_product_data(card):
    """Mengambil detail produk dari elemen HTML."""
    try:
        title_tag = card.find('h3', class_='product-title')
        title = title_tag.text.strip() if title_tag else 'Unknown Product'

        price_tag = card.find('div', class_='price-container')
        price = price_tag.text.strip() if price_tag else 'Price Unavailable'

        rating_tag = card.find('p', string=lambda t: t and 'Rating' in t)
        rating = rating_tag.text.strip().replace('Rating: ', '') if rating_tag else 'Rating: ⭐ Invalid / 5'

        colors_tag = card.find('p', string=lambda t: t and 'Colors' in t)
        colors = int(''.join(filter(str.isdigit, colors_tag.text))) if colors_tag else 0

        size_tag = card.find('p', string=lambda t: t and 'Size' in t)
        size = size_tag.text.strip().replace('Size: ', '') if size_tag else 'Size: Unknown'

        gender_tag = card.find('p', string=lambda t: t and 'Gender' in t)
        gender = gender_tag.text.strip().replace('Gender: ', '') if gender_tag else 'Gender: Unknown'

        return {
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Colors': colors,
            'Size': size,
            'Gender': gender,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        print(f"❌ Gagal ekstrak data: {e}")
        return None

def fetch_product_data(url, delay=2):
    """Mengambil dan memparsing data produk dari halaman koleksi."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise Exception(f"❌ Error mengakses URL {url}: {error}")

    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        product_list = []

        # Ambil data produk dari setiap elemen dengan class 'collection-card'
        cards = soup.find_all('div', class_='collection-card')
        for card in cards:
            product_info = extract_product_data(card)
            if product_info:
                product_list.append(product_info)

        # Tunggu sebentar buat rate limiting
        time.sleep(delay)
        return product_list
    except Exception as error:
        raise Exception(f"❌ Gagal parsing halaman: {error}")
