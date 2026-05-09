import pandas as pd
import numpy as np

# Lee archivo CSV con datos de cultivos
# Retorna: humedades, cultivos, elevaciones, salinidades, temperaturas, puntos
# Si normalizar=True, escala valores a rango [0, 1]
def leer_archivo(nombre_archivo, normalizar = True):
    puntos_cultivo = pd.read_csv(nombre_archivo)
    humedades = puntos_cultivo.iloc[:, 0].values.astype(float)
    cultivos = puntos_cultivo.iloc[:, 1].values.astype(str)
    elevaciones = puntos_cultivo.iloc[:, 2].values.astype(float)
    salinidades = puntos_cultivo.iloc[:, 3].values.astype(float)
    temperaturas = puntos_cultivo.iloc[:, 4].values.astype(float)
    puntos = puntos_cultivo.iloc[:, 5:7].values.astype(float)

    if normalizar:
        elevaciones = normalizar_arreglo(elevaciones)
        salinidades = normalizar_arreglo(salinidades)
        temperaturas = normalizar_arreglo(temperaturas)

    return humedades, cultivos, elevaciones, salinidades, temperaturas, puntos

# Normaliza un arreglo al rango [0, 1] usando min-max
# Si todos los valores son iguales, retorna ceros
def normalizar_arreglo(arr):
    lo, hi = arr.min(), arr.max()

    if hi - lo == 0:
        return np.zeros_like(arr)

    arr_normalizado = (arr - lo) / (hi - lo)
    
    return arr_normalizado