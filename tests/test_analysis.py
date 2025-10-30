"""
Tests unitarios para el módulo analysis
"""
import unittest
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from analysis import RetailAnalyzer

class TestRetailAnalyzer(unittest.TestCase):
    """Tests para la clase RetailAnalyzer"""

    def setUp(self):
        """Configuración inicial para cada test"""

        # Crear DataFrame de prueba limpio
        dates = pd.date_range('2024-01-01', periods=10, freq='D')
        self.test_data = pd.DataFrame({
            'Invoice': [f'INV{i:03d}' for i in range(10)],
            'CustomerID': [100, 100, 200, 200, 300, 100, 200, 400, 300, 400],
            'InvoiceDate': dates,
            'Quantity': [5, 3, 10, 2, 7, 4, 6, 8, 3, 5],
            'Price': [10.0, 15.0, 20.0, 25.0, 12.0, 10.0, 18.0, 22.0, 15.0, 20.0],
            'TotalAmount': [50, 45, 200, 50, 84, 40, 108, 176, 45, 100]
        })

    def test_get_basic_stats(self):
        """Test: estadísticas básicas se calculan correctamente"""

        analyzer = RetailAnalyzer(self.test_data)
        stats = analyzer.get_basic_stats()

        # Verificar claves
        self.assertIn('total_sales', stats)
        self.assertIn('avg_sale', stats)
        self.assertIn('total_customers', stats)
        self.assertIn('total_transactions', stats)

        # Verificar valores
        self.assertEqual(stats['total_sales'], self.test_data['TotalAmount'].sum())
        self.assertEqual(stats['total_customers'], 4)  # 100, 200, 300, 400
        self.assertEqual(stats['total_transactions'], 10)

    def test_customer_rfm_segmentation(self):
        """Test: segmentación RFM se calcula correctamente"""

        analyzer = RetailAnalyzer(self.test_data)
        rfm = analyzer.customer_rfm_segmentation(advanced=False)

        # Verificar estructura
        self.assertEqual(len(rfm.columns), 3)
        self.assertIn('Recency', rfm.columns)
        self.assertIn('Frequency', rfm.columns)
        self.assertIn('Monetary', rfm.columns)

        # Verificar que hay 4 clientes
        self.assertEqual(len(rfm), 4)

        # Verificar que Frequency es correcto para cliente 100
        self.assertEqual(rfm.loc[100, 'Frequency'], 3)  # 3 compras

    def test_get_top_customers(self):
        """Test: top customers retorna número correcto"""

        analyzer = RetailAnalyzer(self.test_data)
        top_3 = analyzer.get_top_customers(n=3)

        # Verificar que retorna 3 clientes
        self.assertEqual(len(top_3), 3)

        # Verificar que está ordenado por Monetary descendente
        monetary_values = top_3['Monetary'].tolist()
        self.assertEqual(monetary_values, sorted(monetary_values, reverse=True))

if __name__ == '__main__':
    unittest.main()
