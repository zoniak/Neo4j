from neo4j import GraphDatabase, RoutingControl

# ---------------- CONFIGURACIÓN ----------------
URI = "bolt://18.234.167.38:7687" 
USUARIO = "neo4j"
PASSWORD = "reactions-department-sums"

def conectar_y_consultar():
    # 1. Crear el driver (el objeto que gestiona las conexiones)
    # Se recomienda usar 'with' para cerrar la conexión automáticamente al terminar
    try:
        with GraphDatabase.driver(URI, auth=(USUARIO, PASSWORD)) as driver:
            
            # 2. Verificar conectividad básica
            driver.verify_connectivity()
            print("¡Conexión exitosa a Neo4j Sandbox!")

            # 3. Ejecutar una consulta de prueba (Cypher)
            # Esta consulta cuenta cuántos nodos hay en total
            query = "MATCH (n) RETURN count(n) AS total_nodos"
            
            # Usamos execute_query (disponible en versiones recientes del driver)
            # para simplificar la gestión de sesiones y transacciones.
            records, summary, keys = driver.execute_query(
                query, 
                database_="neo4j", 
                routing_=RoutingControl.READ
            )

            # 4. Mostrar resultados
            for record in records:
                print(f"Total de nodos en la base de datos: {record['total_nodos']}")

    except Exception as e:
        print(f"Error al conectar: {e}")

if __name__ == "__main__":
    conectar_y_consultar()