import os
import random
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.__driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        if self.__driver:
            self.__driver.close()

    def query(self, q, params=None, db=None):
        with (self.__driver.session(database=db) if db else self.__driver.session()) as s:
            return list(s.run(q, params or {}))

def generate_data():
    random.seed(42)

    suppliers = [f"Supplier {i}" for i in range(1, 101)]
    products  = [f"Product {i}"  for i in range(1, 51)]
    warehouses = [f"Warehouse {i}" for i in range(1, 21)]

    # City → Country → Region (kept small but diverse; includes Shanghai + Germany)
    city_map = {
        # China (APAC)
        "Shanghai":        ("China", "APAC"),
        "Shenzhen":        ("China", "APAC"),
        "Guangzhou":       ("China", "APAC"),
        "Beijing":         ("China", "APAC"),
        # India (APAC)
        "Pune":            ("India", "APAC"),
        "Mumbai":          ("India", "APAC"),
        "Bengaluru":       ("India", "APAC"),
        "Delhi":           ("India", "APAC"),
        "Chennai":         ("India", "APAC"),
        "Hyderabad":       ("India", "APAC"),
        # Japan/Korea (APAC)
        "Tokyo":           ("Japan", "APAC"),
        "Osaka":           ("Japan", "APAC"),
        "Seoul":           ("South Korea", "APAC"),
        # SE Asia (APAC)
        "Singapore":       ("Singapore", "APAC"),
        "Bangkok":         ("Thailand", "APAC"),
        "Kuala Lumpur":    ("Malaysia", "APAC"),
        "Jakarta":         ("Indonesia", "APAC"),
        "Manila":          ("Philippines", "APAC"),
        "Ho Chi Minh City":("Vietnam", "APAC"),
        "Taipei":          ("Taiwan", "APAC"),
        # Germany (Europe)
        "Berlin":          ("Germany", "Europe"),
        "Munich":          ("Germany", "Europe"),
        "Hamburg":         ("Germany", "Europe"),
        # Middle East (MEA)
        "Dubai":           ("UAE", "MEA"),
        "Abu Dhabi":       ("UAE", "MEA"),
        "Doha":            ("Qatar", "MEA"),
        "Riyadh":          ("Saudi Arabia", "MEA"),
        # Others
        "Hong Kong":       ("Hong Kong", "APAC"),
        "Hanoi":           ("Vietnam", "APAC"),
        "Kyoto":           ("Japan", "APAC"),
        "Nagoya":          ("Japan", "APAC"),
        "Karachi":         ("Pakistan", "APAC"),
        "Dhaka":           ("Bangladesh", "APAC"),
    }

    return {
        "suppliers": suppliers,
        "products": products,
        "warehouses": warehouses,
        "city_map": city_map,
    }

def setup_constraints(conn: Neo4jConnection):
    stmts = [
        "CREATE CONSTRAINT supplier_name_unique IF NOT EXISTS FOR (s:Supplier) REQUIRE s.name IS UNIQUE",
        "CREATE CONSTRAINT product_name_unique  IF NOT EXISTS FOR (p:Product)  REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT warehouse_name_unique IF NOT EXISTS FOR (w:Warehouse) REQUIRE w.name IS UNIQUE",
        "CREATE CONSTRAINT city_name_unique     IF NOT EXISTS FOR (c:City)     REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT country_name_unique  IF NOT EXISTS FOR (c:Country)  REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT region_name_unique   IF NOT EXISTS FOR (r:Region)   REQUIRE r.name IS UNIQUE",
        "CREATE INDEX supplier_id_idx           IF NOT EXISTS FOR (s:Supplier) ON (s.supplierID)",
        "CREATE INDEX supplier_id_norm_idx      IF NOT EXISTS FOR (s:Supplier) ON (s.supplier_id)",
    ]
    for s in stmts:
        conn.query(s)

