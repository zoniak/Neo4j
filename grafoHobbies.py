from neo4j import GraphDatabase

# ---------------- CONFIGURACIÓN ----------------
URI = "bolt://18.206.246.24:7687"
AUTH = ("neo4j", "threads-screwdrivers-eve")


def crear_datos_iniciales(driver):
    """
    Crea alumnos y hobbies usando MERGE para no duplicarlos si ejecutas el script 2 veces.
    """
    # Definimos nuestros datos en una lista de diccionarios (JSON)
    datos_alumnos = [
        {"nombre": "Ana", "hobbies": ["Fútbol", "Pintura", "Guitarra"]},
        {"nombre": "Carlos", "hobbies": ["Pintura", "Ciclismo"]},
        {"nombre": "Elena", "hobbies": ["Guitarra", "Ciclismo", "Ajedrez"]},
        {"nombre": "David", "hobbies": ["Ajedrez", "Fútbol", "Videojuegos"]},
        {"nombre": "Lucía", "hobbies": ["Videojuegos", "Anime"]}
    ]

    query = """
    UNWIND $batch AS row
    MERGE (a:Alumno {nombre: row.nombre})
    WITH a, row
    UNWIND row.hobbies AS hobbyName
    MERGE (h:Hobby {nombre: hobbyName})
    MERGE (a)-[:PRACTICA]->(h)
    """

    try:
        # execute_query gestiona la sesión y transacción automáticamente (Driver 5.x+)
        driver.execute_query(query, batch=datos_alumnos, database_="neo4j")
        print("Datos creados correctamente (Alumnos y Hobbies conectados).")
    except Exception as e:
        print(f"Error al crear datos: {e}")


def encontrar_conexiones(driver):
    """
    Busca qué alumnos tienen hobbies en común.
    """
    print("\n--- CONEXIONES ENCONTRADAS ---")
    
    # Esta query busca: Alumno1 -> Hobby <- Alumno2
    # "id(a1) < id(a2)" sirve para evitar ver duplicados (Ana-Carlos y Carlos-Ana)
    query = """
    MATCH (a1:Alumno)-[:PRACTICA]->(h:Hobby)<-[:PRACTICA]-(a2:Alumno)
    WHERE elementId(a1) < elementId(a2)
    RETURN a1.nombre AS Alumno1, a2.nombre AS Alumno2, collect(h.nombre) AS HobbiesComunes
    ORDER BY size(HobbiesComunes) DESC
    """

    records, _, _ = driver.execute_query(query, database_="neo4j")

    if not records:
        print("No se encontraron conexiones.")
    
    for record in records:
        a1 = record["Alumno1"]
        a2 = record["Alumno2"]
        hobbies = record["HobbiesComunes"]
        print(f"{a1} y {a2} conectan por: {', '.join(hobbies)}")

if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        
        # 1. Crear el grafo
        crear_datos_iniciales(driver)
        
        # 2. Consultar quién debería conocerse
        #encontrar_conexiones(driver)