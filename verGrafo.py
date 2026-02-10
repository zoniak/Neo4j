import matplotlib.pyplot as plt
import networkx as nx
from neo4j import GraphDatabase

# --- CONFIGURACIÓN ---
URI = "bolt://18.206.246.24:7687"
AUTH = ("neo4j", "threads-screwdrivers-eve")


def obtener_datos(driver):
    # Traemos todas las relaciones: Alumno -> Hobby
    query = "MATCH (a:Alumno)-[:PRACTICA]->(h:Hobby) RETURN a.nombre AS alumno, h.nombre AS hobby"
    records, _, _ = driver.execute_query(query, database_="neo4j")
    return records

def visualizar():
    # 1. Conectar y extraer datos
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        records = obtener_datos(driver)

    # 2. Crear un objeto Grafo de NetworkX
    G = nx.Graph()

    # Listas para separar tipos de nodos (para colorearlos después)
    alumnos = set()
    hobbies = set()

    # 3. Llenar el grafo con los datos de Neo4j
    for record in records:
        alumno = record["alumno"]
        hobby = record["hobby"]
        
        G.add_node(alumno, type="alumno")
        G.add_node(hobby, type="hobby")
        G.add_edge(alumno, hobby)
        
        alumnos.add(alumno)
        hobbies.add(hobby)

    # 4. Configurar el diseño visual (Colores y Tamaños)
    pos = nx.spring_layout(G, seed=42)  # Algoritmo para distribuir los nodos de forma bonita
    
    # Crear lista de colores: Azul para alumnos, Verde para hobbies
    color_map = []
    for node in G:
        if node in alumnos:
            color_map.append('skyblue')
        else:
            color_map.append('lightgreen')

    # 5. DIBUJAR
    plt.figure(figsize=(10, 8)) # Tamaño de la imagen
    
    nx.draw(G, pos, 
            node_color=color_map, 
            with_labels=True, 
            node_size=2000, 
            font_size=10, 
            font_weight="bold", 
            edge_color="gray")
    
    # Título y mostrar
    plt.title("Red de Alumnos y Hobbies", fontsize=15)
    plt.show()

if __name__ == "__main__":
    visualizar()