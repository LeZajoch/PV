#!/usr/bin/env python3
import json
import csv
import os

# Define the CSV columns.
# Each tuple maps the CSV header to a lambda that extracts a value.
# The lambda receives 4 arguments: (session_code, circuit, team, driver_record)
CSV_COLUMNS = [
    ("Session Code", lambda sess, circuit, team, rec: sess),
    ("Circuit Short Name", lambda sess, circuit, team, rec: circuit),
    ("Team", lambda sess, circuit, team, rec: team),
    ("Driver Number", lambda sess, circuit, team, rec: rec.get("driver_number", "")),
    ("Driver Name", lambda sess, circuit, team, rec: rec.get("name", "")),
    (
        "Fastest Lap Duration",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("lap_duration", ""),
    ),
    (
        "st_speed",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("st_speed", ""),
    ),
    (
        "Duration Sector 1",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("duration_sector_1", ""),
    ),
    (
        "Duration Sector 2",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("duration_sector_2", ""),
    ),
    (
        "Duration Sector 3",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("duration_sector_3", ""),
    ),
    (
        "Compound",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("tire_data", {}).get("compound", ""),
    ),
    (
        "Tyre Age",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("tire_data", {}).get("tyre_age", ""),
    ),
    (
        "Air Temperature",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {}).get("air_temperature", ""),
    ),
    (
        "Rainfall",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {}).get("rainfall", ""),
    ),
    (
        "Track Temp",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {}).get("track_temp", ""),
    ),
    (
        "Wind Direction",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {}).get("wind_direction", ""),
    ),
    (
        "Wind Speed",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {}).get("wind_speed", ""),
    )
]

def convert_json_to_csv(json_file_path, csv_file_path):
    # Load the JSON file.
    with open(json_file_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    rows = []
    # Data is expected to be a dict keyed by session key.
    for session_key, session_data in data.items():
        # Retrieve the session-level circuit short name.
        circuit = session_data.get("circuit_short_name", "UNKNOWN")
        # Retrieve the teams dictionary.
        teams_dict = session_data.get("teams", {})
        for team, driver_records in teams_dict.items():
            for rec in driver_records:
                # Build a CSV row with our extractors.
                row = [extractor(session_key, circuit, team, rec)
                       for header, extractor in CSV_COLUMNS]
                rows.append(row)

    # Write the CSV file.
    with open(csv_file_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow([header for header, _ in CSV_COLUMNS])
        writer.writerows(rows)

    print(f"CSV file successfully written to: {csv_file_path}")

def main():
    input_file = input("Enter the input JSON file name (with path if needed): ").strip()
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    # Construct output file name.
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join("data", "cleaned_data")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{base_name}_cleaned.csv")
    print(f"Output will be written to: {output_file}")
    convert_json_to_csv(input_file, output_file)

if __name__ == "__main__":
    main()
