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
    # But using +ssc for local SSL verification issues
    uri = "neo4j+ssc://9b4e7bcb.databases.neo4j.io"
    username = "9b4e7bcb"
    password = os.environ.get("NEO4J_PASSWORD")

    if not password:
        print("[-] Error: NEO4J_PASSWORD not found.")
        return

    print(f"[+] Starting connection probe to {uri}...")
    try:
        # Using the latest recommended driver pattern
        with GraphDatabase.driver(uri, auth=(username, password)) as driver:
            print("[+] Verifying connectivity...")
            driver.verify_connectivity()

            print("[+] Routing successful! Executing test query on '9b4e7bcb' database...")
            # Explicitly naming the database as per docs
            summary = driver.execute_query(
                "RETURN 'GodBrain is Online' as message", database_="9b4e7bcb"
            ).summary

            print(f"[+] Success! Connected to: {summary.metadata.get('server')}")

    except Exception as e:
        print("\n[-] CONNECTION FAILED:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")


if __name__ == "__main__":
    test_godbrain_connection()
