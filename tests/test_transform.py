import unittest
import pandas as pd
from utils.transform import transform_to_df, clean_data
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TransformTestCase(unittest.TestCase):
    def setUp(self):
        # data dummy
        self.raw_products = [
            {
                "Title": "Kaos Polos",
                "Price": "$10.50",
                "Rating": "4.5 / 5",
                "Colors": "3 Colors",
                "Size": "Size: L",
                "Gender": "Gender: Men",
                "Timestamp": "2025-05-17 10:00:00",
            },
            {
                "Title": "Unknown Product", 
                "Price": "Price Unavailable",
                "Rating": "Invalid Rating / 5",
                "Colors": "0 Colors",
                "Size": "Size: S",
                "Gender": "Gender: Women",
                "Timestamp": "2025-05-17 10:05:00",
            },
        ]

    def test_transform_pipeline(self):
        """Data valid harus tetap ada & bersih; data kotor harus hilang."""
        df_raw = transform_to_df(self.raw_products)
        self.assertEqual(len(df_raw), 2) 

        df_clean = clean_data(df_raw)
        # Hanya 1 baris yang valid seharusnya tersisa
        self.assertEqual(len(df_clean), 1)

        # Kolom & tipe
        expected_cols = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "Timestamp"]
        self.assertListEqual(list(df_clean.columns), expected_cols)
        self.assertTrue(pd.api.types.is_float_dtype(df_clean["Price"]))
        self.assertTrue(pd.api.types.is_float_dtype(df_clean["Rating"]))
        self.assertTrue(pd.api.types.is_integer_dtype(df_clean["Colors"]))

        # Nilai telah dibersihkan
        row = df_clean.iloc[0]
        self.assertEqual(row["Title"], "Kaos Polos")
        self.assertGreater(row["Price"], 0)
        self.assertLessEqual(row["Rating"], 5)

if __name__ == "__main__":
    unittest.main()
