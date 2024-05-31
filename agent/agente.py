import random
from statistics import mean
import networkx as nx
from grafo_we import generador_de_grafo


class Agente:
  sensors = None
  actuators = None
  
  def __init__(self, entorno):
    self.mangos = None 
    self.energia = 30
    self.objetivo = "s1"
    self.historial = []
    self.estado_interno = []
    self.arbol_actual = 1
    self.estado_actual = "s8"
    self.entorno = entorno
    self.estrategia_planeada = []
    self.iteraciones = 0

    # Percepciones
    self.percepciones = {

      "p1":([0,0,0], 0),
      "p2":([0,0,1],(1,11)),
      "p3":([0,1,0],(1,11)),
      "p4":([0,1,1],(2,11)),
      "p5":([1,0,0],(1,11)),
      "p6":([1,0,1],(2,11)),
      "p7":([1,1,0],(2,11)),
      "p8":([1,1,1],(3,11))

    }

    # Estados del entorno
    self.estados = {
      "s1": "Todos los mangos recolectados",
      "s2": "Mangos en arbol 3",
      "s3": "Mangos en arbol 2",
      "s4": "Mangos en arboles 2 y 3",
      "s5": "Mangos en arbol 1",
      "s6": "Mangos en arboles 1 y 3",
      "s7": "Mangos en arboles 1 y 2",
      "s8": "Mangos en arboles 1, 2 y 3"
    }
    
    self.relaciones = {
      "p1": "s1",
      "p2": "s2",
      "p3": "s3",
      "p4": "s4",
      "p5": "s5",
      "p6": "s6",
      "p7": "s7",
      "p8": "s8"
    }

    # Acciones
    self.acciones = {
      "a1": (1, 1),
      "a2": (2, 2),
      "a3": (3, 3),
      "a4": (1, 2),
      "a5": (2, 1),
      "a6": (1, 3),
      "a7": (3, 1),
      "a8": (2, 3),
      "a9": (3, 2)
    }


    # Evolución del entorno
    self.w = {
      's1': [('p1', 's1')],
      's2': [('p1', 's1'), ('p2', 's2')],
      's3': [('p1', 's1'), ('p3', 's3')],
      's4': [('p4', 's4'), ('p3', 's3')],
      's5': [('p2', 's2'), ('p5', 's5'), ('p1', 's1')],
      's6': [('p6', 's6'), ('p5', 's5'), ('p2', 's2')],
      's7': [('p7', 's7'), ('p5', 's5'), ('p3', 's3')],
      's8': [('p8', 's8'), ('p7', 's7'), ('p6', 's6'), ('p4', 's4')]
    }

    self.we = {
      's2': [('a1', 's2'), ('a2', 's2'), ('a3', 's2'), ('a4', 's2'), ('a5', 's2'), ('a6', 's2'),
            ('a7', 's2'), ('a8', 's2'), ('a9', 's2'), ('a3', 's1'), ('a6', 's1'), ('a8', 's1')],
      's3': [('a1', 's3'), ('a2', 's3'), ('a3', 's3'), ('a4', 's3'), ('a5', 's3'), ('a6', 's3'),
            ('a7', 's3'), ('a8', 's3'), ('a9', 's3'), ('a2', 's1'), ('a4', 's1'), ('a9', 's1')],
      's4': [('a1', 's4'), ('a2', 's4'), ('a3', 's4'), ('a4', 's4'), ('a5', 's4')],
      's5': [('a1', 's5'), ('a2', 's5'), ('a3', 's5'), ('a4', 's5'), ('a5', 's5'), ('a6', 's5'), ('a7', 's5'), ('a8', 's5'), ('a9', 's5'),
             ('a1', 's1'), ('a5', 's1'), ('a7', 's1')],
      's6': [('a1', 's2'), ('a5', 's2'), ('a7', 's2'), ('a3', 's5'), ('a6', 's5'), ('a8', 's5')],
      's7': [('a1', 's7'), ('a2', 's7'), ('a3', 's7'), ('a4', 's7'), ('a5', 's7'), ('a6', 's7'),
            ('a7', 's7'), ('a8', 's7'), ('a9', 's7'), ('a1', 's3'), ('a5', 's3'), ('a7', 's3'),
            ('a2', 's5'), ('a4', 's5'), ('a9', 's5')],
      's8': [('a1', 's8'), ('a2', 's8'), ('a3', 's8'), ('a4', 's8'), ('a5', 's8'), ('a6', 's8'),
            ('a7', 's8'), ('a8', 's8'), ('a9', 's8'), ('a1', 's4'), ('a5', 's4'), ('a7', 's4'),
            ('a2', 's6'), ('a4', 's6'), ('a9', 's6'), ('a3', 's7'), ('a6', 's7'), ('a8', 's7')]
    }

  
  def llenar_estado_Interno(self, percepcion, estado):
    self.estado_interno.append((percepcion, estado))
    self.estado_actual = estado

  def llenar_historial(self, estado_actual, accion ,estado_esperado):
    self.historial.append((estado_actual, accion, estado_esperado))

  def convertir_estado_arboles(self, estado_arboles):
    estado_arboles = [int(i) for i in estado_arboles]
    for p, v in self.percepciones.items():
      if v[0] == estado_arboles:
        return p, self.relaciones[p]
      
  def seleccionar_accion_estado(self, estado_real, estado_esperado):
    if (estado_real != estado_esperado):
      estrategia_creada = self.estrategia(estado_real)
      for i in range(1, len(estrategia_creada)):
        accion_elegida = random.choice(self.acciones_posibles())
        for j in estrategia_creada[i][0]:
          if j in self.acciones_posibles():
            accion_elegida = j
            break
        estrategia_creada[i][0] = accion_elegida
      if len(self.estrategia_planeada) > 0:
        nueva_estrategia = estrategia_creada[1:]
        if self.iteraciones == len(self.estrategia_planeada):
          self.estrategia_planeada[-1] = [self.estrategia_planeada[-1][0], estrategia_creada[0][1]]
          self.estrategia_planeada.extend(nueva_estrategia)
        else:
          estrategia_recorrida = self.estrategia_planeada[:self.iteraciones]
          estrategia_recorrida[-1] = [self.estrategia_planeada[-1][0], estrategia_creada[0][1]]
          self.estrategia_planeada = estrategia_recorrida
          self.estrategia_planeada.extend(nueva_estrategia)
      else:
        self.estrategia_planeada = estrategia_creada
        
    print(self.estrategia_planeada[self.iteraciones])
    return self.estrategia_planeada[self.iteraciones] if self.estrategia_planeada[self.iteraciones][0] is not None else [random.choice(self.acciones_posibles()), self.estrategia_planeada[self.iteraciones][1]]
  
  def acciones_posibles(self):
    acciones = list()
    for accion, arboles in self.acciones.items():
      if arboles[0] == self.arbol_actual:
        acciones.append(accion)
        
    return acciones
  
  def traduccion_weights(self, nodo1, nodo2, arista):
    pesos = []
    for accion in arista['weight']:
      arboles = self.acciones[accion]
      pesos.append(self.entorno.caminos[arboles[0]][arboles[1]]['weight'])
    
    return mean(pesos)
  
  def estrategia(self, estado):
    if estado == "s1":
      return []
    else:
      grafo = generador_de_grafo()
      paths = nx.shortest_path(grafo, source=f'{estado}-0-{int(estado[1])-2}-0', weight=self.traduccion_weights)
      paths_objetivo = [path for final, path in paths.items() if 's1' in final]
      elegido = random.choice(paths_objetivo)
      estrategia = [(None ,elegido[0][0:2])]
      for i in range(len(elegido) - 1):
        estrategia.append([grafo[elegido[i]][elegido[i+1]]['weight'], elegido[i+1][0:2]])
        
      return estrategia
      
  
  def ejecutar_accion(self, accion, energia_consumida):
    self.energia -= energia_consumida
    self.arbol_actual = self.acciones[accion][1]
    self.iteraciones += 1
    return self.arbol_actual
