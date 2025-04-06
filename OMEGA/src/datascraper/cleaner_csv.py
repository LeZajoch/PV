import json
import csv
import os

# Define CSV column mappings as tuples of (Column Header, extractor_function).
# Each extractor function takes (session_key, circuit, team, record) and returns the value for that column.
CSV_COLUMNS = [
    ("Session Code", lambda sess, circuit, team, rec: sess),
    ("Circuit Short Name", lambda sess, circuit, team, rec: circuit),
    ("Team", lambda sess, circuit, team, rec: team),
    ("Driver Number", lambda sess, circuit, team, rec: rec.get("driver_number", "")),
    ("Driver Name", lambda sess, circuit, team, rec: rec.get("name", "")),
    (
        "Fastest Lap Duration",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("lap_duration", ""),
    ),
    (
        "st_speed",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("st_speed", ""),
    ),
    (
        "Duration Sector 1",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("duration_sector_1", ""),
    ),
    (
        "Duration Sector 2",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("duration_sector_2", ""),
    ),
    (
        "Duration Sector 3",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("duration_sector_3", ""),
    ),
    (
        "Compound",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("tire_data", {}).get("compound", ""),
    ),
    (
        "Tyre Age",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("tire_data", {}).get("tyre_age", ""),
    ),
    (
        "Air Temperature",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("weather_data", {}).get("air_temperature",
                                                                                                    ""),
    ),
    (
        "Rainfall",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("weather_data", {}).get("rainfall", ""),
    ),
    (
        "Track Temp",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("weather_data", {}).get("track_temp", ""),
    ),
    (
        "Wind Direction",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("weather_data", {}).get("wind_direction",
                                                                                                    ""),
    ),
    (
        "Wind Speed",
        lambda sess, circuit, team, rec: (rec.get("fastest_lap") or {}).get("weather_data", {}).get("wind_speed", ""),
    )
]


def convert_json_to_csv(json_file_path, csv_file_path):
    """
    Convert JSON scraped data to a CSV file using the defined CSV_COLUMNS mapping.

    Args:
        json_file_path (str): Path to the input JSON file.
        csv_file_path (str): Path where the output CSV file will be written.
    """
    # Read the JSON data.
    with open(json_file_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    rows = []
    # Iterate through each session and extract CSV rows.
    for session_key, session_data in data.items():
        circuit = session_data.get("circuit_short_name", "UNKNOWN")
        teams_dict = session_data.get("teams", {})
        for team, driver_records in teams_dict.items():
            for rec in driver_records:
                # Build a row by applying each extractor function.
                row = [extractor(session_key, circuit, team, rec)
                       for header, extractor in CSV_COLUMNS]
                rows.append(row)

    # Write the rows to a CSV file.
    with open(csv_file_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        # Write CSV header.
        writer.writerow([header for header, _ in CSV_COLUMNS])
        writer.writerows(rows)

    print(f"CSV file successfully written to: {csv_file_path}")


def main():
    """
    Main function to prompt for a JSON file path and convert it to a cleaned CSV file.

    It verifies the existence of the JSON file, creates necessary directories, and calls
    convert_json_to_csv() with the appropriate paths.
    """
    input_file = input("Enter the input JSON file name (with path if needed): ").strip()
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return

    # Determine output CSV filename based on the input file's base name.
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join("data", "cleaned_data")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{base_name}_cleaned.csv")
    print(f"Output will be written to: {output_file}")
    convert_json_to_csv(input_file, output_file)


if __name__ == "__main__":
    main()
