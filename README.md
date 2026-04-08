# Germany Accident Analysis 🚗

An AI-powered tool to analyze factors causing road accidents 
in Germany using Gemma 4 running locally via Ollama.

## 📋 Project Summary
This project analyzes 763,851 weather records merged with 
official German accident data (2021-2023) to identify the 
primary factors causing road accidents, aligning with 
Germany's **Vision Zero** initiative.

## 🎯 What it does
- Analyzes accident data from 2021-2023
- Merges with weather data (hourly + daily)
- Uses Gemma 4 locally to explain patterns
- Identifies top factors causing accidents
- Visualizes accident hotspots on interactive maps

## 🛠️ Tech Stack
- Gemma 4 (via Ollama) — local AI, no internet needed
- Python + Pandas — data analysis
- Streamlit — user interface
- Matplotlib — visualizations

## 🚀 How to Run
1. Install Ollama
2. Pull Gemma 4: `ollama pull gemma4:e4b`
3. Install requirements: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`

## 📥 How to Get the Data

### Accident Data
Download from the official German statistics portal:
👉 https://unfallatlas.statistikportal.de/

Download years: 2021, 2022, 2023
Place files in: `data/` folder

### Weather Data
Run the provided script to fetch automatically:
```bash
python weather_data.py
```
Weather data is fetched from Open-Meteo API for each 
accident location and date.

## 📊 Weather Data Structure
- **Daily weather** (combined_daily_all_years.csv) 
  → Used for main accident analysis
- **Hourly weather** (kept separate per year ~900MB each)
  → Used for animated weather map
  → Load individually to avoid memory issues

## 🗺️ Location Code System
German accident data uses official 8-digit municipality 
codes (Amtlicher Gemeindeschlüssel / AGS).
We created a custom lookup table (asg.csv) to map 
these codes to real state, district and city names.

## ⚠️ Data Decisions

### Why 2020 Was Excluded
2020 data showed significantly fewer accident records due to 
**COVID-19 lockdowns** reducing road traffic dramatically.
Including 2020 would skew results — analysis covers 2021-2023 
to reflect normal road conditions.

### Missing Exact Dates
The original dataset contains only **year**, **month**, 
and **weekday** — no exact day.

**Solution:** We estimated dates by finding the first 
occurrence of the given weekday in that month, then combined 
with the accident hour to create a full timestamp for 
weather data merging.
> This may introduce a small margin of error in weather matching.

## 📖 Data Documentation
See [Data Description](docs/DSB_Unfallatlas_EN.pdf) 
for full explanation of all columns.

## 🔑 Key Findings
*(Will be updated after analysis is complete)*

## 👩🏼 Author
Lamiaa Bahgat
