# ============================================================
# PROBLEMA DEL AGENTE VIAJERO CON ALGORITMOS GENÉTICOS
# ============================================================

import random
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# MATRIZ DE DISTANCIAS ENTRE CIUDADES
# ------------------------------------------------------------

datos = {
    "Madrid":       [0,303,442,223,252,654,737,458,555,279,726,456,876,467,614,249,709,368,435,530],
    "Barcelona":    [303,0,409,591,341,403,263,485,385,671,595,738,591,725,502,328,527,617,144,244],
    "Valencia":     [442,409,0,430,273,639,471,152,709,335,178,574,383,281,387,624,310,480,240,683],
    "Sevilla":      [223,591,430,0,619,431,617,629,754,124,534,630,713,295,491,245,630,295,501,478],
    "Zaragoza":     [252,341,273,619,0,332,606,203,506,470,250,562,563,334,311,760,111,757,631,349],
    "Málaga":       [654,403,639,431,332,0,392,306,432,606,539,401,234,449,709,520,317,192,549,271],
    "Murcia":       [737,263,471,617,606,392,0,854,801,89,617,390,698,595,572,405,183,164,360,337],
    "Palma":        [458,485,152,629,203,306,854,0,390,323,733,391,440,319,252,735,394,408,443,456],
    "Las Palmas":   [555,385,709,754,506,432,801,390,0,671,395,200,684,206,423,792,423,614,241,185],
    "Bilbao":       [279,671,335,124,470,606,89,323,671,0,305,534,406,842,475,516,778,579,483,864],
    "Alicante":     [726,595,178,534,250,539,617,733,395,305,0,767,130,551,463,554,432,593,529,864],
    "Córdoba":      [456,738,574,630,562,401,390,391,200,534,767,0,517,853,205,534,261,380,489,515],
    "Valladolid":   [876,591,383,713,563,234,698,440,684,406,130,517,0,387,558,495,308,557,590,443],
    "Vigo":         [467,725,281,295,334,449,595,319,206,842,551,853,387,0,183,171,438,445,417,678],
    "Gijón":        [614,502,387,491,311,709,572,252,423,475,463,205,558,183,0,527,477,294,625,200],
    "L'Hospitalet": [249,328,624,245,760,520,405,735,792,516,554,534,495,171,527,0,466,664,188,437],
    "Vitoria":      [709,527,310,630,111,317,183,394,423,778,432,261,308,438,477,466,0,761,655,752],
    "A Coruña":     [368,617,480,295,757,192,164,408,614,579,593,380,557,445,294,664,761,0,369,634],
    "Granada":      [435,144,240,501,631,549,360,443,241,483,529,489,590,417,625,188,655,369,0,798],
    "Elche":        [530,244,683,478,349,271,337,456,185,864,864,515,443,678,200,437,752,634,798,0]
}

# Lista con los nombres de las ciudades
ciudades = list(datos.keys())

# FUNCIONES DEL ALGORITMO GENÉTICO

# Se crea una ruta aleatoria
# random.sample mezcla las ciudades aleatoriamente

def crearRuta(ciudades):
    return random.sample(ciudades, len(ciudades))


# ------------------------------------------------------------
# Calcula la distancia total de una ruta, recorre ciudad por ciudad sumando distancias

def distanciaRuta(ruta):
    distancia = 0

    for i in range(len(ruta)):

        # Ciudad actual
        origen = ruta[i]

        # Si no es la ultima ciudad toma la siguiente como destino
        if i + 1 < len(ruta):
            destino = ruta[i + 1]

        # Si es la ultima ciudad regresa a la ciudad inicial
        else:
            destino = ruta[0]

        # Suma la distancia entre origen y destino
        distancia += datos[origen][ciudades.index(destino)]

    return distancia


# ------------------------------------------------------------
# Función fitness
# Mientras menor sea la distancia mejor sera el fitness
def fitness(ruta):
    return 1 / distanciaRuta(ruta)


# ------------------------------------------------------------
# Se crea población inicial y genera varias rutas aleatorias
def poblacionInicial(tamano):

    poblacion = []

    # Se crea tantas rutas como indique el tamaño
    for _ in range(tamano):
        poblacion.append(crearRuta(ciudades))

    return poblacion


