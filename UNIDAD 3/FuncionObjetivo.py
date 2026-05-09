import numpy as np
import math
from itertools import combinations

# Calcula la distancia en metros entre dos coordenadas (latitud, longitud)
# usando la fórmula de Haversine
def distancia_haversine(punto_1, punto_2):
    RADIO_TIERRA = 6371000.0

    # 1. Convertir grados a radianes
    phi1 = math.radians(punto_1[0])
    lambda1 = math.radians(punto_1[1])
    phi2 = math.radians(punto_2[0])
    lambda2 = math.radians(punto_2[1])

    # 2. Diferencias
    dlon = lambda2 - lambda1
    dlat = phi2 - phi1

    # 3. Aplicar Fórmula de Haversine
    # a = sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)
    a = math.sin(dlat / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlon / 2)**2
    
    # c = 2 * atan2(√a, √(1−a))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 4. Distancia = R * c
    distancia_m = RADIO_TIERRA * c
    
    return distancia_m

# Obtiene la humedad que detectaría un sensor (corresponde al punto más cercano)
def humedad_sensor(sensor, puntos, humedades, p=2):
    dist = []
    for punto in puntos:
        dist.append(distancia_haversine(punto, sensor))
    
    dist = np.array(dist)

    idx = np.argmin(dist)
    h = humedades[idx]
    return h

# Estima la humedad en cada punto de cultivo usando interpolación ponderada
# Se pesa la humedad de cada sensor inversamente a su distancia
def humedad_estimada(puntos, sensores, h_sensores, p=2):
    N = len(puntos)
    h_estim = np.zeros(N)
    for i in range(N):
        dist = []
        for sensor in sensores:
            dist.append(distancia_haversine(puntos[i], sensor))
        
        dist = np.array(dist)
        dist = np.maximum(dist, 1e-6)  # evitar división por 0
        pesos = 1 / (dist ** p)
        h_estim[i] = np.sum(h_sensores * pesos) / np.sum(pesos)
    return h_estim

# Calcula el peso de importancia de cada punto según:
# - Tipo de cultivo (Tomate > Chile > Maíz)
# - Salinidad, temperatura y elevación normalizadas
# Rango de pesos: 0.5 a 4.0
def pesos_puntos_cultivos(cultivos,
                          salinidad,
                          temperatura,
                          elevacion,
                          peso_cultivo=None,
                          alphas=(0.3, 0.2, 0.15),
                          clip_range=(0.5, 4.0)):
    # Default mapping si no se pasa
    if peso_cultivo is None:
        peso_cultivo = {'Tomate': 2.0, 'Chile': 1.5, 'Maíz': 1.0}

    # Peso base por cultivo
    w_cult = np.array([peso_cultivo.get(c, 1.0) for c in cultivos])

    # Aplicar fórmula del peso
    a1, a2, a3 = alphas
    w = w_cult * (1.0 + a1 * salinidad + a2 * temperatura + a3 * elevacion)

    # Clipping
    w = np.clip(w, clip_range[0], clip_range[1])
    return w

# Calcula el error cuadrático medio ponderado (RMSE) entre
# humedad real y humedad estimada
def rmse_ponderado(h_real, h_estim, w):
    num = np.sum(w * (h_real - h_estim)**2)
    den = np.sum(w)
    return np.sqrt(num / den)

# Función objetivo: calcula el error ponderado para una configuración de sensores
# Entrada: posiciones de sensores y datos de cultivos
# Salida: error (menor es mejor)
def funcion_objetivo(sensores, datos):

    (puntos, cultivos, humedades, salinidades, temperaturas, elevaciones) = datos

    h_sensores = np.array([humedad_sensor(s, puntos, humedades)
                           for s in sensores])
    h_estimadas = humedad_estimada(puntos, sensores, h_sensores)
    w = pesos_puntos_cultivos(cultivos, salinidades, temperaturas, elevaciones)

    error_interp = rmse_ponderado(humedades, h_estimadas, w)

    return error_interp
