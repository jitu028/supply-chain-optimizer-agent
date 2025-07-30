from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.agent import run_agent

app = FastAPI(
    title="Supply Chain Optimizer Agent",
    description="An AI agent built with Gemini + Neo4j for supply chain analysis and simulation.",
    version="0.1.0",
)

# Enable CORS for frontend integration (e.g., Streamlit or web client)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origin(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentInput(BaseModel):
    query: str

@app.post("/invoke")
async def invoke_agent(input_data: AgentInput):
    """Invokes the supply chain optimizer agent with the user's query."""
    try:
        result = await run_agent(input_data.query)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
