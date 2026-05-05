import os
from neo4j import GraphDatabase


def show_results():
    uri = "neo4j+ssc://334f8d57.databases.neo4j.io"
    username = "334f8d57"
    password = os.environ.get("NEO4J_PASSWORD")
    database = "334f8d57"

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session(database=database) as session:
            result = session.run("""
            MATCH (m:Memory {filename: 'h1470.png'})-[r:REFERENCES]->(e) 
            RETURN e.name as entity, labels(e) as type
            """)
            print("Knowledge Graph Entities extracted from h1470.png:")
            for record in result:
                print(f"- {record['entity']} ({record['type'][0]})")


if __name__ == "__main__":
    show_results()
