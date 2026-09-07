# ✈️ Multi-Agent AI Travel Planner

An AI-powered **multi-agent travel planning application** built with **Python, LangGraph, LangChain, MCP, Groq, Streamlit, and PostgreSQL**. The application uses specialized AI agents to assist with flights, hotels, weather, budgeting, and itinerary planning.

## 🚀 Features

* 🤖 **Multi-Agent Architecture** using LangGraph
* ✈️ Flight and airport information using MCP
* 🏨 Hotel recommendations and travel search
* 🌤️ Real-time weather and forecast information
* 💰 Budget estimation and travel planning
* 🗺️ AI-generated travel itineraries
* 👤 Human approval step in the workflow
* 🧠 Groq LLM integration
* 🔌 Model Context Protocol (MCP) integration
* 💾 PostgreSQL/Neon checkpointing for workflow state
* 🎨 Interactive Streamlit interface
* ☁️ Deployment on Streamlit Community Cloud

## 🏗️ Architecture

The application follows a **multi-agent workflow**:

```text
                    ┌───────────────┐
                    │     User      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Supervisor  │
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
   ┌────────────┐    ┌────────────┐    ┌────────────┐
   │   Flight   │    │   Hotel    │    │  Weather   │
   │   Agent    │    │   Agent    │    │   Agent    │
   └──────┬─────┘    └──────┬─────┘    └──────┬─────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                    ┌───────────────┐
                    │ Budget Agent  │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │ Itinerary     │
                    │    Agent      │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │ Human Approval│
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │Final Response │
                    └───────────────┘
```

## 🛠️ Tech Stack

### Languages & Tools

* Python
* SQL
* Git & GitHub

### AI / ML

* Generative AI
* Agentic AI
* LangChain
* LangGraph
* MCP (Model Context Protocol)
* Groq LLM

### Libraries & Frameworks

* Streamlit
* Pandas
* NumPy
* Requests
* FastAPI

### Database & Cloud

* PostgreSQL
* Neon PostgreSQL
* Streamlit Community Cloud

## 📁 Project Structure

```text
multi-agent-travel-planner/
│
├── frontend.py          # Streamlit application
├── graph.py             # LangGraph workflow
├── agent.py             # AI agents
├── mcpClient.py         # MCP client integrations
├── custom_mcp.py        # Custom weather MCP server
├── config.py            # Configuration and environment variables
├── state.py             # Travel workflow state
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

## 🔌 MCP Integrations

The project uses **Model Context Protocol (MCP)** to connect AI agents with external tools.

### Tavily MCP

Used for travel and hotel-related web search.

### AviationStack MCP

Used for flight, airport, and airline information.

### Custom Weather MCP

A custom MCP server provides:

* Current weather
* Temperature
* Humidity
* Weather conditions
* Wind speed
* Forecast information

## 💾 PostgreSQL Checkpointing

The LangGraph workflow uses **PostgreSQL checkpointing** to persist workflow state.

The project can use **Neon PostgreSQL** as the cloud database for deployment.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/psrana344/multi-agent-travel-planner.git
cd multi-agent-travel-planner
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model

TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
OPENWEATHER_API_KEY=your_openweather_api_key

DATABASE_URL=your_postgresql_database_url
```

> Never commit your `.env` file or API keys to GitHub.

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run frontend.py
```

The application will open in your browser.

## ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud**.

Basic deployment steps:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Select the GitHub repository.
4. Set the main file as:

   ```text
   frontend.py
   ```
5. Add the required API keys and database URL to Streamlit Secrets.
6. Deploy the application.

## 🔐 Environment Variables

| Variable                | Purpose                    |
| ----------------------- | -------------------------- |
| `GROQ_API_KEY`          | Groq LLM authentication    |
| `GROQ_MODEL`            | Groq model configuration   |
| `TAVILY_API_KEY`        | Tavily search              |
| `AVIATIONSTACK_API_KEY` | AviationStack API          |
| `OPENWEATHER_API_KEY`   | OpenWeather API            |
| `DATABASE_URL`          | PostgreSQL/Neon connection |

## 🎯 Workflow

The application processes a travel request through multiple specialized agents:

1. **Supervisor Agent** – coordinates the workflow.
2. **Flight Agent** – handles flight-related information.
3. **Hotel Agent** – searches for hotel and accommodation recommendations.
4. **Weather Agent** – retrieves weather information.
5. **Budget Agent** – estimates the travel budget.
6. **Itinerary Agent** – generates the travel itinerary.
7. **Human Approval** – allows human review before finalization.
8. **Final Response Agent** – generates the final travel plan.

## 📸 Application

The application provides an interactive Streamlit interface where users can enter their travel requirements and receive an AI-generated travel plan.

## 👨‍💻 Author

**Pradeep Singh**



## 📄 License

This project is intended for educational and portfolio purposes.
