import json
import csv
import os

# Define the columns to output.
# Each tuple maps a CSV header to a lambda that extracts a value from:
# (session_code, team_name, driver_record)
CSV_COLUMNS = [
    ("Session Code", lambda sess, team, rec: sess),
    ("Team", lambda sess, team, rec: team),
    ("Driver Number", lambda sess, team, rec: rec.get("driver_number", "")),
    ("Driver Name", lambda sess, team, rec: rec.get("name", "")),
    (
        "Fastest Lap Duration",
        lambda sess, team, rec: (rec.get("fastest_lap") or {}).get("lap_duration", ""),
    ),
    (
        "st_speed",
        lambda sess, team, rec: (rec.get("fastest_lap") or {}).get("st_speed", ""),
    ),
    (
        "Duration Sector 1",
        lambda sess, team, rec: (rec.get("fastest_lap") or {}).get("duration_sector_1", ""),
    ),
    (
        "Duration Sector 2",
        lambda sess, team, rec: (rec.get("fastest_lap") or {}).get("duration_sector_2", ""),
    ),
    (
        "Duration Sector 3",
        lambda sess, team, rec: (rec.get("fastest_lap") or {}).get("duration_sector_3", ""),
    ),
    (
        "Compound",
        lambda sess, team, rec: (rec.get("fastest_lap") or {})
        .get("tire_data", {})
        .get("compound", ""),
    ),
    (
        "Tyre Age",
        lambda sess, team, rec: (rec.get("fastest_lap") or {})
        .get("tire_data", {})
        .get("tyre_age", ""),
    ),
    (
        "Air Temperature",
        lambda sess, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {})
        .get("air_temperature", ""),
    ),
    (
        "Rainfall",
        lambda sess, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {})
        .get("rainfall", ""),
    ),
    (
        "Track Temp",
        lambda sess, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {})
        .get("track_temp", ""),
    ),
    (
        "Wind Direction",
        lambda sess, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {})
        .get("wind_direction", ""),
    ),
    (
        "Wind Speed",
        lambda sess, team, rec: (rec.get("fastest_lap") or {})
        .get("weather_data", {})
        .get("wind_speed", ""),
    ),
]


def convert_json_to_csv(json_file_path, csv_file_path):
    # Load the JSON file.
    with open(json_file_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    # Expect data to be a dictionary keyed by session codes.
    rows = []
    for session_code, teams_data in data.items():
        # teams_data is a dictionary: key = team, value = list of driver records.
        for team, driver_records in teams_data.items():
            for rec in driver_records:
                # Build a row using our column extractors.
                row = [extractor(session_code, team, rec) for header, extractor in CSV_COLUMNS]
                rows.append(row)

    # Write the CSV file (this will overwrite an existing file).
    with open(csv_file_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        # Write headers.
        writer.writerow([header for header, extractor in CSV_COLUMNS])
        # Write all rows.
        writer.writerows(rows)

    print(f"CSV file successfully written to: {csv_file_path}")


def main():
    # Prompt the user for input file.
    input_file = input("Enter the input JSON file name (with path if needed): ").strip()

    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    # Use the base name of the input file to create an output file name.
    base_name = os.path.basename(input_file)
    name, _ = os.path.splitext(base_name)

    # Create output directory "data/cleaned_data" if it doesn't exist.
    output_dir = os.path.join("data", "cleaned_data")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{name}_cleaned.csv")
    print(f"Output will be written to: {output_file}")

    # Convert JSON to CSV.
    convert_json_to_csv(input_file, output_file)


if __name__ == "__main__":
    main()
