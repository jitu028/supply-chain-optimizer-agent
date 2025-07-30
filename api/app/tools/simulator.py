from langchain_core.tools import tool
from app.tools.cypher import cypher_query_tool


@tool
def simulator_tool(event: str) -> str:
    """Simulate the impact of a risk event on the supply chain."""
    query = f"""
    MATCH (l:Location {{name: '{event}'}})<-[:LOCATED_IN]-(s:Supplier)-[:SUPPLIES]->(p:Product)
    RETURN s.name AS Supplier, p.name AS Product
    """
    return cypher_query_tool.invoke(query)
