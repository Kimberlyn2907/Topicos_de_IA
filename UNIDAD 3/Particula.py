import numpy as np

# Representa una partícula del enjambre para PSO
# Atributos: posición, velocidad, mejor_posición, mejor_valor
class Particula:
    # Inicializa partícula con posición aleatoria y velocidad en ceros
    # limites: [[min_lat, min_lon], [max_lat, max_lon]]  

    def __init__(self, n_sensores, limites):
        self.limites = limites
        self.n_sensores = n_sensores

        self.posicion = np.random.uniform(limites[0], limites[1], size=(n_sensores, 2))
        self.velocidad = np.zeros((n_sensores, 2))
        self.mejor_posicion = self.posicion.copy()
        self.mejor_valor = np.inf
        self.valor = np.inf

    # Calcula valor de posición actual y actualiza el mejor si es necesario

    def actualizar_valor(self, f_objetivo, datos):
        self.valor = f_objetivo(self.posicion, datos)
        if self.valor < self.mejor_valor:
            self.mejor_valor = self.valor
            self.mejor_posicion = self.posicion.copy()

    # Actualiza velocidad según PSO: inercia + componente local + componente global
    def actualizar_velocidad(self, gbest, w, c1, c2):
        r1, r2 = np.random.rand(), np.random.rand()
        self.velocidad = (w*self.velocidad
                         + c1*r1*(self.mejor_posicion - self.posicion)
                         + c2*r2*(gbest - self.posicion))

    # Actualiza posición según velocidad y mantiene dentro de límites
    def mover(self):
        self.posicion += self.velocidad
        self.posicion = np.clip(self.posicion, self.limites[0], self.limites[1])