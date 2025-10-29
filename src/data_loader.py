"""
Módulo para carga y limpieza de datos del dataset Online Retail II
que puede contener una o varias hojas con igual estructura.
"""

import pandas as pd
import numpy as np
from pathlib import Path

class RetailDataLoader:
    """Clase para cargar, limpiar y resumir datos del dataset Online Retail II."""

    def __init__(self, data_path: str):
        """Inicializa el loader con la ruta del dataset

        Args:
            data_path: Ruta del archivo de datos
        """
        self.data_path = Path(data_path)
        self.df = None

    def load_data(self):
        """Carga el dataset desde archivo Excel, manejando múltiples hojas."""
        print(f"Cargando datos desde {self.data_path}...")

        xls = pd.ExcelFile(self.data_path)
        sheet_names = xls.sheet_names
        print(f"Hojas detectadas: {sheet_names}")

        dfs = []
        reference_columns = None

        for sheet in sheet_names:
            df_sheet = pd.read_excel(xls, sheet_name=sheet)
            print(f"Hoja '{sheet}' cargada con {df_sheet.shape[0]} filas")

            # Registrar columnas de referencia
            if reference_columns is None:
                reference_columns = list(df_sheet.columns)
                dfs.append(df_sheet)
            else:
                # Verificar que la estructura coincida
                if list(df_sheet.columns) == reference_columns:
                    dfs.append(df_sheet)
                else:
                    print(f"⚠️ La hoja '{sheet}' tiene una estructura diferente. Se omitirá.")

        # Unir todas las hoja
        self.df = pd.concat(dfs, ignore_index=True)
        print(f"Datos combinados: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")

        return self.df

    def clean_data(self):
        """Limpia el dataset eliminando valores inválidos"""
        if self.df is None:
            raise ValueError("Primero debe cargar los datos con load_data()")

        print("Iniciando limpieza de datos...")
        initial_rows = len(self.df)

        # Validar columnas requeridas
        required_cols = {'CustomerID', 'Description', 'Invoice', 'Quantity', 'Price', 'InvoiceDate'}
        missing = required_cols - set(self.df.columns)
        if missing:
            raise KeyError(f"Faltan columnas en el dataset: {missing}")

        # Eliminar filas con valores nulos en columnas críticas
        self.df = self.df.dropna(subset=['CustomerID', 'Description'])

        # Eliminar transacciones canceladas (Invoice empieza con 'C')
        self.df = self.df[~self.df['Invoice'].astype(str).str.startswith('C')]

        # Eliminar cantidades y precios negativos
        self.df = self.df[self.df['Quantity'] > 0]
        self.df = self.df[self.df['Price'] > 0]

        # Crear columnas de monto total
        self.df['TotalAmount'] = self.df['Quantity'] * self.df['Price']

        # Convertir fecha a datetime
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])

        final_rows = len(self.df)
        print(f"Limpieza completada: {initial_rows - final_rows} filas eliminadas")
        print(f"Dataset final: {final_rows} filas")

        return self.df

    def get_summary(self):
        """Retorna resumen estadístico del dataset"""
        if self.df is None:
            raise ValueError("Primero debe cargar los datos")

        summary = {
            'total_transactions': len(self.df),
            'total_customers': self.df['CustomerID'].nunique(),
            'total_products': self.df['StockCode'].nunique(),
            'date_range': (
                self.df['InvoiceDate'].min(),
                self.df['InvoiceDate'].max()
            ),
            'total_revenue': self.df['TotalAmount'].sum(),
            'countries': self.df['Country'].nunique()
        }

        return summary

def main():
    """Función de prueba"""
    # Ejemplo de uso
    # loader = RetailDataLoader('data/online_retail_II.xlsx')
    # df = loader.load_data()
    # df_clean = loader.clean_data()
    # summary = loader.get_summary()
    # print(summary)
    print("Módulo data_loader listo para usar")

if __name__ == '__main__':
    main()
