# ✈️ IROPS Recovery Copilot

> **Agentic Multi-Constraint Airline Disruption Recovery & Policy Intelligence System**

IROPS Recovery Copilot is an AI-powered airline operations system designed to assist with **Irregular Operations (IROPS)** such as flight cancellations, weather disruptions, passenger connection risks, and crew constraints.

The system combines:

- Agentic AI
- LangGraph
- OR-Tools optimization
- FastAPI
- SQLite
- Retrieval-Augmented Generation (RAG)
- ChromaDB
- BGE embeddings
- Groq LLM
- HTML/CSS/JavaScript
- Docker

The core recovery decisions are handled by deterministic optimization, while LLMs are used for operational briefings and policy-grounded question answering.

---

# 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [System Architecture](#-system-architecture)
- [Agentic Workflow](#-agentic-workflow)
- [Agents](#-agents)
- [OR-Tools Optimization](#-or-tools-optimization)
- [RAG Policy Intelligence](#-rag-policy-intelligence)
- [Policy Knowledge Base](#-policy-knowledge-base)
- [Dashboard](#-dashboard)
- [Data Layer](#-data-layer)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Generate Synthetic Data](#-generate-synthetic-data)
- [Validate Data](#-validate-data)
- [Database Setup](#-database-setup)
- [Build the RAG Vector Store](#-build-the-rag-vector-store)
- [Test RAG Retrieval](#-test-rag-retrieval)
- [Run the Backend](#-run-the-backend)
- [Run the Frontend](#-run-the-frontend)
- [API Endpoints](#-api-endpoints)
- [Example Recovery Scenario](#-example-recovery-scenario)
- [Docker](#-docker)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)
- [Key Technical Highlights](#-key-technical-highlights)
- [Author](#-author)

---

# 🚨 Problem Statement

Airline disruptions can cause cascading operational problems across:

- Flights
- Aircraft
- Passengers
- Connecting itineraries
- Crew
- Airport operations
- Weather
- Maintenance
- Passenger assistance

When a flight is cancelled, airline operations teams need to quickly determine:

1. Which passengers are affected?
2. Which passengers have onward connections?
3. Which alternative flights are available?
4. Which alternatives have sufficient capacity?
5. Which passengers can be rebooked?
6. Which passengers remain unresolved?
7. Which crew members are available and qualified?
8. What operational policies apply?
9. How should the disruption and recovery plan be communicated?

IROPS Recovery Copilot provides an automated decision-support workflow for these tasks.

---

# 🎯 Objectives

The main objectives of the project are:

- Detect flight disruptions
- Analyze disruption severity
- Identify affected passengers
- Identify connecting passengers
- Find alternative flights
- Check available capacity
- Optimize passenger rebooking
- Respect operational constraints
- Analyze crew availability
- Check crew qualification compatibility
- Generate operational briefings
- Retrieve relevant airline policies
- Provide policy-grounded answers using RAG
- Present recovery information through an operations dashboard

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │      Web Dashboard      │
                         │     HTML / CSS / JS     │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │        FastAPI          │
                         │        REST API         │
                         └────────────┬────────────┘
                                      │
                     ┌────────────────┴────────────────┐
                     │                                 │
                     ▼                                 ▼
             ┌──────────────────┐             ┌──────────────────┐
             │     LangGraph    │             │    RAG System    │
             │ Agentic Workflow │             │ Policy Assistant │
             └─────────┬────────┘             └─────────┬────────┘
                       │                                │
       ┌───────────────┼───────────────┐                │
       │               │               │                ▼
       ▼               ▼               ▼          ┌────────────┐
 Disruption        Passenger         Crew          │  ChromaDB  │
    Agent            Agent          Agent          └─────┬──────┘
       │               │               │                ▼
       └───────────────┼───────────────┘          BGE Embeddings
                       │                                │
                       ▼                                ▼
                ┌──────────────┐                 Policy Context
                │   Rebooking  │                       │
                │    Agent     │                       ▼
                └──────┬───────┘                  ┌────────────┐
                       │                           │  Groq LLM  │
                       ▼                           └─────┬──────┘
                ┌──────────────┐                         │
                │   OR-Tools   │                         ▼
                │   CP-SAT     │                  Policy Answer
                └──────┬───────┘
                       │
                       ▼
                Recovery Results
                       │
                       ▼
                ┌──────────────┐
                │   Briefing   │
                │     Agent    │
                └──────┬───────┘
                       │
                       ▼
                 Groq LLM Output
                       │
                       ▼
                 Web Dashboard
```

---

# 🤖 Agentic Workflow

The core recovery workflow is implemented using LangGraph.

```text
Disruption Agent
       ↓
Passenger Agent
       ↓
Rebooking Agent
       ↓
Crew Agent
       ↓
Briefing Agent
```

Each agent performs a specific operational task.

---

# 🧩 Agents

## 1. Disruption Agent

The Disruption Agent analyzes the disruption associated with the requested flight.

It determines:

- Flight ID
- Disruption type
- Severity
- Disruption status
- Description

Example:

```text
Flight: FL0001
Disruption Type: WEATHER
Severity: HIGH
Status: CANCELLED
```

---

## 2. Passenger Agent

The Passenger Agent determines the passenger impact of the disruption.

It identifies:

- Total affected passengers
- Passengers with onward connections
- Passenger information relevant to recovery

Example:

```text
Affected passengers: 30
Connecting passengers: 15
```

---

## 3. Rebooking Agent

The Rebooking Agent invokes the OR-Tools optimization engine.

It evaluates available alternatives and generates passenger-level recovery decisions.

The output contains:

- Passenger ID
- Passenger name
- Original flight
- New flight
- Recovery status
- Reason

Example:

```text
Passenger    Original    New Flight    Status
------------------------------------------------
P000001      FL0001      FL0002        REBOOKED
P000002      FL0001      FL0003        REBOOKED
P000003      FL0001      --            UNRESOLVED
```

---

## 4. Crew Agent

The Crew Agent evaluates crew availability for the disrupted operation.

It considers information such as:

- Aircraft type
- Crew availability
- Crew qualifications
- Current crew location
- Operational constraints

Example:

```text
Aircraft: B787
Available crew: 17
Matching crew: 2
```

Crew candidates are surfaced for operational review rather than automatically bypassing airline safety and scheduling procedures.

---

## 5. Briefing Agent

The Briefing Agent uses a Groq-hosted LLM to transform deterministic recovery information into a concise operational briefing.

The briefing agent is instructed to:

- Use recovery results as facts
- Avoid inventing flights
- Avoid inventing crew
- Avoid inventing aircraft information
- Distinguish facts from recommendations
- Treat OR-Tools results as the source of truth for rebooking

---

# 🧮 OR-Tools Optimization

Passenger recovery is implemented using **Google OR-Tools CP-SAT**.

The optimizer attempts to maximize useful passenger recovery while respecting operational constraints.

Conceptually:

```text
Maximize:

Rebooking Benefit
       -
Delay Cost
       -
Operational Cost
```

Subject to constraints such as:

```text
A passenger can receive at most one rebooking.

Recovered passengers cannot exceed available flight capacity.

Alternative flights must satisfy the implemented feasibility rules.

Connection requirements must be respected where applicable.
```

The optimization engine returns passenger-level decisions.

Possible statuses include:

```text
REBOOKED
NO_FEASIBLE_FLIGHT
```

The solver also returns its optimization status.

Example:

```text
Solver: OPTIMAL
Total passengers: 30
Rebooked: 28
Unresolved: 2
```

---

# 📚 RAG Policy Intelligence

The project contains a separate Retrieval-Augmented Generation system for airline policy and procedure questions.

The RAG pipeline is:

```text
Policy PDFs
     ↓
PDF Text Extraction
     ↓
Text Chunking
     ↓
BGE Embeddings
     ↓
ChromaDB
     ↓
Semantic Retrieval
     ↓
Relevant Policy Context
     ↓
Groq LLM
     ↓
Policy-Grounded Answer
```

RAG is intentionally separated from the core optimization engine.

The purpose of RAG is to provide:

- Policy lookup
- Procedure lookup
- Operational explanations
- Contextual policy answers

The LLM is instructed to answer using the retrieved policy context and avoid inventing policies.

---

# 📄 Policy Knowledge Base

The current knowledge base contains five synthetic policy documents:

```text
knowledge/
├── rebooking_policy.pdf
├── connection_policy.pdf
├── disruption_policy.pdf
├── crew_policy.pdf
└── compensation_policy.pdf
```

## Rebooking Policy

Contains information about:

- Rebooking priorities
- Alternative flights
- Capacity
- Passenger recovery

## Connection Policy

Contains information about:

- Connecting passengers
- Connection protection
- Minimum connection time
- Missed connections

## Disruption Policy

Contains information about:

- Flight disruptions
- Cancellations
- Weather events
- Escalation procedures

## Crew Policy

Contains information about:

- Crew qualification
- Crew availability
- Aircraft compatibility
- Duty constraints

## Compensation Policy

Contains information about:

- Passenger assistance
- Disruption-related assistance
- Compensation considerations

> **Note:** These documents are synthetic policies created for demonstration purposes. They are not official airline policies.

---

# 🔎 Embeddings

The project uses:

```text
BAAI/bge-base-en-v1.5
```

for semantic embeddings.

Each policy chunk is converted into an embedding vector and stored in ChromaDB.

The same embedding model is used to embed user questions during retrieval.

---

# 🗄️ ChromaDB

ChromaDB is used as the vector database.

The persistent vector store is:

```text
chroma_db/
```

The collection used by the application is:

```text
irops_policies
```

Stored information includes:

- Policy text
- Embeddings
- Source metadata

Example metadata:

```text
{
    "source": "connection_policy.pdf"
}
```

---

# 💬 Policy Assistant

The dashboard includes an interactive:

```text
IROPS Policy Assistant
```

Users can ask questions such as:

```text
What is the priority for passengers with onward connections?
```

The system:

1. Embeds the question
2. Searches ChromaDB
3. Retrieves relevant policy chunks
4. Builds a policy context
5. Sends the context to the Groq LLM
6. Returns a concise answer
7. Displays the source policy documents

Example retrieval result:

```text
Source: connection_policy.pdf

Passengers at risk of missing an onward connection
should be prioritized when feasible alternatives exist.
```

---

# 🖥️ Dashboard

The frontend uses:

- HTML5
- CSS3
- JavaScript

React is intentionally not required for the current implementation.

The dashboard provides an airline operations-center style interface.

## Dashboard Features

### Flight Analysis

Enter a flight ID:

```text
FL0001
```

and select:

```text
Analyze Recovery
```

---

## Disruption Overview

Displays:

- Flight ID
- Disruption type
- Severity
- Recovery status
- Operational description

---

## Passenger Impact

Displays:

- Affected passengers
- Connecting passengers

---

## Recovery Optimization

Displays:

- Solver status
- Total passengers
- Rebooked passengers
- Unresolved passengers

---

## Passenger Recovery

Displays individual recovery decisions.

Example:

```text
Passenger ID
Passenger Name
Original Flight
New Flight
Status
Reason
```

---

## Alternative Flights

Displays feasible alternatives considered by the recovery system.

Information includes:

- Flight ID
- Origin
- Destination
- Departure
- Arrival
- Available seats
- Capacity
- Status

---

## Crew Status

Displays:

- Aircraft
- Available crew
- Matching crew

---

## AI Operational Briefing

Displays a concise LLM-generated operational summary based on deterministic recovery results.

---

## RAG Policy Assistant

Allows users to ask questions about the synthetic airline policy knowledge base.

---

# 🗃️ Data Layer

The project uses synthetic airline operational data.

Current dataset includes:

```text
40 airports
120 aircraft
3000 flights
30000 passengers
6475 connections
600 crew members
742 crew qualifications
23 crew assignments
120 maintenance records
280 weather records
3000 flight rotations
150 disruptions
```

The data is stored primarily in CSV files and SQLite.

---

# 🗄️ Database

The project also contains:

```text
irops.db
```

SQLite is used for structured operational data access.

The database currently contains tables/entities for:

- Airports
- Aircraft
- Flights
- Passengers
- Connections
- Crew
- Crew Qualifications
- Crew Assignments
- Maintenance
- Disruptions
- Flight Rotations

The database layer allows operational tools and API components to query structured data without requiring every component to directly process CSV files.

---

# 📁 Project Structure

```text
IROPS/
│
├── data/
│   ├── airports.csv
│   ├── aircraft.csv
│   ├── flights.csv
│   ├── passengers.csv
│   ├── connections.csv
│   ├── crew.csv
│   ├── crew_qualifications.csv
│   ├── crew_assignments.csv
│   ├── maintenance.csv
│   ├── weather.csv
│   ├── flight_rotations.csv
│   ├── airport_capacity.csv
│   └── disruptions.csv
│
├── knowledge/
│   ├── rebooking_policy.pdf
│   ├── connection_policy.pdf
│   ├── disruption_policy.pdf
│   ├── crew_policy.pdf
│   └── compensation_policy.pdf
│
├── app/
│   │
│   ├── agents/
│   │   ├── disruption_agent.py
│   │   ├── passenger_agent.py
│   │   ├── rebooking_agent.py
│   │   ├── crew_agent.py
│   │   └── briefing_agent.py
│   │
│   ├── graph/
│   │   └── workflow.py
│   │
│   ├── tools/
│   │   ├── flight_tools.py
│   │   ├── passenger_tools.py
│   │   ├── crew_tools.py
│   │   └── aircraft_tools.py
│   │
│   ├── rules/
│   │
│   ├── optimization/
│   │   ├── constraints.py
│   │   ├── model.py
│   │   └── objective.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── seed.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── vectorstore.py
│   │   ├── retrieve.py
│   │   └── chat.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   └── main.py
│
├── scripts/
│   ├── generate_data.py
│   ├── validate_data.py
│   ├── recovery_engine_ortools.py
│   └── disruption_analyzer.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── chroma_db/
├── irops.db
├── requirements.txt
├── Dockerfile
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

## Agentic AI

- LangGraph
- LangChain
- Groq

## Optimization

- Google OR-Tools
- CP-SAT

## RAG

- Sentence Transformers
- BAAI/BGE
- ChromaDB
- PyMuPDF
- LangChain Text Splitters

## Frontend

- HTML5
- CSS3
- JavaScript

## Deployment

- Docker

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd IROPS
```

---

## 2. Create a Virtual Environment

Python 3.12 is recommended.

```bash
python3.12 -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key
```

The Groq API key is required for:

- Operational briefing generation
- RAG policy assistant

Do not commit `.env` to GitHub.

Use `.env.example` for documentation.

Example:

```env
GROQ_API_KEY=
```

---

# 🧪 Generate Synthetic Data

The project includes a synthetic airline data generator.

Run:

```bash
python scripts/generate_data.py
```

This generates the operational datasets under:

```text
data/
```

The generator creates:

- Airports
- Aircraft
- Flights
- Passengers
- Connections
- Crew
- Crew qualifications
- Crew assignments
- Maintenance records
- Weather records
- Flight rotations
- Disruptions

The dataset also contains a guaranteed demonstration disruption involving:

```text
FL0001
```

---

# ✅ Validate Data

Run:

```bash
python scripts/validate_data.py
```

The validation script checks the generated datasets for consistency and required relationships.

---

# 🗄️ Database Setup

Seed the SQLite database using the project's database seed process.

The database file is:

```text
irops.db
```

After successful seeding, the database contains operational records for:

```text
Airports
Aircraft
Flights
Passengers
Connections
Crew
Crew Qualifications
Crew Assignments
Maintenance
Disruptions
Flight Rotations
```

---

# 📚 Build the RAG Vector Store

The policy PDFs are stored in:

```text
knowledge/
```

First extract and chunk the PDFs:

```bash
python -m app.rag.ingest
```

Then build the ChromaDB vector store:

```bash
python -m app.rag.vectorstore
```

Expected output:

```text
Stored 10 chunks in ChromaDB
```

The exact number of chunks may change if the policy documents are modified.

---

# 🔎 Test RAG Retrieval

Run:

```bash
python -m app.rag.retrieve
```

Example question:

```text
What is the priority for passengers with onward connections?
```

The retriever should return relevant content from:

```text
connection_policy.pdf
```

along with other semantically related policies.

---

# 💬 Test the RAG Assistant

The RAG assistant can be tested through the API once the backend is running.

Example question:

```text
What is the priority for passengers with onward connections?
```

The assistant retrieves relevant policy context and generates an answer using the Groq LLM.

---

# 🚀 Run the Backend

Make sure the virtual environment is activated.

Run:

```bash
python -m uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 Run the Frontend

The frontend is located in:

```text
frontend/
```

Run a simple local HTTP server:

```bash
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

The frontend communicates with:

```text
http://127.0.0.1:8000
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

# 🔄 Recovery API

```http
POST /recover
```

Request:

```json
{
  "flight_id": "FL0001"
}
```

The endpoint runs the recovery workflow.

The response includes information such as:

```text
Flight information
Disruption information
Passenger impact
Connecting passengers
Solver status
Rebooked passengers
Unresolved passengers
Passenger-level recovery
Alternative flights
Crew information
Operational briefing
```

---

# 💬 Policy Chat API

```http
POST /chat
```

The current implementation accepts the question as a query parameter.

Example:

```text
/chat?question=What%20is%20the%20priority%20for%20connecting%20passengers?
```

Example response structure:

```json
{
  "question": "What is the priority for connecting passengers?",
  "answer": "Passengers at risk of missing an onward connection should be prioritized when feasible alternatives exist.",
  "sources": [
    {
      "source": "connection_policy.pdf"
    }
  ]
}
```

---

# ✈️ Example Recovery Scenario

The guaranteed demonstration scenario uses:

```text
Flight: FL0001
Route: NRT → SIN
Departure: 2026-10-01 10:00
Duration: 7 hours
```

The disruption scenario identifies:

```text
Disruption: WEATHER
Severity: HIGH
Status: CANCELLED
```

Passenger impact:

```text
Affected passengers: 30
Connecting passengers: 15
```

The recovery optimizer searches for feasible alternatives.

Current test result:

```text
Solver: OPTIMAL
Total passengers: 30
Rebooked: 28
Unresolved: 2
```

Crew analysis:

```text
Aircraft: B787
Available crew: 17
Matching crew: 2
```

The final workflow therefore produces:

```text
Flight: FL0001
Disruption: WEATHER
Affected: 30
Connecting: 15
Solver: OPTIMAL
Rebooked: 28
Unresolved: 2
Crew matches: 2
```

The dashboard then presents these results in an operations-center interface.

---

# 🐳 Docker

The project can be containerized using Docker.

## Dockerfile

The Docker image contains:

- Python runtime
- Application code
- Data
- Policy knowledge base
- ChromaDB
- SQLite database

Build the image:

```bash
docker build -t irops-recovery-copilot .
```

Run the container:

```bash
docker run \
  --name irops-backend \
  -p 8000:8000 \
  --env-file .env \
  irops-recovery-copilot
```

The backend will be available at:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 🧹 Recommended .gitignore

The following files/directories should generally not be committed:

```gitignore
.venv/
__pycache__/
*.pyc

.env

chroma_db/
*.db

.DS_Store

.pytest_cache/
```

If the project intentionally requires the generated database or vector store to be included for a demo, they can instead be distributed separately or generated during setup.

---

# ⚠️ Limitations

This project is a **demonstration and decision-support prototype**, not a production airline operations system.

Current limitations include:

- Synthetic airline data
- Synthetic policy documents
- No live airline scheduling data
- No live weather API
- No live airport operations data
- No live aircraft tracking
- No integration with airline reservation systems
- No real crew rostering system
- Limited network-wide optimization
- Simplified passenger recovery constraints
- Simplified crew constraints
- SQLite is used for the current prototype
- Policy documents are not official airline policies

The system should therefore not be used for real-world operational decisions without appropriate validation, airline-specific rules, safety procedures, and integration with authoritative operational systems.

---

# 🚀 Future Improvements

Potential future improvements include:

## Network-Wide Recovery

Extend optimization from a single disrupted flight to a complete airline network.

```text
Multiple disrupted flights
        ↓
Aircraft rotations
        ↓
Passenger itineraries
        ↓
Crew rotations
        ↓
Airport constraints
        ↓
Network-wide optimization
```

---

## Live Data Integration

Integrate:

- Airline operational APIs
- Flight status APIs
- Weather APIs
- Airport data
- Aircraft tracking
- Real-time passenger data

---

## Advanced Crew Recovery

Implement:

- Duty-time calculations
- Crew pairing
- Deadheading
- Rest requirements
- Positioning
- Crew reassignment optimization

---

## Improved Passenger Prioritization

Introduce configurable priorities based on:

- Connecting passengers
- Special assistance requirements
- Missed connections
- Loyalty status
- Fare class
- Time sensitivity

These rules would need to be defined according to the applicable airline's actual policies.

---

## Context-Aware RAG

The policy assistant can eventually combine policy context with the current recovery scenario.

For example:

```text
Current Flight:
FL0001

Disruption:
Weather cancellation

Affected:
30 passengers

Question:
How should connecting passengers be handled?
```

The assistant could then combine:

```text
Current operational state
+
Retrieved policy
```

while still keeping deterministic recovery decisions separate from the LLM.

---

## Human-in-the-Loop Approval

A future production-oriented workflow could introduce:

```text
AI Recovery Recommendation
          ↓
Operations Officer Review
          ↓
Approve / Modify / Reject
          ↓
Execute Recovery
```

This would keep operational authority with human decision-makers.

---

# 🔐 Why OR-Tools + LLM?

A key architectural decision is avoiding the use of an LLM as the optimization engine.

LLMs are useful for:

- Understanding natural language
- Summarizing information
- Explaining policies
- Generating operational briefings
- Conversational interaction

OR-Tools is useful for:

- Hard constraints
- Capacity constraints
- Feasibility
- Optimization
- Deterministic decisions

Therefore:

```text
                    IROPS SYSTEM

          ┌───────────────────────────┐
          │       OR-Tools            │
          │                           │
          │ Deterministic decisions   │
          │ Constraints               │
          │ Optimization              │
          └─────────────┬─────────────┘
                        │
                        ▼
                 Recovery Results
                        │
                        ▼
          ┌───────────────────────────┐
          │          LLM              │
          │                           │
          │ Explanation               │
          │ Briefing                  │
          │ Natural language          │
          └───────────────────────────┘
```

This separation makes the architecture easier to reason about and reduces the risk of allowing a generative model to directly invent operational decisions.

---

# 🧠 Why RAG?

Airline operations depend heavily on policies and procedures.

Instead of asking an LLM to rely entirely on its pretrained knowledge, this project provides a controlled knowledge base.

```text
User Question
      ↓
Embedding
      ↓
Semantic Search
      ↓
Relevant Policy Chunks
      ↓
LLM
      ↓
Grounded Answer
```

This provides a mechanism for the assistant to reference the project's policy documents when answering operational questions.

---

# 📊 Current End-to-End Test

The complete workflow has been tested successfully.

```text
                     FL0001
                       │
                       ▼
              Disruption Agent
                       │
                       ▼
            WEATHER / HIGH / CANCELLED
                       │
                       ▼
              Passenger Agent
                       │
                       ▼
             30 affected
             15 connecting
                       │
                       ▼
             Rebooking Agent
                       │
                       ▼
                OR-Tools
                       │
                       ▼
            OPTIMAL SOLUTION
                       │
                 ┌─────┴─────┐
                 ▼           ▼
             28 Rebooked   2 Unresolved
                       │
                       ▼
                 Crew Agent
                       │
                       ▼
              2 Matching Crew
                       │
                       ▼
               Briefing Agent
                       │
                       ▼
             Operational Briefing
                       │
                       ▼
                  Dashboard
```

The RAG pipeline is separately tested through:

```text
Policy PDFs
     ↓
BGE Embeddings
     ↓
ChromaDB
     ↓
Semantic Retrieval
     ↓
Groq LLM
     ↓
Policy Assistant
```

---

# 💡 Key Technical Highlights

This project demonstrates practical implementation of:

- Agentic AI workflows
- LangGraph
- LLM integration
- Retrieval-Augmented Generation
- Semantic search
- Vector databases
- Sentence Transformers
- BGE embeddings
- ChromaDB
- Constraint programming
- OR-Tools CP-SAT
- FastAPI
- SQLAlchemy
- SQLite
- Synthetic data generation
- Multi-agent orchestration
- AI-generated operational briefings
- Policy-grounded conversational AI
- REST API development
- Frontend-backend integration
- Docker containerization

---

# 📌 Project Status

Current implementation includes:

```text
✅ Synthetic airline dataset
✅ Data validation
✅ SQLite database
✅ Operational database tools
✅ Disruption Agent
✅ Passenger Agent
✅ Rebooking Agent
✅ OR-Tools optimization
✅ Crew Agent
✅ Briefing Agent
✅ LangGraph workflow
✅ FastAPI backend
✅ Recovery API
✅ Passenger-level recovery results
✅ Alternative flight display
✅ HTML/CSS/JavaScript dashboard
✅ Policy PDF knowledge base
✅ PDF extraction
✅ Text chunking
✅ BGE embeddings
✅ ChromaDB vector store
✅ Semantic policy retrieval
✅ Groq-powered RAG assistant
✅ Frontend RAG chat
✅ Docker support
```

---

# 👨‍💻 Author

**Madhav Manoj**

---

# 📄 Disclaimer

IROPS Recovery Copilot is an academic/portfolio project built using synthetic airline data and synthetic policy documents.

It is intended to demonstrate the engineering concepts involved in airline disruption recovery, optimization, agentic AI, and RAG.

It is **not an official airline operations system** and should not be used to make real-world airline operational, safety, crew, passenger, or compensation decisions.
