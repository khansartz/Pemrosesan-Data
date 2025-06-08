from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

def save_to_csv(df, filename="products.csv"):
    """Simpan DataFrame ke file CSV lokal."""
    try:
        df.to_csv(filename, index=False)
        print(f"✅ Data berhasil disimpan ke '{filename}'")
    except Exception as e:
        print(f"❌ Gagal simpan ke CSV: {e}")

def save_to_google_sheets(df, spreadsheet_id, range_name): 
    try:
        SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Convert semua kolom Timestamp ke string
        df_copy = df.copy()
        for col in df_copy.columns:
            if df_copy[col].dtype == 'datetime64[ns]':
                df_copy[col] = df_copy[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        values = df_copy.values.tolist()
        body = {'values': values}

        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("✅ Data berhasil ditambahkan ke Google Sheets!")

    except Exception as e:
        print(f"❌ Gagal simpan ke Google Sheets: {e}")


def store_to_postgre(df, table_name='bookstoscrape'):
    """Simpan DataFrame ke PostgreSQL."""
    try:
        username = 'postgres'
        password = 'password'
        host = 'localhost'
        port = '5432'
        database = 'fashion'

        db_url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
        engine = create_engine(db_url)

        with engine.connect() as conn:
            df.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"{len(df)} baris berhasil ditambahkan ke tabel '{table_name}'")

    except Exception as e:
        print(f"❌ Gagal simpan data ke PostgreSQL: {e}")