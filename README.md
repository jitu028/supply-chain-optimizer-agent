# Supply Chain Optimizer Agent

This project implements an AI-powered agent to optimize and analyze supply chain data using a Neo4j graph database, Google Cloud, and the Agent Development Kit (ADK).

## Features

- **Intent-Driven Agent:** Understands natural language queries about the supply chain.
- **Neo4j Knowledge Graph:** Models suppliers, products, locations, and their relationships.
- **AI-Powered Tools:**
    - `CypherQueryTool`: Runs queries against the Neo4j database.
    - `VectorSearchTool`: Finds similar past incidents.
    - `GeminiPlannerTool`: Suggests alternative sourcing routes.
    - `SimulatorTool`: Simulates disruptions like port closures.
- **Cloud Native:** Designed for deployment on Google Cloud Run.
- **Optional UI:** Includes a Streamlit app for visualization.

## Project Structure

```
supply-optimizer-agent/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI application
│   ├── agent.py        # Agent logic (LangGraph/ADK)
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── cypher.py
│   │   ├── search.py
│   │   ├── planner.py
│   │   └── simulator.py
│   └── models/
│       ├── __init__.py
│       └── schema.py       # Pydantic models for data
├── data/
│   └── ingest.py       # Script to generate and ingest demo data
├── ui/
│   └── app.py          # Streamlit UI
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Docker
- Google Cloud SDK
- Access to a Neo4j instance (local or Aura)
- Google Cloud Project with Vertex AI API enabled

### 2. Local Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd supply-optimizer-agent
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env`: `cp .env.example .env`
   - Fill in the values in your `.env` file.

5. **Ingest demo data into Neo4j:**
   ```bash
   python data/ingest.py
   ```

6. **Run the agent locally:**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Run the UI (optional):**
   ```bash
   streamlit run ui/app.py
   ```

### 3. Cloud Deployment (Google Cloud Run)

1. **Build the Docker image:**
   ```bash
   docker build -t supply-optimizer-agent .
   ```

2. **Tag and push the image to Google Container Registry (GCR):**
   ```bash
   docker tag supply-optimizer-agent gcr.io/your-gcp-project-id/supply-optimizer-agent
   docker push gcr.io/your-gcp-project-id/supply-optimizer-agent
   ```

3. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy supply-optimizer-agent \
       --image gcr.io/your-gcp-project-id/supply-optimizer-agent \
       --platform managed \
       --region your-gcp-region \
       --allow-unauthenticated \
       --set-env-vars-from-file .env
   ```

```