1. pip install neo4j
2. El lenguaje de consultas de Neo4j se llama Cypher.
3. Buscar nodos que juguen al futbol
   MATCH (a:Alumno)-[:PRACTICA]->(h:Hobby)
   WHERE h.nombre = 'Fútbol'
   RETURN a.nombre
4. Hobbies en comun
   MATCH (a1:Alumno {nombre: 'Ana'})-[:PRACTICA]->(h:Hobby)<-[:PRACTICA]-(a2:Alumno {nombre: 'David'})
   RETURN h.nombre

Para imprimir el grafo:

1. pip install networkx matplotlib

Para lanzar la bbdd en local con docker:

docker run \
 --name neo4j-local \
 -p 7474:7474 -p 7687:7687 \
 -d \
 -e NEO4J_AUTH=neo4j/tu_contraseña_secreta \
 neo4j:latest

Acceso al navegador: http://localhost:7474
Acceso desde código: bolt://localhost:7687
