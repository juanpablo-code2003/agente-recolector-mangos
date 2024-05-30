import networkx as nx
import matplotlib.pyplot as plt



def reemplazar_nodos_sin_sucesores(grafico_general, graficos_de_reemplazo, contador):
    # Obtener todos los nodos sin sucesores
    nodos_sin_sucesores = [nodo for nodo in grafico_general.nodes if len(list(grafico_general.successors(nodo))) == 0]
    print(f'Nodos sin sucesores: {nodos_sin_sucesores}')

    for nodo in nodos_sin_sucesores:
        
        print(f'Nodo a reemplazar: {nodo}')
        # Obtener el nombre del grafo de reemplazo
        nombre_grafo = nodo.split('-')[0]
        print(nombre_grafo)
        
        # Encontrar el grafo de reemplazo
        grafo_reemplazo = next((grafo for grafo in graficos_de_reemplazo if grafo.name == nombre_grafo), None)
        print(grafo_reemplazo)

        if grafo_reemplazo is not None:
            
            print("antes de iteracion")
            for node in grafico_general.nodes:
                connections = list(grafico_general.adj[node])
                connections_with_weights = []
                for connection in connections:
                    weight = grafico_general.edges[node, connection]['weight']
                    connections_with_weights.append(f"{connection}({weight})")
                print(f"{node}: {connections_with_weights}")
            print("---------------------------------------------------")

            # Crear una copia del grafo de reemplazo
            copia_grafo_reemplazo = grafo_reemplazo.copy()

            # Modificar los nombres de los nodos en la copia
            pepe = nodo.split('-')[2]
            print(pepe)
            mapeo = {nodo_viejo: nodo if nodo_viejo.split('-')[1] == '0' else f"{nodo_viejo.split('-')[0]}-{int(nodo.split('-')[1])+int(nodo_viejo.split('-')[1])}-{pepe}-{contador}" 
                     for nodo_viejo in copia_grafo_reemplazo.nodes}
            
            copia_grafo_reemplazo = nx.relabel_nodes(copia_grafo_reemplazo, mapeo)
            print(copia_grafo_reemplazo.nodes)
          
            # Encontrar el nodo padre del nodo sin sucesor
            nodo_padre = next(iter(grafico_general.predecessors(nodo)), None)

            # Encontrar el nodo padre del grafo de reemplazo
            nodo_padre_reemplazo = next((nodo for nodo in copia_grafo_reemplazo.nodes if len(list(copia_grafo_reemplazo.predecessors(nodo))) == 0), None)
            #print(f'{nodo_padre}, {nodo_padre_reemplazo}')

            # Guardar pesos
            pesos = grafico_general.edges[nodo_padre, nodo]['weight']

            # Eliminar el nodo
            grafico_general.remove_node(nodo)
            #print(grafico_general.nodes)

            # Fusionar la copia del grafo de reemplazo en el grafo general
            grafico_general = nx.union(grafico_general, copia_grafo_reemplazo)
            #print(grafico_general.edges)
            
            # Conectar el nodo padre del nuevo grafo al nodo padre del nodo sin sucesor
            if nodo_padre is not None:
              grafico_general.add_edge(nodo_padre, nodo_padre_reemplazo, weight=pesos) 

            print("Despues de iteracion")
            for node in grafico_general.nodes:
                connections = list(grafico_general.adj[node])
                connections_with_weights = []
                for connection in connections:
                    weight = grafico_general.edges[node, connection]['weight']
                    connections_with_weights.append(f"{connection}({weight})")
                print(f"{node}: {connections_with_weights}")
            print("---------------------------------------------------")
        else:
          print("Este nodo es final, no se reemplaza,\n---------------------------------------------------")
        contador += 1
    return grafico_general, contador



