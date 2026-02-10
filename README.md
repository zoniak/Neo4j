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
