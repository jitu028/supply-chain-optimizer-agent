from langchain_core.tools import tool
from langchain_google_vertexai import ChatVertexAI


@tool
def gemini_planner_tool(query: str) -> str:
    """Generate a step-by-step plan to address a supply chain issue."""
    model = ChatVertexAI(model_name="gemini-2.5-pro")
    prompt = f"""Create a step-by-step plan to address the following supply chain query. 
The plan should include actions like data analysis, simulation, or Cypher queries.
Query: {query}
Plan:"""
    response = model.invoke(prompt)
    return response.content
