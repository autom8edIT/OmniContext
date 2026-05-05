import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


def test_connection():
    # GodBrain Standard: neo4j+ssc for local stability, DB ID for target
    uri = "neo4j+ssc://334f8d57.databases.neo4j.io"
    username = "334f8d57"
    password = os.environ.get("NEO4J_PASSWORD")

    if not password:
        print("[-] Error: NEO4J_PASSWORD not found in environment.")
        return

    print(f"[+] Attempting to connect to {uri}...")
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session(database="334f8d57") as session:
            result = session.run("RETURN 'GodBrain is Online' as message")
            message = result.single()["message"]
            print(f"[+] Success: {message}")
        driver.close()
    except Exception as e:
        print(f"[-] Connection failed: {e}")


if __name__ == "__main__":
    test_connection()
