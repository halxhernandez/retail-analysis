"""
Módulo de análisis estadístico para datos de retail
versión inicial - estructura base
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
        self.version = "0.1.0"

    def get_basic_stats(self):
        """Retorna estadísticas básicas del dataset"""
        stats = {
            'total_sales': self.df['TotalAmount'].sum(),
            'avg_sales': self.df['TotalAmount'].mean(),
            'total_customers': self.df['CustomerID'].unique(),
            'total_transactions': len(self.df)
        }
        return stats

if __name__ == '__main__':
    print(f"Módulo de análisis - version 0.1.0")
