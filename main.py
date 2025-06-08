from utils.extract import fetch_product_data
from utils.transform import transform_to_df, clean_data
from utils.load import save_to_csv, store_to_postgre, save_to_google_sheets

def main():
    all_data = []
    
    print("Mulai proses ETL...")

    # Ambil page pertama
    print("📦 Scraping page 1...")
    try:
        page_data = fetch_product_data("https://fashion-studio.dicoding.dev/")
        all_data.extend(page_data)
    except Exception as e:
        print(f"❌ Error ambil data dari page 1: {e}")

    # Ambil page 2 sampai 50
    for page in range(2, 51):
        print(f"📦 Scraping page {page}...")
        url = f"https://fashion-studio.dicoding.dev/page{page}"
        try:
            page_data = fetch_product_data(url)
            all_data.extend(page_data)
        except Exception as e:
            print(f"❌ Error ambil data dari page {page}: {e}")

    print(f"Total data mentah diambil: {len(all_data)}")

    # Transform data
    print("🔧 Transformasi data...")
    df_raw = transform_to_df(all_data)
    df_transformed = clean_data(df_raw)

    # Optional preview
    print("📊 Preview data:")
    print(df_transformed.head())

    # Load data
    print("💾 Simpan data ke CSV...")
    save_to_csv(df_transformed, filename="products.csv")

    print("📥 Simpan data ke PostgreSQL...")
    store_to_postgre(df_transformed, table_name="fashion_products")

    print("☁️ Upload data ke Google Sheets...")
    save_to_google_sheets(
        df_transformed,
        spreadsheet_id='1e5MY-2kt6Vg15V85W2f4ASkw9cQKjkmGTxjgxHqYOyM',
        range_name='Sheet1!A2'
    )

    print("✅ Proses ETL selesai!")

if __name__ == '__main__':
    main()
