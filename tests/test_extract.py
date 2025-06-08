import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils.extract import fetch_product_data, extract_product_data
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class ExtractTestCase(unittest.TestCase):

    # Test extract_product_data
    def test_extract_product_data_valid(self):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Jaket</h3>
            <div class="price-container">Rp150.000</div>
            <p>Rating: 4.0 / 5</p>
            <p>Colors: 3</p>
            <p>Size: XL</p>
            <p>Gender: Female</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        card = soup.find('div', class_='collection-card')
        data = extract_product_data(card)
        self.assertEqual(data['Title'], "Jaket")
        self.assertEqual(data['Price'], "Rp150.000")
        self.assertEqual(data['Colors'], 3)
        self.assertEqual(data['Gender'], "Female")
        self.assertIn("Timestamp", data)

    # Test extract_product_data exception handling
    def test_extract_product_data_exception(self):
        bad_card = None
        result = extract_product_data(bad_card)
        self.assertIsNone(result)

    # Case sukses normal fetch_product_data 
    @patch("utils.extract.requests.get")
    @patch("utils.extract.time.sleep", return_value=None)
    def test_fetch_product_data_valid(self, mock_sleep, mock_get):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Jacket</h3>
            <div class="price-container">$45.50</div>
            <p>Rating: 2.5 / 5</p>
            <p>Colors: 2</p>
            <p>Size: L</p>
            <p>Gender: Male</p>
        </div>
        """
        
        mock_resp = MagicMock(status_code=200, text=html)
        mock_get.return_value = mock_resp

        data = fetch_product_data("dummy-url")
        self.assertEqual(len(data), 1)
        row = data[0]
        self.assertEqual(row["Title"], "Jacket")
        self.assertEqual(row["Colors"], 2)
        self.assertEqual(row["Gender"], "Male")
        mock_sleep.assert_called_once() 

    # Multiple products
    @patch("utils.extract.requests.get")
    @patch("utils.extract.time.sleep", return_value=None)
    def test_fetch_product_data_multiple(self, mock_sleep, mock_get):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Item 1</h3>
            <div class="price-container">$10</div>
            <p>Rating: 3.0 / 5</p>
            <p>Colors: 1</p>
            <p>Size: S</p>
            <p>Gender: Male</p>
        </div>
        <div class="collection-card">
            <h3 class="product-title">Item 2</h3>
            <div class="price-container">$20</div>
            <p>Rating: 4.5 / 5</p>
            <p>Colors: 2</p>
            <p>Size: M</p>
            <p>Gender: Female</p>
        </div>
        """

        mock_resp = MagicMock(status_code=200, text=html)
        mock_get.return_value = mock_resp

        data = fetch_product_data("dummy-url")
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["Title"], "Item 1")
        self.assertEqual(data[1]["Title"], "Item 2")

    # Error HTTP 
    @patch("utils.extract.requests.get")
    def test_fetch_product_data_http_error(self, mock_get):
        mock_resp = MagicMock(status_code=500)
        mock_resp.raise_for_status.side_effect = Exception("500 error")
        mock_get.return_value = mock_resp
        with self.assertRaises(Exception):
            fetch_product_data("dummy-url")

    # Halaman tanpa card
    @patch("utils.extract.requests.get")
    def test_fetch_product_data_empty_page(self, mock_get):
        mock_resp = MagicMock(status_code=200, text="<html><body>No product</body></html>")
        mock_get.return_value = mock_resp
        data = fetch_product_data("dummy-url")
        self.assertEqual(data, [])

    # Card dengan tag hilang 
    @patch("utils.extract.requests.get")
    def test_fetch_product_data_partial_tags(self, mock_get):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Item Tanpa Harga</h3>
            <!-- price-container hilang -->
            <p>Rating: ⭐ Invalid Rating / 5</p>  <!-- rating invalid -->
            <!-- Colors hilang -->
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """

        mock_resp = MagicMock(status_code=200, text=html)
        mock_get.return_value = mock_resp
        data = fetch_product_data("dummy-url")
        self.assertEqual(len(data), 1)
        row = data[0]

        self.assertEqual(row["Price"], "Price Unavailable")
        self.assertIn("Invalid", row["Rating"])

if __name__ == "__main__":
    unittest.main()