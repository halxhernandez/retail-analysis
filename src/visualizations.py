"""
Módulo para visualización de datos de retail.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional, List

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class RetailVisualizer:
    """Clase para crear visualizaciones del análisis de ventas retail."""

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el visualizador.

        Args:
            df: DataFrame con datos de retail.
        """
        self.df = df

    def _validate_columns(self, required_cols: List[str]):
        """Valida que existan las columnas necesarias en el DataFrame."""
        missing = [c for c in required_cols if c not in self.df.columns]
        if missing:
            raise KeyError(f"Faltan columnas requeridas en el DataFrame: {missing}")

    def plot_sales_over_time(self, freq: str = 'M', save_path: Optional[str] = None):
        """Gráfico de ventas a lo largo del tiempo."""
        self._validate_columns(['InvoiceDate', 'TotalAmount'])

        sales_time = self.df.groupby(
            pd.Grouper(key='InvoiceDate', freq=freq)
        )['TotalAmount'].sum()

        plt.figure(figsize=(14, 6))
        plt.plot(sales_time.index, sales_time.values, linewidth=2, marker='o')
        plt.title('Evolución de Ventas en el Tiempo', fontsize=16, fontweight='bold')
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Ventas Totales (£)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()

    def plot_top_countries(self, top_n: int = 10, save_path: Optional[str] = None):
        """Gráfico de top países por ventas."""
        self._validate_columns(['Country', 'TotalAmount'])

        country_sales = self.df.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False)
        top_countries = country_sales.head(top_n)

        plt.figure(figsize=(12, 8))
        colors = sns.color_palette("viridis", len(top_countries))
        bars = plt.barh(range(len(top_countries)), top_countries.values, color=colors)
        plt.yticks(range(len(top_countries)), top_countries.index)
        plt.xlabel('Ventas Totales (£)', fontsize=12)
        plt.title(f'Top {top_n} Países por Ventas', fontsize=16, fontweight='bold')
        plt.gca().invert_yaxis()

        # Agregar valores
        for bar in bars:
            width = bar.get_width()
            plt.text(width + top_countries.max() * 0.01,
                     bar.get_y() + bar.get_height() / 2,
                     f'£{width:,.0f}', ha='left', va='center', fontsize=9)

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()

    def plot_top_products(self, top_n: int = 15, save_path: Optional[str] = None):
        """Gráfico de productos más vendidos."""
        self._validate_columns(['Description', 'Quantity'])

        product_sales = self.df.groupby('Description')['Quantity'].sum().sort_values(ascending=False)
        top_products = product_sales.head(top_n)

        plt.figure(figsize=(12, 8))
        colors = sns.color_palette("rocket", len(top_products))
        plt.barh(range(len(top_products)), top_products.values, color=colors)
        plt.yticks(range(len(top_products)),
                   [desc[:40] + '...' if len(desc) > 40 else desc
                    for desc in top_products.index])
        plt.xlabel('Cantidad Vendida', fontsize=12)
        plt.title(f'Top {top_n} Productos Más Vendidos', fontsize=16, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()

    def plot_sales_distribution(self, save_path: Optional[str] = None):
        """Distribución de montos de venta."""
        self._validate_columns(['TotalAmount'])

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Histograma
        axes[0].hist(self.df['TotalAmount'], bins=50, color='steelblue', edgecolor='black')
        axes[0].set_xlabel('Monto de Venta (£)', fontsize=12)
        axes[0].set_ylabel('Frecuencia', fontsize=12)
        axes[0].set_title('Distribución de Montos de Venta', fontsize=14, fontweight='bold')
        axes[0].set_xlim(0, self.df['TotalAmount'].quantile(0.95))

        # Boxplot
        axes[1].boxplot(self.df['TotalAmount'], vert=True)
        axes[1].set_ylabel('Monto de Venta (£)', fontsize=12)
        axes[1].set_title('Boxplot de Montos de Venta', fontsize=14, fontweight='bold')
        axes[1].set_ylim(0, self.df['TotalAmount'].quantile(0.95))

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()


def main():
    """Función de prueba."""
    print("Módulo de visualizaciones listo para usar.")


if __name__ == '__main__':
    main()
