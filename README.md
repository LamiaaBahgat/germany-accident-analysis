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

## 🗺️ Location Code System
German accident data uses official 8-digit municipality 
codes (Amtlicher Gemeindeschlüssel / AGS).
We created a custom lookup table (asg.csv) to map 
these codes to real state, district and city names.

## Data Sources
- Accident data: download from 
  https://unfallatlas.statistikportal.de/
- Weather data: fetched using weather_data.py
  from Open-Meteo API

## ⚠️ Data Limitations & Solutions

### Missing Exact Dates
The original German accident dataset contains only **year**, 
**month**, and **weekday** — no exact day.

**Our solution:** We estimated dates by finding the first 
occurrence of the given weekday in that month, then combined 
with the accident hour to create a full timestamp for 
weather data merging.

> This may introduce a small margin of error in weather matching.

## Data Documentation
See [Data Description](docs/DSB_Unfallatlas_EN.pdf) 
for full explanation of all columns.

## Author
Lamiaa Bahgat
