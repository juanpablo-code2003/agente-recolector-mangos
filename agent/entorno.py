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
      Arbol(5), Arbol(3), Arbol(7)
    ]
    self.cant_arboles = len(self.arboles)
    self.cant_mangos = sum([arbol.mangos for arbol in self.arboles])
    self.caminos = nx.DiGraph()
    self.caminos.add_nodes_from(list(range(1, self._arboles + 1)))
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
    self.arboles[arbol - 1].cosechar()
    self.cant_mangos -= 1
    
    
if __name__ == '__main__':
  entorno = Entorno()
  print(entorno.caminos)
  print(nx.shortest_path(entorno.caminos, 1, 1, weight='weight'))
  print(entorno.caminos.edges.data('weight'))
  nx.draw(entorno.caminos, with_labels=True)
  plt.show()