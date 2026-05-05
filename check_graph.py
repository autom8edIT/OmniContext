import os
from neo4j import GraphDatabase


def check_memory():
    uri = "neo4j+ssc://334f8d57.databases.neo4j.io"
    username = "334f8d57"
    password = os.environ.get("NEO4J_PASSWORD")
    database = "334f8d57"

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session(database=database) as session:
            result = session.run(
                "MATCH (m:Memory {filename: 'h1470.png'}) RETURN m.text as text"
            )
            record = result.single()
            if record:
                print(f"Text from h1470.png:\n{record['text']}")
            else:
                print("No record found for h1470.png")


if __name__ == "__main__":
    check_memory()
