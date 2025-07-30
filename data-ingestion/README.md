# Data Ingestion Module

This module handles the ingestion of supply chain data into a Neo4j graph database. It simulates realistic supply chain entities and relationships and prepares the graph for downstream reasoning, querying, and simulation.

---

## 🔧 Prerequisites

Before running this module, you need to set up a **Neo4j AuraDB Free instance**:

### 🌐 Steps to Create a Free Neo4j AuraDB Instance

1. Go to [https://neo4j.com/cloud/aura/](https://neo4j.com/cloud/aura/)
2. Sign up or log in using your Google, GitHub, or email credentials.
3. Click on **"Create Database"**.
4. Select **"AuraDB Free"**.
5. Name your database (e.g., `supply-chain-db`).
6. Once the database is created:
   - Copy the **Bolt connection URI** (e.g., `neo4j+s://...`)
   - Copy the **Username** and **Password**

7. Update your local `.env` file with these credentials:

   ```
   NEO4J_URI=neo4j+s://<your-bolt-uri>
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=<your-password>
   ```

---

## 🚀 Features

- Ingests sample supply chain data:
  - `Suppliers`, `Products`, `Locations`
  - Relationships like `SUPPLIES`, `LOCATED_IN`
- Cleans existing data before fresh ingestion
- Supports manual execution or cloud deployment as a job

---

## 📁 Folder Structure

```
data-ingestion/
├── ingest.py           # Main ingestion logic
├── requirements.txt    # Python dependencies
├── .env                # Environment file with Neo4j credentials
```

---

## ☁️ Deploying to Google Cloud Run (as a Job)

To deploy this ingestion module as an on-demand Cloud Run Job:

```bash
gcloud run jobs create data-ingestion-job \
  --image=gcr.io/YOUR_PROJECT_ID/YOUR_IMAGE \
  --region=us-central1 \
  --command="python" \
  --args="ingest.py" \
  --project=YOUR_PROJECT_ID
```

Trigger the job manually:

```bash
gcloud run jobs execute data-ingestion-job --region=us-central1
```

---

## 🧪 Running Locally

Ensure Python and the required dependencies are installed.

```bash
pip install -r requirements.txt
python ingest.py
```

Ensure the `.env` file includes:

```env
NEO4J_URI=neo4j+s://<host>:<port>
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

---

## 🛡 License

MIT License
