import pandas as pd
import os
import glob

# --- Configuration ---
# This should be the same directory where your individual CSV files are saved
INPUT_DIR = 'weather_data_output_2023'

# Define the names for your combined output files
COMBINED_HOURLY_OUTPUT_FILE = 'combined_all_hourly_weather_data_2023.csv'
COMBINED_DAILY_OUTPUT_FILE = 'combined_all_daily_weather_data_2023.csv'

# --- Main execution ---
if __name__ == "__main__":
    # --- Combine Hourly Data ---
    print(f"Combining all hourly data from '{INPUT_DIR}'...")
    all_hourly_files = glob.glob(os.path.join(INPUT_DIR, 'hourly_*.csv'))

    if not all_hourly_files:
        print("No hourly CSV files found in the input directory. Skipping hourly combination.")
    else:
        # Create an empty list to store individual hourly dataframes
        hourly_dfs = []
        for f_path in all_hourly_files:
            try:
                df = pd.read_csv(f_path)
                hourly_dfs.append(df)
            except Exception as e:
                print(f"Error reading hourly file {f_path}: {e}")

        if hourly_dfs:
            combined_hourly_df = pd.concat(hourly_dfs, ignore_index=True)
            output_path_hourly = os.path.join(INPUT_DIR, COMBINED_HOURLY_OUTPUT_FILE)
            combined_hourly_df.to_csv(output_path_hourly, index=False)
            print(f"✅ Successfully combined {len(all_hourly_files)} hourly files into {output_path_hourly}")
            print(
                f"Combined hourly DataFrame has {len(combined_hourly_df)} rows and {len(combined_hourly_df.columns)} columns.")
        else:
            print("No hourly dataframes were successfully loaded to combine.")

    # --- Combine Daily Data ---
    print(f"\nCombining all daily data from '{INPUT_DIR}'...")
    all_daily_files = glob.glob(os.path.join(INPUT_DIR, 'daily_*.csv'))

    if not all_daily_files:
        print("No daily CSV files found in the input directory. Skipping daily combination.")
    else:
        # Create an empty list to store individual daily dataframes
        daily_dfs = []
        for f_path in all_daily_files:
            try:
                df = pd.read_csv(f_path)
                daily_dfs.append(df)
            except Exception as e:
                print(f"Error reading daily file {f_path}: {e}")

        if daily_dfs:
            combined_daily_df = pd.concat(daily_dfs, ignore_index=True)
            output_path_daily = os.path.join(INPUT_DIR, COMBINED_DAILY_OUTPUT_FILE)
            combined_daily_df.to_csv(output_path_daily, index=False)
            print(f"✅ Successfully combined {len(all_daily_files)} daily files into {output_path_daily}")
            print(
                f"Combined daily DataFrame has {len(combined_daily_df)} rows and {len(combined_daily_df.columns)} columns.")
        else:
            print("No daily dataframes were successfully loaded to combine.")

    print("\n--- Combination Complete ---")