# ------------------------------------------------------------
# Ordenar rutas segun su fitness
def rankRutas(poblacion):
    resultados = {}

    for i in range(len(poblacion)):
        resultados[i] = fitness(poblacion[i])

    # Se ordena de mayor fitness a menor
    return sorted(resultados.items(), key=lambda x: x[1], reverse=True)


# ------------------------------------------------------------
# Selección de individuos
# Se usa elitismo + ruleta
def seleccion(popRanked, eliteSize):

    resultados = []

    # ---------------------------
    # ELITISMO
    # Se guarda los mejores individuos
    for i in range(eliteSize):
        resultados.append(popRanked[i][0])

    # ---------------------------
    # MÉTODO DE RULETA
    
    # Se obtene fitness de cada individuo
    fitnesses = [x[1] for x in popRanked]

    # Suma total de fitness
    suma = sum(fitnesses)

    # Calcular probabilidades
    probs = [f / suma for f in fitnesses]

    # Se selecciona el resto
    for _ in range(len(popRanked) - eliteSize):

        pick = random.random()
        actual = 0

        for i in range(len(popRanked)):

            actual += probs[i]

            # Se elije al individuo segun probabilidad
            if actual >= pick:
                resultados.append(popRanked[i][0])
                break

    return resultados


# ------------------------------------------------------------
# Crea mating pool
# grupo de padres para reproducción
def matingPool(poblacion, resultadosSeleccion):

    pool = []

    for i in resultadosSeleccion:
        pool.append(poblacion[i])

    return pool


# ------------------------------------------------------------
# Cruce (Crossover)
# Combina dos padres para crear un hijo
def crossover(parent1, parent2):

    child = []

    # Selecciona un segmento aleatorio
    inicio = int(random.random() * len(parent1))
    fin = int(random.random() * len(parent1))

    startGene = min(inicio, fin)
    endGene = max(inicio, fin)

    # Copia genes del padre 1
    for i in range(startGene, endGene):
        child.append(parent1[i])

    # Completa con genes del padre 2 sin repetir ciudades
    childP2 = [item for item in parent2 if item not in child]

    child.extend(childP2)

    return child


# ------------------------------------------------------------
# Aplica crossover a toda la población
def crossoverPoblacion(pool, eliteSize):

    hijos = []

    # Cantidad de hijos a generar
    length = len(pool) - eliteSize

    # Mezcla individuos
    mezcla = random.sample(pool, len(pool))

    # ---------------------------
    # Conserva élite
    for i in range(eliteSize):
        hijos.append(pool[i])

    # ---------------------------
    # Genera hijos
    for i in range(length):

        child = crossover(
            mezcla[i],
            mezcla[len(pool) - i - 1]
        )

        hijos.append(child)

    return hijos


# ------------------------------------------------------------
# Mutación
# Intercambia ciudades aleatoriamente
def mutacion(individuo, mutationRate):

    for swapped in range(len(individuo)):

        # Aplica mutación segun probabilidad
        if random.random() < mutationRate:

            swapWith = int(random.random() * len(individuo))

            # Intercambia posiciones
            ciudad1 = individuo[swapped]
            ciudad2 = individuo[swapWith]

            individuo[swapped] = ciudad2
            individuo[swapWith] = ciudad1

    return individuo


# ------------------------------------------------------------
# Aplica mutación a toda la población
def mutacionPoblacion(poblacion, mutationRate):

    poblacionMutada = []

    for individuo in poblacion:
        poblacionMutada.append(
            mutacion(individuo, mutationRate)
        )

    return poblacionMutada


# ------------------------------------------------------------
# Se crea la siguiente generación
def siguienteGeneracion(actualGen,
                        eliteSize,
                        mutationRate):

    # Ordena rutas
    popRanked = rankRutas(actualGen)

    # Selecciona mejores individuos
    seleccionResultados = seleccion(
        popRanked,
        eliteSize
    )

    # Crea grupo de padres
    pool = matingPool(
        actualGen,
        seleccionResultados
    )

    # Genera hijos
    hijos = crossoverPoblacion(
        pool,
        eliteSize
    )

    # Se aplica mutación
    siguienteGen = mutacionPoblacion(
        hijos,
        mutationRate
    )

    return siguienteGen


