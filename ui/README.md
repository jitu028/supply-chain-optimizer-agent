# Supply Chain Optimizer UI

This is the Streamlit-based user interface for interacting with the AI-powered supply chain optimization agent.

## Features

- Clean and responsive web UI built using Streamlit.
- Accepts natural language queries to analyze supply chain scenarios.
- Displays AI-generated responses based on Neo4j graph data and Vertex AI agents.
- Easy integration with FastAPI backend.

## Structure

- `ui/`
  - `app.py`: The main entry point to launch the Streamlit app.
  - `requirements.txt`: Lists Python dependencies.

## Running Locally

Make sure the backend agent (FastAPI) is running at `http://localhost:8080`.

```bash
cd ui
pip install -r requirements.txt
streamlit run app.py
```

## Sample Questions to Ask the Agent

Try asking the agent any of the following queries in the UI:

1. **"Simulate the impact if Shanghai suppliers are delayed by 5 days."**
2. **"What are the top 3 most critical suppliers based on current relationships?"**
3. **"Suggest a backup plan if products from Germany are delayed."**
4. **"Analyze which products depend on a single source supplier."**
5. **"List suppliers who supply to more than one region."**

## Prerequisites

Ensure the backend API is running locally on `http://localhost:8080`, and that Neo4j AuraDB is connected and loaded with sample supply chain data.

## License

MIT License
