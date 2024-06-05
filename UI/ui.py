import pygame
import random
import sys
import os
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent')))

import agente
import entorno

# Configuraciones iniciales
arbol_actual_lista = []
energia = []
mangos = []

entorno = entorno.Entorno()
pepe = agente.Agente(entorno)
print(entorno.gastar_energia(1, 2))
iteracion = 0
estado_esperado = "s1"

while (pepe.estado_actual != "s1" and pepe.energia > 0 and entorno.hay_mangos()):
    print(entorno.hay_mangos())

    if pepe.arbol_actual != None:
        arbol_actual_lista.append(pepe.arbol_actual)

    mangos.append(entorno.total_mangos())

    if pepe.energia >= 0:
        energia.append(pepe.energia)

    iteracion += 1
    print(f'Iteración {iteracion}')
    print(f'Energía actual: {pepe.energia}')
    print(f'Mangos restantes: {entorno.total_mangos()}')
    print(f'Arbol actual: {pepe.arbol_actual}')
    
    percepcion, estado = pepe.convertir_estado_arboles(entorno.estado_arboles())
    print(f'percepción: {percepcion}')
    print(f'Estado actual: {estado}')

    pepe.llenar_estado_Interno(percepcion, estado)
    accion, estado_esperado = pepe.seleccionar_accion_estado(estado, estado_esperado)

    print(f'Accion seleccionada: {accion}')
    entorno.cosechar(pepe.acciones[accion][1])
    pepe.ejecutar_accion(accion, entorno.gastar_energia(*pepe.acciones[accion]))
    pepe.llenar_historial(estado, accion, estado_esperado)

    print(f'Estado interno: {pepe.estado_interno}')
    print(f'Historial: {pepe.historial}')
    print(f'Energía restante: {pepe.energia}')

    print('---------------------------------')

arboles_visitados = arbol_actual_lista

WIDTH, HEIGHT = 800, 600
NUM_TREES = len(entorno.arboles)
TREE_RADIUS = 50
AGENT_RADIUS = 40  # Radio del agente (para colisiones)
STEP_SIZE = 5  # Tamaño del paso del agente
FONT_SIZE = 30

# Inicializa Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entorno de Árboles con Caminos Texturizados")

pygame.font.init()
font = pygame.font.SysFont('Arial', FONT_SIZE)

# Cargar la textura del camino con transparencia
camino_textura = pygame.image.load('images/camino_textura.png').convert_alpha()
camino_textura = pygame.transform.scale(camino_textura, (30, 30))

# Cargar la imagen de fondo y redimensionarla
fondo_imagen = pygame.image.load('images/fondo.jpg').convert()
fondo_imagen = pygame.transform.scale(fondo_imagen, (WIDTH, HEIGHT))

# Cargar la imagen del árbol y redimensionarla
tree_image = pygame.image.load('images/tree.png').convert_alpha()
tree_image = pygame.transform.scale(tree_image, (TREE_RADIUS * 3, TREE_RADIUS * 3))

# Cargar la imagen del agente y redimensionarla
agent_image = pygame.image.load('images/pou.png').convert_alpha()
agent_image = pygame.transform.scale(agent_image, (AGENT_RADIUS * 2, AGENT_RADIUS * 2))

def generate_random_positions(num_positions, width, height, radius):
    positions = []
    for _ in range(num_positions):
        while True:
            x = random.randint(radius, width - radius)
            y = random.randint(radius, height - radius)
            # Asegurarse de que los árboles no se superpongan
            if all(math.hypot(x - px, y - py) > 2 * radius for px, py in positions):
                positions.append((x, y))
                break
    return positions

def draw_trees(screen, positions, tree_image):
    arbol = 0
    for (x, y) in positions:
        arbol += 1
        screen.blit(tree_image, (x - TREE_RADIUS, y - TREE_RADIUS))
        text_surface = font.render(f'A{arbol}', True, (0, 0, 0))
        screen.blit(text_surface, (x*1.01,y*1.03))

def draw_paths_with_texture(screen, positions, texture):
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            draw_textured_line(screen, positions[i], positions[j], texture)

def draw_textured_line(screen, start_pos, end_pos, texture):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    angle = math.atan2(dy, dx)
    length = math.hypot(dx, dy)

    # Repetir la textura a lo largo del camino
    for i in range(0, int(length), texture.get_width()):
        x = x1 + i * math.cos(angle)
        y = y1 + i * math.sin(angle)
        blit_rotate_center(screen, texture, (x, y), math.degrees(angle))

def blit_rotate_center(screen, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, -angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    screen.blit(rotated_image, new_rect.topleft)

def render_text(screen, text, position, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Generar posiciones aleatorias para los árboles
tree_positions = generate_random_positions(NUM_TREES, WIDTH, HEIGHT, TREE_RADIUS)

# Variables para la interpolación
agent_pos = [WIDTH // 2, HEIGHT // 2]
target_pos = agent_pos[:]
moving = False

current_index = 0
mangos_actuales = mangos[0]
energia_disponible = 30

def move_agent(agent_pos, step_size):
    dx = tree_positions[arboles_visitados[0] - 1][0] - agent_pos[0]
    dy = tree_positions[arboles_visitados[0] - 1][1] - agent_pos[1]
    distance = math.hypot(dx, dy)
    if distance < step_size:
        return list(tree_positions[arboles_visitados[0] - 1]), True  # Hemos llegado al objetivo
    angle = math.atan2(dy, dx)
    agent_pos[0] += step_size * math.cos(angle)
    agent_pos[1] += step_size * math.sin(angle)
    return agent_pos, False

# Bucle principal del juego
running = True
while running and arboles_visitados:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(fondo_imagen, (0, 0))  # Dibujar la imagen de fondo redimensionada

    draw_paths_with_texture(screen, tree_positions, camino_textura)  # Dibujar caminos texturizados
    draw_trees(screen, tree_positions, tree_image)  # Dibujar árboles con imagen PNG
    
    # Mover el agente hacia el objetivo
    agent_pos, arrived = move_agent(agent_pos, STEP_SIZE)
    if arrived:
        current_index = arboles_visitados.pop(0)
        mangos_actuales = mangos.pop(0)
        energia_disponible = energia.pop(0)

    # Dibujar al agente en su posición actual
    screen.blit(agent_image, (agent_pos[0] - AGENT_RADIUS, agent_pos[1] - AGENT_RADIUS))
    
    # Renderizar texto
    text = f"Arbol visitado: {current_index}"
    render_text(screen, text, (10, 10), font)

    text = f"Mangos restantes: {mangos_actuales}"
    render_text(screen, text, (10, 40), font)

    text = f"Energía: {energia_disponible}"
    render_text(screen, text, (10, 70), font)

    pygame.time.delay(20)  # Delay for 1 millisecond
    pygame.display.flip()  # Actualizar la pantalla

pygame.quit()
