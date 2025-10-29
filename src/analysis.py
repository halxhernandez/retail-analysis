"""
Módulo de análisis estadístico para datos de retail
Incluye análisis de patrones temporales de ventas
"""

import pandas as pd
import numpy as np
from datetime import datetime

class RetailAnalyzer:
    """Clase para análisis de datos retail con foco en patrones temporales"""

    def __init__(self, df: pd.DataFrame):
        """Inicializa el analizador

        Args:
            df: DataFrame con datos limpios de retail
        """
        self.df = df
        self.version = "2.0.0"
        self.analysis_date = datetime.now()

    def get_basic_stats(self):
        """Retorna estadísticas básicas del dataset"""
        stats = {
            'total_sales': self.df['TotalAmount'].sum(),
            'avg_sales': self.df['TotalAmount'].mean(),
            'total_customers': self.df['CustomerID'].unique(),
            'total_transactions': len(self.df)
        }
        return stats

    def sales_by_month(self):
        """
        Analiza ventas agrupadas por mes

        Returns:
            Series con ventas totales por mes
        """

        monthly_sales = self.df.groupby(
            self.df['InvoiceDate'].dt.to_period('M')
        )['TotalAmount'].sum()

        return monthly_sales

    def sales_by_day_of_week(self):
        """
        Analiza ventas por día de la semana

        Returns:
            DataFrame con ventas por día
        """

        self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.day_name()

        daily_sales = self.df.groupby('DayOfWeek').agg({
            'TotalAmount': ['sum', 'mean', 'count']
        }).round(2)

        # Ordenar por días de la semana
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                    'Friday', 'Saturday', 'Sunday']

        daily_sales = daily_sales.reindex(day_order)

        return daily_sales

    def sales_by_hour(self):
        """
        Analiza ventas por hora del día

        Returns:
            Series con ventas por hora
        """
        hourly_sales = self.df.groupby(
            self.df['InvoiceDate'].dt.hour
        )['TotalAmount'].sum()

        return hourly_sales

    def get_peak_sales_time(self):
        """
        Identifica el periodo de mayor actividad

        Returns:
            Dict con información de pico de ventas
        """
        hourly = self.sales_by_hour()
        peak_hour = hourly.idxmax()
        peak_amount = hourly.max()

        return {
            'peak_hour': peak_hour,
            'peak_amount': peak_amount,
            'analysis_date': self.analysis_date
        }

if __name__ == '__main__':
    print(f"Módulo de análisis - version 2.0.0 - Análisis temporal")
