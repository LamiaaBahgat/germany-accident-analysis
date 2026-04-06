# Germany Accident Analysis 🚗

An AI-powered tool to analyze factors 
causing road accidents in Germany using 
Gemma 4 running locally via Ollama.

## What it does
- Analyzes accident data from multiple years
- Merges with weather data (hourly + daily)
- Uses Gemma 4 to explain patterns
- Identifies top factors causing accidents

## Tech Stack
- Gemma 4 (via Ollama) — local AI, no internet needed
- Python + Pandas — data analysis
- Streamlit — user interface
- Matplotlib — visualizations

## How to run
1. Install Ollama
2. Pull Gemma 4: `ollama pull gemma4:e4b`
3. Install requirements: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`

## Data
- Accident data: 2019-2021 (Germany)
- Weather data: hourly + daily records

## Author
Lamiaa Bahgat
