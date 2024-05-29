import networkx as nx
import matplotlib.pyplot as plt

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
      (1, 1, 7), (1, 2, 14), (2, 1, 8), 
      (1, 3, 4), (3, 1, 5), 
      (2, 2, 9), (2, 3, 1), (3, 2, 11),
      (3, 3, 6)
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
    
    
if __name__ == '__main__':
  entorno = Entorno()
  print(entorno.gastar_energia(1, 2))