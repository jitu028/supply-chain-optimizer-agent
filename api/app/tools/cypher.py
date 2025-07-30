import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def cypher_query_tool(query: str) -> str:
    """
    Run a Cypher query on the Neo4j supply chain graph.
    The tool connects to the database, executes the query, and returns the result as a string.
    """
    driver = None
    try:
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run(query)
            response = str([r.data() for r in result])
    except Exception as e:
        response = f"Error executing Cypher query: {e}"
    finally:
        if driver:
            driver.close()
    return response