# 🚀 Proyek ETL: Pemrosesan Data Produk Fashion

Proyek ini merupakan implementasi pipeline ETL (Extract, Transform, Load) untuk data produk fashion dari website [Dicoding Fashion Studio](https://fashion-studio.dicoding.dev). Tujuannya adalah mengotomatiskan pengambilan data, pembersihan, dan penyimpanan ke dalam Google Sheets atau database PostgreSQL.

## 🧩 Struktur Folder
```
├── utils/
│ ├── extract.py        # Fungsi scraping data produk
│ ├── transform.py      # Fungsi pembersihan & transformasi data
│ └── load.py           # Fungsi penyimpanan ke Google Sheets / PostgreSQL
├── tests/              # Unit tests
│ ├── test_extract.py
│ ├── test_transform.py
│ └── test_load.py
├── main.py             # Skrip utama untuk menjalankan ETL
├── products.csv        # Output CSV hasil ETL
├── requirements.txt    # Daftar dependencies
├── submission.txt      # Langkah-langkah menjalankan proyek
└── README.md  
```

## ⚙️ Fitur Utama

- **Extract**: Mengambil data produk dari halaman web fashion secara dinamis.
- **Transform**: Membersihkan teks, menghapus duplikat dan nilai kosong, mengubah harga menjadi Rupiah.
- **Load**: Menyimpan data ke Google Sheets dan PostgreSQL.

## 🧪 Pengujian

Jalankan test dengan:

```bash
python -m pytest tests
```
test (coverage) dapat dilihat dengan:
```
coverage run -m pytest tests
coverage report -m
```

