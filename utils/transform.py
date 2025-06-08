import pandas as pd
import re

def transform_to_df(raw_data):
    """Ubah list of dicts jadi DataFrame."""
    df = pd.DataFrame(raw_data)
    return df

def clean_data(df):
    """Bersihin dan standarisasi data produk."""

    print(f"[DEBUG] Jumlah awal data: {len(df)}")

    # Filter dirty patterns
    dirty_patterns = {
        "Title": ["Unknown Product"],
        "Rating": ["Invalid Rating / 5", "Not Rated"],
        "Price": ["Price Unavailable", None]
    }

    df = df[~df['Title'].isin(dirty_patterns["Title"])]
    df = df[~df['Rating'].isin(dirty_patterns["Rating"])]
    df = df[~df['Price'].isin(dirty_patterns["Price"])]

    print(f"Setelah filter dirty patterns: {len(df)}")

    # Bersihkan kolom 'Price' dan ubah ke IDR
    df['Price'] = df['Price'].str.replace(r'[^0-9.]', '', regex=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce') * 16000

    # Bersihkan kolom 'Rating'
    df['Rating'] = df['Rating'].str.extract(r'([\d.]+)').astype(float)

    # Bersihkan kolom 'Colors'
    df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)').astype(int)

    # Standarisasi 'Gender' & 'Size'
    df['Gender'] = df['Gender'].astype(str).str.strip().str.capitalize()
    df['Size'] = df['Size'].astype(str).str.strip().str.upper()

    # Ubah 'Timestamp' jadi datetime object
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    # Drop baris yang critical-nya masih kosong setelah dibersihkan
    df.dropna(subset=['Title', 'Price', 'Rating'], inplace=True)

    print(f"Setelah dropna terakhir: {len(df)} baris")
    print(f"✅ Data selesai dibersihin. Total baris akhir: {len(df)}")

    return df
