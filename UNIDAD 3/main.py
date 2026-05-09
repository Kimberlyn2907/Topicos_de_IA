import numpy as np
import LecturaCSV
import ReporteResultados
import FuncionObjetivo

# Ejecuta PSO con datos del archivo CSV
def caso_csv(nombre_csv, n_sensores = 10):
    # Leer datos del CSV
    humedades, cultivos, elevaciones, salinidades, temperaturas, puntos = LecturaCSV.leer_archivo(nombre_csv)

    # Verificar lectura de datos
    print(humedades[:5])
    print(cultivos[:5])
    print(elevaciones[:5])
    print(salinidades[:5])
    print(temperaturas[:5])
    print(puntos[:5])

    datos = (puntos, cultivos, humedades, salinidades, temperaturas, elevaciones)

    # Obtener rango de latitudes
    minimos = np.min(puntos, axis=0)
    latitud_min = minimos[0]
    longitud_min = minimos[1]

    # Obtener rango de longitudes
    maximos = np.max(puntos, axis=0)
    latitud_max = maximos[0]
    longitud_max = maximos[1]

    # Generar reporte
    ReporteResultados.reporte_visual(100, 
                                     n_sensores, 
                                     [[latitud_min, longitud_min], [latitud_max, longitud_max]], 
                                     FuncionObjetivo.funcion_objetivo, 
                                     250,
                                     datos)

# Ejecuta PSO con datos generados aleatoriamente
def caso_random(n_puntos, n_particulas, n_sensores, max_iter):

    # Rango de coordenadas (latitud y longitud)
    lat_min, lat_max = 25.40, 25.80
    lon_min, lon_max = -108.70, -108.30

    # Generar puntos aleatorios
    latitudes = np.random.uniform(lat_min, lat_max, n_puntos)
    longitudes = np.random.uniform(lon_min, lon_max, n_puntos)
    puntos = np.stack((latitudes, longitudes), axis=1)
    
    # Generar humedad (0-100%)
    humedades = np.random.uniform(0.0, 100.0, n_puntos)

    # Generar salinidad, temperatura y elevación (0-1)
    salinidades = np.random.rand(n_puntos)
    temperaturas = np.random.rand(n_puntos)
    elevaciones = np.random.rand(n_puntos)
    
    # Asignar cultivos aleatorios
    opciones_cultivos = np.array(['Tomate', 'Chile', 'Maíz'])
    
    cultivos = np.random.choice(opciones_cultivos, size=n_puntos)

    datos = (puntos, cultivos, humedades, salinidades, temperaturas, elevaciones)

    # Generar reporte
    ReporteResultados.reporte_visual(n_particulas, 
                                     n_sensores, 
                                     [[lat_min, lon_min], [lat_max, lon_max]], 
                                     FuncionObjetivo.funcion_objetivo, 
                                     max_iter,
                                     datos)

# Programa principal
if __name__ == "__main__":
    caso_csv("cultivos.csv")
