import pandas as pd
import os

# ============================================
# Combine Weather Data - Daily Only
# ============================================
# DESIGN DECISION / DESIGNENTSCHEIDUNG
#
# Daily data: combined all years into one file
# → Small size (~136MB), used for main analysis
#
# Hourly data: kept separate per year
# → Each file ~900MB, loaded individually
# → Used for animated weather map per year
# → Combining all would exceed 2.6GB RAM limit
#
# Tägliche Daten: alle Jahre in einer Datei
# → Kleine Größe (~136MB), für Hauptanalyse
#
# Stündliche Daten: getrennt pro Jahr
# → Jede Datei ~900MB, einzeln geladen
# → Für animierte Wetterkarte pro Jahr
# → Zusammenführung würde 2.6GB RAM überschreiten
# ============================================

INPUT_DIR = '/Users/lamiaabahgat/Documents/Portfolio/data_4_years/pycharm/venv/weather_data_output'
OUTPUT_DIR = '/Users/lamiaabahgat/Documents/germany-accident-analysis'

YEARS = [2021, 2022, 2023]

all_daily = []

print("📅 Loading daily weather data for all years...")
print("📅 Tägliche Wetterdaten für alle Jahre werden geladen...")

for year in YEARS:
    daily_path = os.path.join(INPUT_DIR, f'combined_{year}_daily_weather_data.csv')

    if os.path.exists(daily_path):
        df = pd.read_csv(daily_path)
        all_daily.append(df)
        print(f"✅ Daily {year}: {len(df)} rows loaded")
    else:
        print(f"⚠️  Daily {year} not found at: {daily_path}")

# ============================================
# Save combined daily file
# ============================================
if all_daily:
    print("\n💾 Combining and saving...")
    combined_daily = pd.concat(all_daily, ignore_index=True)

    output_path = os.path.join(OUTPUT_DIR, 'combined_daily_all_years.csv')
    combined_daily.to_csv(output_path, index=False)

    print(f"\n✅ Saved: combined_daily_all_years.csv")
    print(f"   Total rows: {len(combined_daily)}")
    print(f"   Total columns: {len(combined_daily.columns)}")
    print(f"   Columns: {list(combined_daily.columns)}")
    print(f"\n   Years included: {YEARS}")
else:
    print("\n❌ No daily data found! Check your INPUT_DIR path.")

# ============================================
# Hourly files info — kept separate per year
# ============================================
print("\n📋 Hourly files available (kept separate):")
print("📋 Stündliche Dateien verfügbar (getrennt):")
for year in YEARS:
    hourly_path = os.path.join(INPUT_DIR, f'combined_{year}_hourly_weather_data.csv')
    if os.path.exists(hourly_path):
        size_mb = os.path.getsize(hourly_path) / (1024 * 1024)
        print(f"   ✅ {year}: combined_{year}_hourly_weather_data.csv ({size_mb:.1f} MB)")
    else:
        print(f"   ⚠️  {year}: not found")

print("\n--- ✅ Done! / Fertig! ---")