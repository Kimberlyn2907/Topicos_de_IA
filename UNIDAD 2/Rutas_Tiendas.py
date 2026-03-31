#NOTA: El código es interactivo, el ususario puede encontrar lo optimo y decidir si seguir iterando para
#encontrar una mejor solución. El proceso mientras no encuentre uno mejor va a seguir preguntando cada vez,
#y si encuentra va a mostrarlo en pantalla, una vez que le digan que no (N), el proceso se detendrá
#para proceder a enviar a pantalla los resultados obtenidos.

import pandas as pd
import random
from collections import deque

#Aquí se ingresan los datos de las tiendas, centros de distribución, matriz de distancias y matriz de costos de combustible.
#Luego se ejecuta la búsqueda tabú interactiva para optimizar las rutas de distribución.
#Al final, se muestra el resultado con el costo total, porcentaje de mejora y las iteraciones iniciales y finales.
def read_distances():
    #Lee la matriz de distancias desde un archivo CSV y la convierte en lista de listas.
    distances_df = pd.read_csv("matriz_distancias.csv")
    distances = distances_df.values.tolist()
    return distances

def read_fuel_costs():
    #Lee la matriz de costos de combustible desde un archivo CSV.
    fuel_df = pd.read_csv("matriz_costos_combustible.csv")
    fuel_costs = fuel_df.values.tolist()
    return fuel_costs

def read_store_data():
    #Lee los datos de centros de distribución y tiendas. Separa los registros según el tipo y los devuelve como listas de diccionarios.
    df = pd.read_csv("datos_distribucion_tiendas.csv")

    centers = df[df["Tipo"] == "Centro de Distribución"]
    stores = df[df["Tipo"] == "Tienda"]

    centers = centers[["Nombre", "Latitud_WGS84", "Longitud_WGS84"]].to_dict(orient="records")
    stores = stores[["Nombre", "Latitud_WGS84", "Longitud_WGS84"]].to_dict(orient="records")

    return centers, stores

#Solución inicial: se asigna cada tienda al centro de distribución más cercano, creando rutas iniciales para cada centro.
def generate_initial_solve(num_centers, num_stores, distance):
    #Se genera una solución inicial asignando cada tienda al centro más cercano.
    #Cada ruta comienza con un centro de distribución y luego se le asignan tiendas.
    routes = []
    # Inicializar cada ruta con su centro de distribución (índices 0..num_centers-1)
    for i in range(num_centers):
        routes.append([i])
    # Mezclar las tiendas para evitar sesgos en la asignación inicial
    random_stores = random.sample(range(num_centers, num_centers + num_stores), num_stores)
    
    for id_store in random_stores:
        best_route = 0 # Suponemos que el primer centro es el mejor inicialmente
        for j in range(num_centers):
            last_loc = routes[j][-1]
            best_loc = routes[best_route][-1]
            # Si la distancia desde el centro j a la tienda es menor, actualizamos mejor ruta
            if distance[last_loc][id_store] < distance[best_loc][id_store]:
                best_route = j
        routes[best_route].append(id_store) # Asignamos la tienda al centro más cercano
    
    return routes

#Aquí se calcula el costo total de las rutas, considerando tanto la distancia como el costo de combustible entre 
# cada par de ubicaciones en las rutas.
def calculate_cost(routes, num_centers, distances, fuel_costs):
    # El costo es la suma de (distancia * costo de combustible) para cada par de puntos consecutivos en cada ruta.
    # También considera el retorno al centro (por eso se usa (j+1) % len(route)).
    cost = 0
    for i in range(num_centers):
        route = routes[i]
        for j in range(len(route)):
            a = route[j]
            b = route[(j + 1) % len(route)]
            cost += distances[a][b] * fuel_costs[a][b]
    return cost

#Aquí se busca encontrar la mejor ubicación de una tienda dentro de las rutas,
#  evaluando el costo de mover una tienda a otra posición en las rutas y seleccionando la que ofrezca
#  la mayor reducción de costo.
def best_relocation(routes, cost, num_centers, distances, fuel_costs, pos_store):
    (route, pos) = pos_store
    store = routes[route][pos] # Tienda que se va a mover

    a = routes[route][pos - 1]
    c = routes[route][(pos + 1) % len(routes[route])] # Ubicaciones antes y después de la tienda en su ruta actual

    #Costo de eliminar la tienda de su posición actual (considerando el cambio en la ruta)
    cost1 = (distances[a][c] * fuel_costs[a][c]) - \
            ((distances[a][store] * fuel_costs[a][store]) + 
             (distances[store][c] * fuel_costs[store][c]))

    best_relocation_cost = float('inf')
    movs = ()
    # Evaluar todas las posibles ubicaciones para la tienda en otras rutas
    for i in range(num_centers):
        lenRoute = len(routes[i])
        for j in range(lenRoute):
            if route == i and (pos == j or pos - 1 == j):
                continue

            d = routes[i][j]
            e = routes[i][(j + 1) % lenRoute]

            cost_act = cost + cost1 + \
                ((distances[d][store] * fuel_costs[d][store]) + 
                 (distances[store][e] * fuel_costs[store][e])) - \
                (distances[d][e] * fuel_costs[d][e])
            # Si el costo de mover la tienda a esta nueva ubicación es mejor que la mejor encontrada, actualizamos
            if cost_act < best_relocation_cost:
                best_relocation_cost = cost_act
                movs = (route, pos, i, j)

    return (best_relocation_cost, movs)

