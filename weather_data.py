
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import os
import requests

# --- Configuration ---
# Define the name of your input file containing location and date data.
# This script is now configured for the 2022 data file.
INPUT_FILENAME = '/Users/lamiaabahgat/Documents/Portfolio/data_4_years/pycharm/venv/openmeteo_all_germany_2023.txt'

# Define the directory where you want to save the output CSV files.
OUTPUT_DIR = 'weather_data_output_2023'

# --- RESUME FEATURE ---
# Set the line number to start processing from.
# Setting to 1 to start from the beginning as requested.
START_LINE = 1
# --------------------
# --- CACHE CLEARING OPTION ---
# Set to True to clear the cache before starting a new run.
# Set to False to keep the cache and benefit from previously downloaded data.
CLEAR_CACHE_BEFORE_RUN = False
# -----------------------------

# --- FETCH MODE OPTION ---
# This script is now configured to fetch both daily and hourly data.
FETCH_MODE = "ALL"
# -------------------------


# --- Setup Open-Meteo API Client with Cache and Retry ---
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)

# Perform cache clearing if enabled
if CLEAR_CACHE_BEFORE_RUN:
    print("Clearing cache before starting new fetch...")
    cache_session.cache.clear()
    print("Cache cleared.")

retry_session: requests.Session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Define common weather variables ---
HOURLY_VARS = [
    "temperature_2m", "rain", "snowfall", "wind_speed_10m",
    "wind_direction_10m", "weather_code", "shortwave_radiation", "cloud_cover"
]
DAILY_VARS = [
    "weather_code", "temperature_2m_mean", "temperature_2m_max",
    "temperature_2m_min", "precipitation_sum", "rain_sum",
    "sunrise", "sunset", "daylight_duration", "sunshine_duration"
]


# --- Function to process each location and date range ---
def fetch_and_process_weather_data(latitude, longitude, timezone, start_date, end_date, fetch_mode):
    """
    Fetches weather data for a given location and date range,
    based on the specified fetch_mode, and returns DataFrames.
    """
    url = "https://customer-archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": timezone,
        "apikey": "0LM33DNELXbI7xJY"
    }

    # Conditionally add hourly and daily parameters based on fetch_mode
    if fetch_mode == "ALL":
        params["hourly"] = HOURLY_VARS
        params["daily"] = DAILY_VARS
    elif fetch_mode == "DAILY_ONLY":
        params["daily"] = DAILY_VARS
        params["hourly"] = []
    else:
        raise ValueError(f"Invalid FETCH_MODE: {fetch_mode}. Must be 'ALL' or 'DAILY_ONLY'.")

    try:
        responses = openmeteo.weather_api(url, params=params)

        if not responses:
            print(
                f"API returned an empty response list for Lat: {latitude}, Lon: {longitude}, Dates: {start_date} to {end_date}.")
            return None, None

        response = responses[0]
        hourly_dataframe = None
        daily_dataframe = None

        # --- Process Hourly Data (if requested and available) ---
        hourly_response_data = response.Hourly()
        if fetch_mode == "ALL" and hourly_response_data:
            try:
                hourly = hourly_response_data
                hourly_timestamps = pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left"
                )

                num_hourly_rows = len(hourly_timestamps)

                hourly_data = {
                    "date": pd.Series(hourly_timestamps),
                    "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
                    "rain": hourly.Variables(1).ValuesAsNumpy(),
                    "snowfall": hourly.Variables(2).ValuesAsNumpy(),
                    "wind_speed_10m": hourly.Variables(3).ValuesAsNumpy(),
                    "wind_direction_10m": hourly.Variables(4).ValuesAsNumpy(),
                    "weather_code": hourly.Variables(5).ValuesAsNumpy(),
                    "shortwave_radiation": hourly.Variables(6).ValuesAsNumpy(),
                    "cloud_cover": hourly.Variables(7).ValuesAsNumpy(),
                    'latitude': [latitude] * num_hourly_rows,
                    'longitude': [longitude] * num_hourly_rows,
                    'timezone': [timezone] * num_hourly_rows,
                    'data_start_date': [start_date] * num_hourly_rows,
                    'data_end_date': [end_date] * num_hourly_rows,
                }
                hourly_dataframe = pd.DataFrame(data=hourly_data)
            except Exception as hourly_e:
                print(
                    f"ERROR: Failed to process hourly data for Lat: {latitude}, Lon: {longitude}. Details: {hourly_e}")
        elif fetch_mode == "ALL" and not hourly_response_data:
            print(f"DEBUG: Hourly data requested but Hourly object is None for Lat: {latitude}, Lon: {longitude}.")

        # --- Process Daily Data (if available) ---
        daily_response_data = response.Daily()
        if daily_response_data:
            try:
                daily = daily_response_data
                daily_timestamps = pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=daily.Interval()),
                    inclusive="left"
                )

                num_daily_rows = len(daily_timestamps)

                daily_data = {
                    "date": pd.Series(daily_timestamps),
                    "weather_code": daily.Variables(0).ValuesAsNumpy(),
                    "temperature_2m_mean": daily.Variables(1).ValuesAsNumpy(),
                    "temperature_2m_max": daily.Variables(2).ValuesAsNumpy(),
                    "temperature_2m_min": daily.Variables(3).ValuesAsNumpy(),
                    "precipitation_sum": daily.Variables(4).ValuesAsNumpy(),
                    "rain_sum": daily.Variables(5).ValuesAsNumpy(),
                    "sunrise": daily.Variables(6).ValuesInt64AsNumpy(),
                    "sunset": daily.Variables(7).ValuesInt64AsNumpy(),
                    "daylight_duration": daily.Variables(8).ValuesAsNumpy(),
                    "sunshine_duration": daily.Variables(9).ValuesAsNumpy(),
                    'latitude': [latitude] * num_daily_rows,
                    'longitude': [longitude] * num_daily_rows,
                    'timezone': [timezone] * num_daily_rows,
                    'data_start_date': [start_date] * num_daily_rows,
                    'data_end_date': [end_date] * num_daily_rows,
                }
                daily_dataframe = pd.DataFrame(data=daily_data)
            except Exception as daily_e:
                print(f"ERROR: Failed to process daily data for Lat: {latitude}, Lon: {longitude}. Details: {daily_e}")
        else:
            print(
                f"DEBUG: Daily object is None for Lat: {latitude}, Lon: {longitude}. Skipping daily dataframe creation.")

        return hourly_dataframe, daily_dataframe

    except requests.exceptions.HTTPError as e:
        print(
            f"ERROR: Failed to fetch data for Lat: {latitude}, Lon: {longitude}, Dates: {start_date} to {end_date}: {e}")
        print(f"API response details: {e.response.text}")
        return None, None
    except Exception as e:
        print(
            f"ERROR: An unexpected error occurred while fetching data for Lat: {latitude}, Lon: {longitude}, Dates: {start_date} to {end_date}: {e}")
        return None, None


