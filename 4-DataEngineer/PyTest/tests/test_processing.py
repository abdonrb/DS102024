import pytest
import pandas as pd
import numpy as np
import sys
import os

# Añadimos el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.abspath('..'))

from utils.data_processing import calcular_metricas_ventas, categorizar_productos_por_precio, calcular_tendencia_ventas

@pytest.fixture
def df_ventas_sample():
    """Fixture que crea un pequeño DataFrame de muestra para testing."""
    data = {
        'id': [1, 2, 3],
        'fecha': ['2023-01-05', '2023-01-10', '2023-01-15'],
        'producto': ['Laptop HP', 'Monitor Dell', 'Teclado Logitech'],
        'categoria': ['Electrónica', 'Electrónica', 'Accesorios'],
        'precio': [899.99, 249.99, 59.99],
        'cantidad': [1, 2, 3],
        'descuento': [0.05, 0.00, 0.10],
        'total': [854.99, 499.98, 161.97]
    }
    return pd.DataFrame(data)

@pytest.fixture
def df_ventas_completo():
    """Fixture que carga el dataset completo de ventas."""
    return pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ventas_productos.csv'))

def test_calcular_metricas_ventas(df_ventas_sample):
    """Test para la función de cálculo de métricas de ventas."""
    metricas = calcular_metricas_ventas(df_ventas_sample)

    # Verificamos que todas las métricas esperadas estén presentes
    assert set(metricas.keys()) == {'total_ventas', 'promedio_venta', 'total_productos_vendidos', 
                                    'precio_promedio', 'descuento_promedio', 'ahorro_total'}

    # Verificamos algunos cálculos específicos
    assert metricas['total_ventas'] == pytest.approx(1516.94, 0.01)
    assert metricas['total_productos_vendidos'] == 6
    assert metricas['precio_promedio'] == pytest.approx(403.32, 0.01)

def test_calcular_metricas_ventas_dataset_completo(df_ventas_completo):
    """Test para la función de cálculo de métricas con el dataset completo."""
    metricas = calcular_metricas_ventas(df_ventas_completo)

    # Verificamos que todas las métricas sean números válidos
    for metrica, valor in metricas.items():
        assert isinstance(valor, (int, float))
        assert not np.isnan(valor)
        assert not np.isinf(valor)

def test_categorizar_productos_por_precio(df_ventas_sample):
    """Test para la función de categorización de productos por precio."""
    df_categorizado = categorizar_productos_por_precio(df_ventas_sample)

    # Verificamos que se haya añadido la columna de categoría de precio
    assert 'categoria_precio' in df_categorizado.columns

    # Verificamos que las categorías sean correctas
    assert df_categorizado.loc[0, 'categoria_precio'] == 'Lujo'  # Laptop HP: 899.99
    assert df_categorizado.loc[1, 'categoria_precio'] == 'Premium'  # Monitor Dell: 249.99
    assert df_categorizado.loc[2, 'categoria_precio'] == 'Estándar'  # Teclado Logitech: 59.99

    # Verificamos que el DataFrame original no se haya modificado
    assert 'categoria_precio' not in df_ventas_sample.columns

def test_categorizar_productos_dataset_completo(df_ventas_completo):
    """Test para la función de categorización con el dataset completo."""
    df_categorizado = categorizar_productos_por_precio(df_ventas_completo)

    # Verificamos que se haya añadido la columna de categoría de precio
    assert 'categoria_precio' in df_categorizado.columns

    # Verificamos que todas las filas tengan una categoría válida
    categorias_validas = {'Económico', 'Estándar', 'Premium', 'Lujo', 'Sin categoría'}
    assert set(df_categorizado['categoria_precio'].unique()).issubset(categorias_validas)

    # Verificamos que haya al menos un producto en cada categoría principal
    for categoria in ['Económico', 'Estándar', 'Premium', 'Lujo']:
        assert categoria in df_categorizado['categoria_precio'].values, f"No hay productos en la categoría {categoria}"

def test_calcular_tendencia_ventas(df_ventas_sample):
    """Test para la función de cálculo de tendencia de ventas."""
    tendencia = calcular_tendencia_ventas(df_ventas_sample)

    # Verificamos que el DataFrame tenga las columnas esperadas
    assert set(tendencia.columns) == {'mes', 'total', 'variacion_porcentual'}

    # Verificamos que solo haya un mes (ya que todas las fechas son de enero 2023)
    assert len(tendencia) == 1
    assert tendencia.iloc[0]['mes'] == '2023-01'
    assert tendencia.iloc[0]['total'] == pytest.approx(1516.94, 0.01)
    assert np.isnan(tendencia.iloc[0]['variacion_porcentual'])  # No hay mes anterior para comparar

def test_calcular_tendencia_dataset_completo(df_ventas_completo):
    """Test para la función de tendencia con el dataset completo."""
    tendencia = calcular_tendencia_ventas(df_ventas_completo)

    # Verificamos que el DataFrame tenga las columnas esperadas
    assert set(tendencia.columns) == {'mes', 'total', 'variacion_porcentual'}

    # Verificamos que haya al menos un mes
    assert len(tendencia) > 0

    # Verificamos que los meses estén en formato YYYY-MM
    import re
    for mes in tendencia['mes']:
        assert re.match(r'^\d{4}-\d{2}$', mes), f"El mes {mes} no tiene el formato esperado (YYYY-MM)"
