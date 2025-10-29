"""
Módulo de análisis estadístico para datos de retail
Incluye segmentación RFM de clientes
"""

import pandas as pd
import numpy as np

class RetailAnalyzer:
    """Clase para análisis de datos retail"""

    def __init__(self, df: pd.DataFrame):
        """Inicializa el analizador

        Args:
            df: DataFrame con datos limpios de retail
        """
        self.df = df
        self.version = "1.0.0"

    def get_basic_stats(self):
        """Retorna estadísticas básicas del dataset"""
        stats = {
            'total_sales': self.df['TotalAmount'].sum(),
            'avg_sales': self.df['TotalAmount'].mean(),
            'total_customers': self.df['CustomerID'].unique(),
            'total_transactions': len(self.df)
        }
        return stats

    def customer_rfm_segmentation(self):
        """
        Segmentación RFM (Recency, Frequency, Monetary) de clientes

        Returns:
            DataFrame con métricas RFM por clientes
        """

        # Fecha de referencia para calcular recency
        snapshot_date = self.df['InvoiceDate'].max() + pd.Timedelta(days=1)

        # Calcular métricas RFM
        rfm = self.df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (snapshot_date - x.max()).days,    # Recency
            'Invoice': 'count',    # Frequency
            'TotalAmount': 'sum'    # Monetary
        })

        rfm.columns = ['Recency', 'Frequency', 'Monetary']
        rfm = rfm.sort_values('Monetary', ascending=False)

        return rfm

    def get_top_customers(self, n: int = 10):
        """
        Obtiene los top N clientes por valor monetario

        Args:
            n: Número de clientes a retornar

        Returns:
            DataFrame con top clientes
        """

        rfm = self.customer_rfm_segmentation()
        return rfm.head(n)

if __name__ == '__main__':
    print(f"Módulo de análisis - version 0.1.0")