#Aquí se busca generar los vecinos, aplicando lo anterior de la mejor ubicación y creando nuevas rutas.
def generate_neighbor(routes, movs):
    (route_or, pos_or, route_tg, pos_tg) = movs
    store = routes[route_or][pos_or]

    new_routes = [row[:] for row in routes]
    # Si la tienda está en la lista tabú, no se considera
    if route_or != route_tg or pos_or > pos_tg:
        pos_tg += 1
    # Si encontramos una mejora, se guarda
    new_routes[route_or].pop(pos_or) # Eliminamos la tienda de su ruta original
    new_routes[route_tg].insert(pos_tg, store) 

    return new_routes

#Aquí se busca generar el mejor vecino, evaluando todas las posibles ubicaciones de las tiendas 
#y seleccionando la que ofrezca la mayor reducción de costo
def generate_best_neighbor(routes, cost, num_centers, distances, fuel_costs, tabu_stores):
    best_cost = float('inf')
    movs = ()
    for i in range(num_centers):
        for j in range(1, len(routes[i])):

            if routes[i][j] in tabu_stores:
                continue

            (cost_act, movs_act) = best_relocation(
                routes, cost, num_centers, distances, fuel_costs, (i, j)
            )

            if cost_act < best_cost:
                best_cost = cost_act
                movs = movs_act
    #Si se encontró algún movimiento, generamos el vecino y agregamos la tienda a la lista tabú
    if movs:
        best_neighbor = generate_neighbor(routes, movs)
        (route_or, pos_or, _, _) = movs
        tabu_stores.append(routes[route_or][pos_or])
        return (best_neighbor, best_cost)
    else:
        # Si no se encontró ningún movimiento, se devuelve la solución actual sin cambios
        return (routes, cost)

#Implementación de la búsqueda tabú, donde se itera buscando el mejor vecino y actualizando las rutas y costos
def solve(num_centers, num_stores, distances, fuel_costs):
    N = num_centers + num_stores
    #Generamos una solución inicial y calculamos su costo
    act_routes = generate_initial_solve(num_centers, num_stores, distances)
    act_cost = calculate_cost(act_routes, num_centers, distances, fuel_costs)

    best_routes = act_routes
    best_cost = act_cost

    # Registrar evolución del costo en cada iteración
    steps = [act_cost]

    max_tabu = N // 10
    tabu_stores = deque() # Cola para almacenar las tiendas prohibidas temporalmente
    iteration = 0

    print(f"\nSolución inicial: {act_cost:.2f}")

    # Bucle principal de búsqueda tabú
    while True:
        iteration += 1
        previous_best = best_cost
        # Generar el mejor vecino posible (respetando la lista tabú)
        (best_neighbor, neighbor_cost) = generate_best_neighbor(
            act_routes, act_cost, num_centers, distances, fuel_costs, tabu_stores
        )

        if neighbor_cost < best_cost:
            best_cost = neighbor_cost
            best_routes = best_neighbor
            print(f"Iteración {iteration} - Mejor costo encontrado: {best_cost:.2f}")
         # Mantener la lista tabú dentro del tamaño maximo
        if len(tabu_stores) > max_tabu:
            tabu_stores.popleft()
         # Actualizar la solución actual
        act_routes = best_neighbor
        act_cost = neighbor_cost
        steps.append(act_cost)

        # Preguntar al usuario si desea continuar buscando
        if best_cost == previous_best and iteration > 1:
            respuesta = input(f"\nNo se encontró mejora en esta iteración. ¿Desea seguir buscando? (S/N): ").upper()
            if respuesta in ['N', 'NO', 'NOT', 'n']:
                break

    return (best_routes, best_cost, steps, steps[0])

#MAIN
def main():
     # Cargar datos desde archivos CSV
    distances = read_distances() 
    fuel_costs = read_fuel_costs()
    centers, stores = read_store_data()
    routes, cost, steps, initial_cost = solve(
        len(centers), len(stores), distances, fuel_costs
    )

    # Calcular porcentaje de mejora
    mejora = ((initial_cost - cost) / initial_cost) * 100

    # Muestra rutas optimizadas
    print("\nMEJOR RUTA:")
    print(routes)

    # Muestra costo total con solo 2 decimales 
    print(f"\nCOSTO TOTAL: {cost:.2f} uS")

    # Muestra porcentaje de mejora
    print(f"\nPORCENTAJE DE MEJORA: {mejora:.2f}%")

    # Muestra primeras 10 iteraciones con 2 decimales
    print("\nPRIMERAS 10 ITERACIONES:")
    primeros = [f"{val:.2f}" for val in steps[:10]]
    print(primeros)

    # Muestra últimas 10 iteraciones con 2 decimales
    print("\nÚLTIMAS 10 ITERACIONES:")
    ult = [f"{val:.2f}" for val in steps[-10:]]
    print(ult)
main()
