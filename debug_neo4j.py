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
    # Aura best practice: neo4j+s for encrypted routing
    uri = "neo4j+ssc://334f8d57.databases.neo4j.io"
    username = "334f8d57"
    password = os.environ.get("NEO4J_PASSWORD")

    if not password:
        print("[-] Error: NEO4J_PASSWORD not found.")
        return

    print(f"[+] Starting connection probe to {uri}...")
    try:
        # Using the latest recommended driver pattern
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            print("[+] Verifying connectivity (fetching routing table)...")
            driver.verify_connectivity()

            print("[+] Routing successful! Executing test query on 'neo4j' database...")
            # Explicitly naming the database as per docs
            summary = driver.execute_query(
                "RETURN 'GodBrain is Online' as message", database_="334f8d57"
            ).summary

            print(f"[+] Success! Connected to: {summary.metadata.get('server')}")

    except Exception as e:
        print("\n[-] CONNECTION FAILED:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")


if __name__ == "__main__":
    test_godbrain_connection()
