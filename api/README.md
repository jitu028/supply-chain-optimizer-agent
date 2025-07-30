# 🧠 API – Supply Chain Optimizer Agent

This folder contains the **FastAPI**-based backend service for the Supply Chain Optimizer Agent. It exposes a REST endpoint to interact with AI agents powered by **Google Vertex AI**, **Neo4j**, and **LangChain**.

---

## 🚀 Overview

The API provides a `/invoke` endpoint that accepts a natural language supply chain query and returns a structured response using AI-driven reasoning.

Supported tools:
- **Gemini Planner Tool** – Creates action plans from queries.
- **Cypher Query Tool** – Interacts with Neo4j to fetch data.
- **Simulator Tool** – Simulates risk events (e.g., location delays).
- **Vector Search Tool** – Retrieves similar past incidents.

---

## 🛠️ Setup

### 1. Install dependencies

```bash
cd api
pip install -r requirements.txt
```

### 2. Environment variables

Create a `.env` file in the `api/` directory with the following:

```env
NEO4J_URI=bolt+s://<your-neo4j-uri>
NEO4J_USERNAME=<username>
NEO4J_PASSWORD=<password>
```

You must also have Google Cloud credentials set up locally for Vertex AI:
```bash
gcloud auth application-default login
gcloud config set project <your-gcp-project-id>
```

---

## 🧪 Run Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Test the API using:

```bash
curl -X POST http://localhost:8080/invoke \
     -H "Content-Type: application/json" \
     -d '{"query": "Simulate the impact if Shanghai suppliers are delayed by 5 days."}'
```

---

## 📁 Folder Structure

```
api/
│
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── agent.py             # LangGraph agent logic
│   └── tools/
│       ├── cypher_tool.py   # Neo4j integration
│       ├── planner_tool.py  # Gemini planner tool
│       ├── simulator_tool.py# Impact simulation logic
│       └── vector_search_tool.py # Similarity search
│
└── requirements.txt         # Python dependencies
```

---

## 🧩 Integration

This API can be integrated with the streamlit `ui/` frontend or scheduled using a Cloud Run Job to perform batch risk simulations.

---

## 📜 License

[MIT](../LICENSE)