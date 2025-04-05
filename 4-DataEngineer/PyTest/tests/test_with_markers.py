import pytest
import pandas as pd
import numpy as np
import time
import sys
import os

# Añadimos el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.abspath('..'))

@pytest.fixture
def df_ventas():
    """Fixture que carga el dataset de ventas."""
    return pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ventas_productos.csv'))

@pytest.mark.rapido
def test_columnas_requeridas(df_ventas):
    """Test rápido que verifica que el DataFrame tenga las columnas requeridas."""
    columnas_requeridas = ['id', 'fecha', 'producto', 'categoria', 'precio', 'cantidad', 'descuento', 'total']
    for columna in columnas_requeridas:
        assert columna in df_ventas.columns, f"La columna {columna} debería estar presente"

@pytest.mark.lento
def test_calculo_intensivo(df_ventas):
    """Test lento que simula un cálculo intensivo."""
    # Simulamos un cálculo que toma tiempo
    time.sleep(2)

    # Realizamos algún cálculo con el DataFrame
    resultado = df_ventas.groupby(['categoria', 'fecha']).agg({'total': 'sum'}).reset_index()
    assert not resultado.empty, "El resultado no debería estar vacío"

@pytest.mark.validacion
def test_valores_no_negativos(df_ventas):
    """Test que verifica que no haya valores negativos en columnas numéricas."""
    columnas_numericas = ['precio', 'cantidad', 'total']
    for columna in columnas_numericas:
        assert (df_ventas[columna] >= 0).all(), f"No debería haber valores negativos en {columna}"
