import os
import logging
import sys
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Enable heavy logging to see exactly where the handshake/routing fails
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger = logging.getLogger("neo4j")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

load_dotenv()


def test_godbrain_connection():
    uri = os.environ.get("NEO4J_URI")
    username = os.environ.get("NEO4J_USERNAME")
    password = os.environ.get("NEO4J_PASSWORD")
    database = os.environ.get("NEO4J_DB", "neo4j")

    if not uri:
        print("[-] Error: NEO4J_URI not found.")
        return
    if not username:
        print("[-] Error: NEO4J_USERNAME not found.")
        return
    if not password:
        print("[-] Error: NEO4J_PASSWORD not found.")
        return

    print(f"[+] Starting connection probe to {uri}...")
    try:
        # Using the latest recommended driver pattern
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            print("[+] Verifying connectivity...")
            driver.verify_connectivity()

            print(f"[+] Routing successful! Executing test query on '{database}' database...")
            # Explicitly naming the database as per docs
            summary = driver.execute_query(
                "RETURN 'GodBrain is Online' as message", database_=database
            ).summary

            print(f"[+] Success! Connected to: {summary.metadata.get('server')}")

    except Exception as e:
        print("\n[-] CONNECTION FAILED:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")


if __name__ == "__main__":
    test_godbrain_connection()
