from langchain_core.tools import tool
from app.tools.cypher import cypher_query_tool


@tool
def vector_search_tool(query: str) -> str:
    """Search for similar past incidents using vector logic (placeholder)."""
    # In a real case, this would use embedding-based similarity
    return cypher_query_tool.invoke("MATCH (i:Incident) RETURN i.description AS Incident")
