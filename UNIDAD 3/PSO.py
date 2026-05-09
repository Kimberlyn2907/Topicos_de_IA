import numpy as np
import Particula

# Implementa el algoritmo PSO (Particle Swarm Optimization)
# para optimizar la posición de sensores
class PSO:

    # Inicializa el enjambre con partículas aleatorias
    # w, c1, c2: parámetros de PSO (inercia, coeficientes local y global)
    def __init__(self, n_particulas, n_sensores, limites, f_objetivo, w = 0.8, c1 = 2, c2 = 2):
        self.particulas = [Particula.Particula(n_sensores, limites) for _ in range(n_particulas)]
        self.f_objetivo = f_objetivo
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.gbest = None
        self.gbest_value = np.inf

    # Ejecuta PSO por max_iters iteraciones
    # Retorna: mejor solución (gbest), su valor y historial de convergencia
    def optimizar(self, max_iters, datos):
        valor_iteracion = []
        for it in range(max_iters):
            print(f"Iteracion {it}/{max_iters}")
            for p in self.particulas:
                p.actualizar_valor(self.f_objetivo, datos)
                if p.valor < self.gbest_value:
                    self.gbest_value = p.valor
                    self.gbest = p.posicion.copy()

            for p in self.particulas:
                p.actualizar_velocidad(self.gbest,
                                       self.w,
                                       self.c1,
                                       self.c2)
                p.mover()

            valor_iteracion.append(self.gbest_value)

        return self.gbest, self.gbest_value, valor_iteracion