def ingest_data(conn, data):
    print("Deleting all previous data...")
    conn.query("MATCH (n) DETACH DELETE n")

    print("Creating constraints/indexes...")
    setup_constraints(conn)

    print("Ingesting nodes...")
    # Regions & Countries (dedup as we go)
    regions = set(v[1] for v in data["city_map"].values())
    for r in regions:
        conn.query("MERGE (:Region {name: $name})", {"name": r})

    countries = set(v[0] for v in data["city_map"].values())
    for c in countries:
        conn.query("MERGE (:Country {name: $name})", {"name": c})

    # Cities with dual label :Location:City and hierarchy
    for city, (country, region) in data["city_map"].items():
        conn.query("""
            MERGE (c:Location:City {name: $city})
            SET   c.country = $country, c.region = $region
            WITH c
            MATCH (co:Country {name: $country})
            MERGE (c)-[:IN_COUNTRY]->(co)
            WITH c, co
            MATCH (r:Region {name: $region})
            MERGE (co)-[:IN_REGION]->(r)
        """, {"city": city, "country": country, "region": region})

    # Suppliers (with supplierID & failure_rate)
    for i, supplier_name in enumerate(data["suppliers"], start=1):
        supplier_id = f"S{i:04d}"
        conn.query("""
            MERGE (s:Supplier {name: $name})
            SET s.supplierID = $supplierID,
                s.supplier_id = $supplierID,
                s.failure_rate = $failure_rate
        """, {"name": supplier_name, "supplierID": supplier_id, "failure_rate": random.uniform(0, 0.1)})

    # Products
    for product_name in data["products"]:
        conn.query("MERGE (:Product {name: $name})", {"name": product_name})

    # Warehouses
    for w in data["warehouses"]:
        conn.query("MERGE (:Warehouse {name: $name})", {"name": w})

    print("Creating relationships...")
    # Supplier SUPPLIES Product
    for s in data["suppliers"]:
        for _ in range(random.randint(1, 5)):
            p = random.choice(data["products"])
            conn.query("""
                MATCH (sup:Supplier {name: $s})
                MATCH (prod:Product {name: $p})
                MERGE (sup)-[:SUPPLIES]->(prod)
            """, {"s": s, "p": p})

    # Supplier LOCATED_IN City (random)
    cities = list(data["city_map"].keys())
    for s in data["suppliers"]:
        city = random.choice(cities)
        conn.query("""
            MATCH (sup:Supplier {name: $s})
            MATCH (c:City {name: $city})
            MERGE (sup)-[:LOCATED_IN]->(c)
        """, {"s": s, "city": city})

    # Warehouse LOCATED_IN City (random)
    for w in data["warehouses"]:
        city = random.choice(cities)
        conn.query("""
            MATCH (wh:Warehouse {name: $w})
            MATCH (c:City {name: $city})
            MERGE (wh)-[:LOCATED_IN]->(c)
        """, {"w": w, "city": city})

    # Supplier SUPPLIES_TO Warehouse (to trace served regions via shipments)
    for s in data["suppliers"]:
        wh_targets = random.sample(data["warehouses"], k=random.randint(1, 3))
        for w in wh_targets:
            conn.query("""
                MATCH (sup:Supplier {name: $s})
                MATCH (wh:Warehouse {name: $w})
                MERGE (sup)-[:SUPPLIES_TO]->(wh)
            """, {"s": s, "w": w})

    # Warehouse SHIPS_TO City (existing)
    for w in data["warehouses"]:
        for _ in range(random.randint(5, 15)):
            city = random.choice(cities)
            conn.query("""
                MATCH (wh:Warehouse {name: $w})
                MATCH (c:City {name: $city})
                MERGE (wh)-[:SHIPS_TO]->(c)
            """, {"w": w, "city": city})

    # Product PRODUCED_IN City
    for p in data["products"]:
        city = random.choice(cities)
        conn.query("""
            MATCH (prod:Product {name: $p})
            MATCH (c:City {name: $city})
            MERGE (prod)-[:PRODUCED_IN]->(c)
        """, {"p": p, "city": city})

    # City CONNECTED_TO City (sparse network)
    for c1 in cities:
        for c2 in cities:
            if c1 != c2 and random.random() < 0.1:
                conn.query("""
                    MATCH (a:City {name: $c1})
                    MATCH (b:City {name: $c2})
                    MERGE (a)-[:CONNECTED_TO]->(b)
                """, {"c1": c1, "c2": c2})

    # Incidents
    for i in range(10):
        conn.query("CREATE (:Incident {description: $d})",
                   {"d": f"Incident {i}: Port closure due to storm"})

    print("Data ingestion complete.")

if __name__ == "__main__":
    conn = Neo4jConnection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    data = generate_data()
    ingest_data(conn, data)
    conn.close()
