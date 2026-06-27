from neo4j import GraphDatabase
import os

uri = os.environ.get("NEO4J_URI", "neo4j+ssc://9b4e7bcb.databases.neo4j.io")
username = os.environ.get("NEO4J_USERNAME", "9b4e7bcb")
password = os.environ.get("NEO4J_PASSWORD")

if not password:
    print("Error: NEO4J_PASSWORD environment variable not set.")
    exit(1)

driver = GraphDatabase.driver(uri, auth=(username, password))

def query_titan():
    with driver.session() as session:
        result = session.run("MATCH (n:Model) RETURN n.id as id, n.name as name, n.downloads as downloads, n.best_use_case as use_case")
        print("Model Nodes in Knowledge Graph:")
        for record in result:
            print(f"ID: {record[
'
id
'
]}, Name: {record[
'
name
'
]}, Downloads: {record[
'
downloads
'
]}, Use Case: {record[
'
use_case
'
]}")

if __name__ == "__main__":
    try:
        query_titan()
    finally:
        driver.close()
