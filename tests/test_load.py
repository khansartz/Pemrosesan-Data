import unittest
import pandas as pd
import tempfile
from unittest.mock import patch, MagicMock
from utils.load import save_to_csv, save_to_google_sheets
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class LoadTestCase(unittest.TestCase):
    def setUp(self):
        self.df_sample = pd.DataFrame(
            {
                "title": ["Jaket Hoodie", "Celana Jogger"],
                "price": [150000, 175000],
                "rating": [4.2, 4.7],
            }
        )

    # CSV real‑file test 
    def test_save_to_csv_real_file(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            file_path = tmp.name

        try:
            save_to_csv(self.df_sample, file_path)
            self.assertTrue(os.path.exists(file_path))

            loaded = pd.read_csv(file_path)
            self.assertEqual(len(loaded), len(self.df_sample))
            self.assertListEqual(list(loaded.columns), list(self.df_sample.columns))
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    # CSV mocked test 
    @patch("pandas.DataFrame.to_csv")
    def test_save_to_csv_mocked(self, mock_to_csv):
        save_to_csv(self.df_sample, "dummy.csv")
        mock_to_csv.assert_called_once_with("dummy.csv", index=False)

    # Google Sheets mocked test 
    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_save_to_google_sheets(self, mock_creds, mock_build):
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        save_to_google_sheets(self.df_sample, "fake_sheet_id", "Sheet1!A2")

        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

    # PostgreSQL mocked success 
    @patch("pandas.DataFrame.to_sql")
    @patch("utils.load.create_engine")
    def test_store_to_postgre_success(self, mock_engine, mock_to_sql):
        from utils.load import store_to_postgre

        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

        store_to_postgre(self.df_sample, table_name="dummy_tbl")

        mock_to_sql.assert_called_once_with("dummy_tbl", mock_conn, if_exists="append", index=False)

    # PostgreSQL mocked failure 
    @patch("utils.load.create_engine", side_effect=Exception("DB down"))
    @patch("builtins.print")
    def test_store_to_postgre_failure(self, mock_print, mock_engine):
        from utils.load import store_to_postgre

        store_to_postgre(self.df_sample, table_name="dummy_tbl")

        mock_print.assert_any_call("❌ Gagal simpan data ke PostgreSQL: DB down")

if __name__ == "__main__":
    unittest.main()