def generador_de_grafo():

    s2 = nx.DiGraph()
    s2.name = "s2"
    nodes_s2 = ["s2-0-0-0"]
    edges_s2 = [("s2-0-0-0", "s2-1-0-0", {"weight": ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]}),
                ("s2-0-0-0", "s1-1-0-0", {"weight": ["a3", "a6", "a8"]})]
    s2.add_nodes_from(nodes_s2)
    s2.add_edges_from(edges_s2)

    s3 = nx.DiGraph()
    s3.name = "s3"
    nodes_s3 = ["s3-0-0-0"]
    edges_s3 = [("s3-0-1-0", "s3-1-1-0", {"weight": ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]}),
                ("s3-0-1-0", "s1-1-1-0", {"weight": ["a2", "a4", "a9"]})]
    s3.add_nodes_from(nodes_s3)
    s3.add_edges_from(edges_s3)

    s4 = nx.DiGraph()
    s4.name = "s4"
    nodes_s4 = ["s4-0-2-0"]
    edges_s4 = [("s4-0-2-0", "s4-1-2-0", {"weight": ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]})]
    s4.add_nodes_from(nodes_s4)
    s4.add_edges_from(edges_s4)

    s5 = nx.DiGraph()
    s5.name = "s5"
    nodes_s5 = ["s5-0-3-0"]
    edges_s5 = [("s5-0-3-0", "s5-1-3-0", {"weight": ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]}),
                ("s5-0-3-0", "s1-1-3-0", {"weight": ["a1", "a5", "a7"]})]
    s5.add_nodes_from(nodes_s5)
    s5.add_edges_from(edges_s5)

    s6 = nx.DiGraph()
    s6.name = "s6"
    nodes_s6 = ["s6-0-4-0"]
    edges_s6 = [("s6-0-4-0", "s5-1-4-0", {"weight": ["a3", "a6", "a8"]}), 
                ("s6-0-4-0", "s2-1-4-0", {"weight": ["a1", "a5", "a7"]})]
    s6.add_nodes_from(nodes_s6)
    s6.add_edges_from(edges_s6)

    s7 = nx.DiGraph()
    s7.name = "s7"
    nodes_s7 = ["s7-0-5-0"]
    edges_s7 = [("s7-0-5-0", "s3-1-5-0", {"weight": ["a1", "a5", "a7"]}), 
                ("s7-0-5-0", "s5-1-5-0", {"weight": ["a2", "a4", "a9"]}),
                ("s7-0-5-0", "s7-1-5-0", {"weight": ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]})]
    s7.add_nodes_from(nodes_s7)
    s7.add_edges_from(edges_s7)

    s8 = nx.DiGraph()
    s8.name = "s8"
    nodes_s8 = ["s8-0-6-0"]
    edges_s8 = [("s8-0-6-0", "s6-1-6-0", {"weight": ["a2", "a4", "a9"]}), 
                ("s8-0-6-0", "s7-1-6-0", {"weight": ["a3", "a6", "a8"]}),
                ("s8-0-6-0", "s8-1-6-0", {"weight": ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]}),
                ("s8-0-6-0", "s4-1-6-0", {"weight": ["a1", "a5", "a7"]})
                ]
    s8.add_nodes_from(nodes_s8)
    s8.add_edges_from(edges_s8)



    general = nx.DiGraph()
    general.add_edges_from([
            ("inicial", "s2-0-0-0", {"weight": 1}),
            ("inicial", "s3-0-1-0", {"weight": 1}),
            ("inicial", "s4-0-2-0", {"weight": 1}),
            ("inicial", "s5-0-3-0", {"weight": 1}),
            ("inicial", "s6-0-4-0", {"weight": 1}),
            ("inicial", "s7-0-5-0", {"weight": 1}),
            ("inicial", "s8-0-6-0", {"weight": 1}),
            ])

    # Repetir el proceso de reemplazar los nodos sin sucesores 3 veces
    contador = 1

    for i in range(2):
        print(f'\n\nITERACION {i} \n\n')
        general, contador = reemplazar_nodos_sin_sucesores(general, [s2, s3, s4, s5 ,s6, s7, s8], contador)

    return general

generador_de_grafo()

