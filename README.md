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
   git clone https://github.com/jitu028/supply-chain-optimizer-agent.git
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

### 3.1 `api` - Agent Backend

```bash
gcloud run deploy supply-chain-api \
  --source ./api \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --project YOUR_PROJECT_ID
```

Test the endpoint:

```bash
curl -X POST https://supply-chain-api-<hash>-<region>.a.run.app/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "Simulate the impact if Shanghai suppliers are delayed by 5 days."}'
```

---

### 3.2 `data-ingestion` - Neo4j Seeder (Cloud Run Job)

```bash
# Step 1: Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/data-ingestion ./data-ingestion

# Step 2: Create Cloud Run Job
gcloud run jobs create data-ingestion-job \
  --image=gcr.io/YOUR_PROJECT_ID/data-ingestion \
  --region=us-central1 \
  --project=YOUR_PROJECT_ID

# Step 3: Run the Job
gcloud run jobs execute data-ingestion-job \
  --region=us-central1 \
  --project=YOUR_PROJECT_ID
```

---

### 3.3 `ui` - Streamlit Frontend

Ensure `PORT=8080` is set in `.streamlit/config.toml` or via `os.environ`.

```bash
gcloud run deploy supply-chain-ui \
  --source ./ui \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --project=YOUR_PROJECT_ID
```