# --- Main execution ---
if __name__ == "__main__":
    processed_count = 0
    total_lines = 0

    try:
        print("--- Starting script execution ---")
        with open(INPUT_FILENAME, 'r') as f:
            lines_to_process = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
            total_lines = len(lines_to_process)
            print(f"SUCCESS: Successfully opened input file '{INPUT_FILENAME}'.")
            print(f"Total lines detected in input file: {total_lines}")
            print(f"Starting processing from line: {START_LINE}")
            print(f"Current FETCH_MODE is: {FETCH_MODE}")

            for line_idx, line in enumerate(lines_to_process):
                original_line_num = line_idx + 1

                if original_line_num < START_LINE:
                    if original_line_num == START_LINE - 1 or original_line_num % 1000 == 0:
                        print(f"Skipping line {original_line_num} (before START_LINE: {START_LINE})...")
                    continue

                print(f"\n--- Processing Line {original_line_num}/{total_lines} ---")
                parts = line.split(',')

                if len(parts) < 6:
                    print(
                        f"SKIPPING: Malformed line {original_line_num}: '{line}' (not enough comma-separated values).")
                    continue

                try:
                    latitude = float(parts[0])
                    longitude = float(parts[1])
                    timezone = parts[3].strip()
                    start_date = parts[4].strip()
                    end_date = parts[5].strip()
                    print(f"INFO: Parsed data: Lat: {latitude}, Lon: {longitude}, Dates: {start_date} to {end_date}")

                    # Fetch both daily and hourly data
                    hourly_df, daily_df = fetch_and_process_weather_data(
                        latitude, longitude, timezone, start_date, end_date, FETCH_MODE
                    )

                    if hourly_df is not None or daily_df is not None:
                        coords_str = f"{latitude:.6f}_{longitude:.6f}".replace('.', '_').replace('-', 'minus')

                        # --- Conditionally save Hourly Filename ---
                        if hourly_df is not None:
                            hourly_filename = os.path.join(
                                OUTPUT_DIR,
                                f"hourly_{coords_str}_{start_date}_to_{end_date}.csv"
                            )
                            hourly_df.to_csv(hourly_filename, index=False)
                            print(f"SUCCESS: Saved hourly to {hourly_filename.split(os.sep)[-1]}")

                        # --- Conditionally save Daily Filename ---
                        if daily_df is not None:
                            daily_filename = os.path.join(
                                OUTPUT_DIR,
                                f"daily_{coords_str}_{start_date}_to_{end_date}.csv"
                            )
                            daily_df.to_csv(daily_filename, index=False)
                            print(f"SUCCESS: Saved daily to {daily_filename.split(os.sep)[-1]}")

                        processed_count += 1
                        if processed_count % 50 == 0 or processed_count == total_lines:
                            print(
                                f"Progress: Processed {processed_count}/{total_lines} requests. Current Line: {original_line_num}.")
                    else:
                        print(
                            f"WARNING: No dataframes returned for Lat: {latitude}, Lon: {longitude}. Check for errors above.")


                except ValueError as ve:
                    print(
                        f"ERROR: Parsing data on Line {original_line_num}: {ve} - Could not convert '{parts[0]}' or '{parts[1]}' to float. Line content: '{line}'")
                except IndexError as ie:
                    print(
                        f"ERROR: Missing data parts on Line {original_line_num}: {ie} - Check if line has enough commas. Line content: '{line}'")
                except Exception as e:
                    print(
                        f"ERROR: An unexpected error occurred while processing Line {original_line_num}: {e} - Line content: '{line}')")

    except FileNotFoundError:
        print(f"\nFATAL ERROR: The input file '{INPUT_FILENAME}' was not found.")
        print("Please check that the file path is correct and the file exists.")
    except Exception as e:
        print(f"\nFATAL ERROR: An unexpected error occurred: {e}")

    print(f"\n--- Processing Complete ---")
    print(
        f"Successfully processed {processed_count} out of {total_lines} total potential location(s) from line {START_LINE} onwards.")
    print(f"All individual CSV files are saved in the '{OUTPUT_DIR}' directory.")

