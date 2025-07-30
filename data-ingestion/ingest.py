import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from neo4j import GraphDatabase
import time

load_dotenv(override=True)

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.__uri = uri
        self.__user = user
        self.__password = password
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__password))
        except Exception as e:
            print(f"Failed to create the driver: {e}")

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print(f"Query failed: {e}")
        finally:
            if session is not None:
                session.close()
        return response

def generate_data():
    """Generates demo data for the supply chain knowledge graph."""
    suppliers = [f"Supplier {i}" for i in range(1, 101)]
    products = [f"Product {i}" for i in range(1, 51)]
    locations = [f"Location {i}" for i in range(1, 31)]
    warehouses = [f"Warehouse {i}" for i in range(1, 21)]

    return {
        "suppliers": suppliers,
        "products": products,
        "locations": locations,
        "warehouses": warehouses
    }

def ingest_data(conn, data):
    """Ingests the generated data into Neo4j."""
    print("Deleting all previous data...")
    conn.query("MATCH (n) DETACH DELETE n")

    print("Ingesting new data...")
    # Ingest Suppliers
    for supplier_name in data["suppliers"]:
        conn.query("CREATE (:Supplier {name: $name, failure_rate: $failure_rate})", 
                   parameters={"name": supplier_name, "failure_rate": random.uniform(0, 0.1)})

    # Ingest Products
    for product_name in data["products"]:
        conn.query("CREATE (:Product {name: $name})", parameters={"name": product_name})

    # Ingest Locations
    for location_name in data["locations"]:
        conn.query("CREATE (:Location {name: $name})", parameters={"name": location_name})

    # Ingest Warehouses
    for warehouse_name in data["warehouses"]:
        conn.query("CREATE (:Warehouse {name: $name})", parameters={"name": warehouse_name})

    # Create relationships
    for supplier in data["suppliers"]:
        for _ in range(random.randint(1, 5)):
            product = random.choice(data["products"])
            conn.query("""
                MATCH (s:Supplier {name: $supplier_name})
                MATCH (p:Product {name: $product_name})
                MERGE (s)-[:SUPPLIES]->(p)
            """, parameters={"supplier_name": supplier, "product_name": product})

    for supplier in data["suppliers"]:
        location = random.choice(data["locations"])
        conn.query("""
            MATCH (s:Supplier {name: $supplier_name})
            MATCH (l:Location {name: $location_name})
            MERGE (s)-[:LOCATED_IN]->(l)
        """, parameters={"supplier_name": supplier, "location_name": location})

    for warehouse in data["warehouses"]:
        location = random.choice(data["locations"])
        conn.query("""
            MATCH (w:Warehouse {name: $warehouse_name})
            MATCH (l:Location {name: $location_name})
            MERGE (w)-[:LOCATED_IN]->(l)
        """, parameters={"warehouse_name": warehouse, "location_name": location})

    for warehouse in data["warehouses"]:
        for _ in range(random.randint(5, 15)):
            location = random.choice(data["locations"])
            conn.query("""
                MATCH (w:Warehouse {name: $warehouse_name})
                MATCH (l:Location {name: $location_name})
                MERGE (w)-[:SHIPS_TO]->(l)
            """, parameters={"warehouse_name": warehouse, "location_name": location})

    for product in data["products"]:
        location = random.choice(data["locations"])
        conn.query("""
            MATCH (p:Product {name: $product_name})
            MATCH (l:Location {name: $location_name})
            MERGE (p)-[:PRODUCED_IN]->(l)
        """, parameters={"product_name": product, "location_name": location})

    for loc1 in data["locations"]:
        for loc2 in data["locations"]:
            if loc1 != loc2 and random.random() < 0.1: # 10% chance of connection
                conn.query("""
                    MATCH (l1:Location {name: $loc1_name})
                    MATCH (l2:Location {name: $loc2_name})
                    MERGE (l1)-[:CONNECTED_TO]->(l2)
                """, parameters={"loc1_name": loc1, "loc2_name": loc2})
        # Ingest Incidents
    for i in range(10):
        conn.query("CREATE (:Incident {description: $description})", 
                   parameters={"description": f"Incident {i}: Port closure due to storm"})

    print("Data ingestion complete.")


import time

if __name__ == "__main__":
    conn = Neo4jConnection(uri=NEO4J_URI, user=NEO4J_USERNAME, password=NEO4J_PASSWORD)
    data = generate_data()
    ingest_data(conn, data)
    conn.close()
