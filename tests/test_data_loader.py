"""
Test unitarios para el módulo data_loader
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_loader import RetailDataLoader

class TestRetailDataLoader(unittest.TestCase):
    """Test para la clase RetailDataLoader"""

    def setUp(self):
        """Configuración inicial para cada test"""

        # Crear DataFrame de prueba
        self.test_data = pd.DataFrame({
            'Invoice': ['INV001', 'INV002', 'C001','INV003'],
            'StockCode': ['A001', 'A002', 'A001', 'A003'],
            'Description': ['Product 1', 'Product 2', 'Product 1', None],
            'Quantity': [10, 5, -10, 3],
            'InvoiceDate': pd.to_datetime([
                '2024-01-01', '2024-01-02',
                '2024-01-03', '2024-01-04'
            ]),
            'Price': [10.5, 20.0, 10.5, -5.0],
            'CustomerID': [100, 200, 100, None],
            'Country': ['UK', 'UK', 'UK', 'France']
        })

    def test_clean_data_removes_nulls(self):
        """Test: limpieza elimina nulos en CustomerID y Description"""

        loader = RetailDataLoader('dummy_path.xlsx')
        loader.df = self.test_data.copy()

        cleaned = loader.clean_data()

        # Verificar que se eliminaron nulos
        self.assertFalse(cleaned['CustomerID'].isnull().any())
        self.assertFalse(cleaned['Description'].isnull().any())

    def test_clean_data_removes_cancellations(self):
        """Test: limpieza elimina transacciones canceladas"""

        loader = RetailDataLoader('dummy_path.xlsx')
        loader.df = self.test_data.copy()

        cleaned = loader.clean_data()

        # Verificar que no hay invoices que empiecen con 'C'
        cancelled = cleaned['Invoice'].str.startswith('C').any()
        self.assertFalse(cancelled)

    def test_clean_data_removes_negative_values(self):
        """Test: limpieza elimina cantidades y precios negativos"""

        loader = RetailDataLoader('dummy_path.xlsx')
        loader.df = self.test_data.copy()

        cleaned = loader.clean_data()

        # Verificar que no hay valores negativos
        self.assertTrue((cleaned['Quantity'] > 0).all())
        self.assertTrue((cleaned['Price'] > 0).all())

    def test_clean_data_creates_total_amount(self):
        """Test: limpieza crea columna TotalAmount"""

        loader = RetailDataLoader('dummy_path.xlsx')
        loader.df = self.test_data.copy()

        cleaned = loader.clean_data()

        # Verificar que existe la columna
        self.assertIn('TotalAmount', cleaned.columns)

        # Verificar cálculo correcto
        expected = cleaned['Quantity'] * cleaned['Price']
        pd.testing.assert_series_equal(
            cleaned['TotalAmount'], expected,
            check_names=False
        )

    def test_get_summary_returns_correct_structure(self):
        """Test: summary retorna estructura correcta"""

        loader = RetailDataLoader('dummy_path.xlsx')
        loader.df = self.test_data.copy()
        loader.clean_data()

        summary = loader.get_summary()

        # Verificar claves del diccionario
        expected_keys = ['total_transactions', 'total_customers',
                        'total_products', 'date_range', 'total_revenue',
                        'countries']
        for key in expected_keys:
            self.assertIn(key, summary)

if __name__ == '__main__':
    unittest.main()
