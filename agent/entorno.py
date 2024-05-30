import networkx as nx
import matplotlib.pyplot as plt
from agente import Agente

class Arbol:
  def __init__(self, mangos):
    self.mangos = mangos
    
  def set_mangos(self, mangos):
    self.mangos = mangos
    
  def hay_mangos(self):
    return self.mangos > 0
  
  def cosechar(self):
    self.mangos -= 1

class Entorno:
  def __init__(self):
    self.arboles = [
      Arbol(3), Arbol(2), Arbol(5)
    ]
    self.cant_arboles = len(self.arboles)
    self.cant_mangos = sum([arbol.mangos for arbol in self.arboles])
    self.caminos = nx.DiGraph()
    self.caminos.add_nodes_from(list(range(1, self.cant_arboles + 1)))
    self.caminos.add_weighted_edges_from([
      (1, 1, 2), (1, 2, 3), (2, 1, 1), 
      (1, 3, 4), (3, 1, 4), 
      (2, 2, 2), (2, 3, 1), (3, 2, 5),
      (3, 3, 1)
    ])
    
  def hay_mangos(self):
    return self.cant_mangos > 0
  
  def total_mangos(self):
    return self.cant_mangos
  
  def estado_arboles(self):
    return [arbol.hay_mangos() for arbol in self.arboles]
  
  def cosechar(self, arbol):
    if self.arboles[arbol - 1].hay_mangos():
      self.arboles[arbol - 1].cosechar()
      self.cant_mangos -= 1
    else:
      print("No hay mangos en el arbol")

  def gastar_energia(self, arbol1, arbol2):
    return self.caminos[arbol1][arbol2]['weight']
    
    
  def run():
    arbol_actual_lista = []


    entorno = Entorno()
    pepe = Agente()
    print(entorno.gastar_energia(1, 2))
    iteracion = 0

    while (pepe.estado_actual != "s1" and pepe.energia > 0 and entorno.hay_mangos()):
      
      iteracion += 1
      print(f'Iteración {iteracion}')
      print(f'Energía actual: {pepe.energia}')
      print(f'Mangos restantes: {entorno.total_mangos()}')
      print(f'Arbol actual: {pepe.arbol_actual}')
      arbol_actual_lista.append(pepe.arbol_actual)
      
      percepcion, estado = pepe.convertir_estado_arboles(entorno.estado_arboles())
      print(f'percepción: {percepcion}')
      print(f'Estado actual: {estado}')
      
      pepe.llenar_estado_Interno(percepcion, estado)
      accion, estado_esperado = pepe.seleccionar_accion_estado(estado)
      print(f'Accion seleccionada: {accion}')
      entorno.cosechar(pepe.acciones[accion][1])
      pepe.ejecutar_accion(accion, entorno.gastar_energia(*pepe.acciones[accion]))
      pepe.llenar_historial(estado, accion, estado_esperado)
      
      print(f'Estado interno: {pepe.estado_interno}')
      print(f'Historial: {pepe.historial}')
      print(f'Energía restante: {pepe.energia}')
      print('---------------------------------')

      return arbol_actual_lista
      
      
      