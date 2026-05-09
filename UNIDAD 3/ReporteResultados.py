import matplotlib.pyplot as plt
import numpy as np
import PSO

# Ejecuta PSO y retorna mejor solución (gbest), su valor y historial de convergencia
def reporte(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos):
    pso = PSO.PSO(n_particulas, n_sensores, limites, f_objetivo)

    gbest, gbest_value, valor_iteracion = pso.optimizar(max_iter, datos)

    return gbest, gbest_value, valor_iteracion

# Muestra resultados de PSO en consola (parámetros, mejor valor, posiciones)
def reporte_consola(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos):

    gbest, gbest_value, valor_iteracion = reporte(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos)

    # Parámetros iniciales
    print("VALORES INICIALES:")
    print(f"Número de partículas (soluciones): {n_particulas}")
    print(f"Número de sensores a optimizar:   {n_sensores}")
    print(f"Número máximo de iteraciones:    {max_iter}")
    print("-" * 50)
    
    # Resultados finales
    print("RESULTADOS FINALES:")
    print(f"Mejor valor encontrado (gbest_value): {gbest_value}")
    print(f"Mejor posición encontrada (gbest):\n{gbest}")
    print("-" * 50)

    print("HISTORIAL DE CONVERGENCIA")
    print(f"{valor_iteracion}")

# Muestra resultados de PSO con gráficas: convergencia y ubicación de sensores
def reporte_visual(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos):

    (puntos, cultivos, _, _, _, _) = datos

    gbest, gbest_value, valor_iteracion = reporte(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos)

    # Gráfica 1: Convergencia del algoritmo por iteración
    plt.figure(figsize=(10, 6))
    if valor_iteracion is not None and len(valor_iteracion) > 0:
        plt.plot(range(1, len(valor_iteracion) + 1), valor_iteracion, marker='o', linestyle='-', color='blue')
        plt.title('Convergencia del Mejor Valor Global por Iteración')
        plt.xlabel('Número de Iteración')
        plt.ylabel('Mejor Valor Global (gbest_value)')
        plt.grid(True)
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    else:
        plt.text(0.5, 0.5, "No hay datos de historial de iteración disponibles.", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.title('Convergencia del Mejor Valor Global')
    plt.show()

    # Gráfica 2: Puntos de cultivo y posición óptima de sensores
    plt.figure(figsize=(12, 8))

    # Mostrar sensores óptimos en rojo
    plt.scatter(gbest[:, 1], gbest[:, 0], # Longitud en X, Latitud en Y
                marker='X', 
                color='red', 
                s=200,
                edgecolors='black', 
                label='Sensores Óptimos')

    # Definir colores para los cultivos
    colores_cultivos = {}
    cultivos_unicos = np.unique(cultivos)
    cmap = plt.cm.get_cmap('tab10', len(cultivos_unicos))
    for i, c_name in enumerate(cultivos_unicos):
        colores_cultivos[c_name] = cmap(i)

    # Mostrar puntos de cultivo por tipo con colores diferenciados
    for c_name in cultivos_unicos:
        idx = (cultivos == c_name)
        plt.scatter(puntos[idx, 1], puntos[idx, 0], 
                    color=colores_cultivos[c_name], 
                    label=f'Cultivo: {c_name}', 
                    alpha=0.6, s=50)
        
    # Creamos la cadena de texto a mostrar
    texto_solucion = f"Mejor Valor (Fitness): {gbest_value:.4f}"

    # Configuración del gráfico
    plt.title('Distribución de Puntos de Muestreo y Posición Optima de Sensores. ' + texto_solucion)
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    plt.tight_layout()
    plt.show()