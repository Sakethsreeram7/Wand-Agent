# Wand-Agent

A Python-based AI travel assistant that helps you plan trips with real-time data and smart suggestions.

## Features
- AI-powered itinerary planning
- Real-time weather, currency, and place info
- Budget and expense calculations
- Streamlit UI and FastAPI backend

## Quick Start
1. Clone the repo:
   ```sh
   git clone https://github.com/Sakethsreeram7/Wand-Agent.git
   cd AI_Trip_Planner
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up API keys:
   -  Add `.env` and add your keys
4. Run the app:
   - Streamlit UI: `python run.py web` (http://localhost:8501)
   - FastAPI API: `python run.py api` (http://localhost:8000)

## API Example
```sh
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Trip to Paris, 4 days, $1500 budget"}'
```

## Project Structure
- `run.py` — Entry point
- `app/` — Main code (agents, tools, UI, API)
- `requirements.txt` — Dependencies
- `test_components.py` — Component tests

## Environment Variables
- `GROQ_API_KEY` (required)
- `OPENWEATHERMAP_API_KEY` (optional)
- `EXCHANGERATE_API_KEY` (optional)

## License
MIT License © 2025




