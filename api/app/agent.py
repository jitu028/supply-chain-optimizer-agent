from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

# ✅ Relative imports (make sure this file is inside the app/ package)
from app.tools.cypher import cypher_query_tool
from app.tools.planner import gemini_planner_tool
from app.tools.search import vector_search_tool
from app.tools.simulator import simulator_tool

from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_google_vertexai import ChatVertexAI
from vertexai.preview.language_models import ChatModel
import vertexai


class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]


class Agent:
    def __init__(self, model, tools):
        self.model = model
        self.tools = {t.name: t for t in tools}

    def call_model(self, state: AgentState):
        messages = state['messages']
        response = self.model.invoke(messages)
        return {"messages": [response]}

    def call_tool(self, state: AgentState):
        last_message = state['messages'][-1]
        tool_call = last_message.tool_calls[0]
        tool = self.tools[tool_call['name']]
        result = tool.invoke(tool_call['args'])
        return {"messages": [ToolMessage(content=str(result), tool_call_id=tool_call['id'])]}

    def router(self, state: AgentState):
        last_message = state['messages'][-1]
        if last_message.tool_calls:
            return "tool_node"
        return "end"


async def run_agent(query: str):
    # ✅ Explicitly initialize Vertex AI
    vertexai.init(project="your-gcp-project-id", location="us-central1")
    model = ChatVertexAI(model_name="gemini-2.5-pro")

    # ✅ Tool functions registered using @tool
    tools = [
        cypher_query_tool,
        gemini_planner_tool,
        vector_search_tool,
        simulator_tool,
    ]
    model_with_tools = model.bind_tools(tools)

    agent = Agent(model=model_with_tools, tools=tools)

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent.call_model)
    workflow.add_node("tool_node", agent.call_tool)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        agent.router,
        {"tool_node": "tool_node", "end": END}
    )
    workflow.add_edge('tool_node', 'agent')

    chain = workflow.compile()
    result = chain.invoke({
        "messages": [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=query)
        ]
    })
    return result['messages'][-1].content