# ------------------------------------------------------------
# ALGORITMO GENÉTICO PRINCIPAL
def algoritmoGenetico(
        tamanoPoblacion,
        eliteSize,
        mutationRate,
        generaciones):

    # Crea población inicial
    poblacion = poblacionInicial(tamanoPoblacion)

    # Lista para guardar progreso
    progreso = []

    # Se ejecutan generaciones
    for i in range(generaciones):

        poblacion = siguienteGeneracion(
            poblacion,
            eliteSize,
            mutationRate
        )

        # Obtiene mejor distancia
        mejorDistancia = 1 / rankRutas(poblacion)[0][1]

        progreso.append(mejorDistancia)

    # Obtiene mejor ruta final
    mejorIndice = rankRutas(poblacion)[0][0]

    mejorRuta = poblacion[mejorIndice]

    print("\nDistancia Final:",
          distanciaRuta(mejorRuta))

    return mejorRuta, progreso


# ============================================================
# EJECUCIÓN PRINCIPAL

if __name__ == "__main__":

    # Ejecuta algoritmo genetico
    mejorRuta, progreso = algoritmoGenetico(
        tamanoPoblacion=50,
        eliteSize=5,
        mutationRate=0.01,
        generaciones=10
    )

    # Muestra mejor ruta encontrada
    print("Mejor ruta:", mejorRuta)

    # ========================================================
    # GRÁFICA DE EVOLUCIÓN
    
    plt.plot(progreso)

    plt.title("Evolución del Algoritmo Genético")
    plt.xlabel("Generaciones")
    plt.ylabel("Distancia")

    plt.show()

    # ========================================================
    # GRÁFICA DE LA RUTA ÓPTIMA
    
    # Coordenadas simuladas para visualizar ciudades
    
    coordenadas = {
        "Madrid": (5,8),
        "Barcelona": (9,9),
        "Valencia": (8,6),
        "Sevilla": (3,3),
        "Zaragoza": (7,8),
        "Málaga": (4,2),
        "Murcia": (7,4),
        "Palma": (10,5),
        "Las Palmas": (1,0),
        "Bilbao": (4,9),
        "Alicante": (8,5),
        "Córdoba": (4,4),
        "Valladolid": (4,7),
        "Vigo": (1,7),
        "Gijón": (3,9),
        "L'Hospitalet": (9,8),
        "Vitoria": (5,9),
        "A Coruña": (0,8),
        "Granada": (5,3),
        "Elche": (8,4)
    }

    # Listas para coordenadas X y Y
    x = []
    y = []

    # Se obtiene coordenadas de cada ciudad
    for ciudad in mejorRuta:

        x.append(coordenadas[ciudad][0])
        y.append(coordenadas[ciudad][1])

    # Regresa al punto inicial
    x.append(coordenadas[mejorRuta[0]][0])
    y.append(coordenadas[mejorRuta[0]][1])

    # Crea gráfica
    plt.figure(figsize=(12,8))

    # Dibuja ruta
    plt.plot(x, y, 'o-')

    # Muestra nombres de ciudades
    for ciudad in mejorRuta:

        plt.text(
            coordenadas[ciudad][0],
            coordenadas[ciudad][1],
            ciudad
        )

    plt.title("Ruta Óptima del Agente Viajero")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.grid(True)

    plt.show()

    # ========================================================
    # MOSTRAR RESULTADOS FINALES
    
    print("\n==============================")
    print(" RUTA RECOMENDADA ")
    print("==============================\n")

    # Convertir lista en texto bonito
    rutaTexto = " → ".join(mejorRuta)

    # Agrega regreso al inicio
    rutaTexto += " → " + mejorRuta[0]

    print(rutaTexto)

    print("\n==============================")
    print(" DISTANCIA TOTAL ")
    print("==============================\n")

    print(distanciaRuta(mejorRuta), "km")