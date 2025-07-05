# Wand-Agent

A Python-based AI travel assistant that helps you plan trips with real-time data and smart suggestions.

## Quick Start
1. Clone the repo:
   ```sh
   git clone https://github.com/Sakethsreeram7/Wand-Agent.git
   cd Wand-Agent
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
curl -X 'POST' \
  'http://localhost:8000/query' \
  -H 'Content-Type: application/json' \
  -d '{
  "messages": [
    {
      "role": "user",
      "content": "Trip to Goa, 4 days, in ₹15k budget"
    }
  ]
}'
```

## Project Structure
- `run.py` — Entry point
- `app/` — Main code (agents, tools, UI, API)
- `requirements.txt` — Dependencies

## Environment Variables
- `GOOGLE_API_KEY` (required)
- `GROQ_API_KEY` (required)
- `OPENWEATHERMAP_API_KEY` (optional)