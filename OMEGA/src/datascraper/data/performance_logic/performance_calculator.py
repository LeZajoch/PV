import os
import csv


def parse_duration(duration_str):
    """
    Parse a duration string that may be provided either
    as a plain number (seconds) or in the format m:ss.sss,
    and return its value in seconds.
    """
    duration_str = duration_str.strip()
    if ":" in duration_str:
        try:
            minutes, seconds = duration_str.split(":")
            return int(minutes) * 60 + float(seconds)
        except ValueError:
            raise ValueError(f"Invalid time format: {duration_str}")
    else:
        return float(duration_str)


def normalize_team(team):
    """
    Normalize team names based on the following rules:
      1. Group team names that are "RB" or "AlphaTauri" (ignoring case and spaces)
         into "RB & AlphaTauri".
      2. Group team names that are "Alfa Romeo" or "Kick Sauber"
         (ignoring case and spaces) into "Alfa Romeo & Kick Sauber".
      3. Leave all other teams unchanged.
    """
    team_clean = team.strip()
    lower_nospace = team_clean.lower().replace(" ", "")

    if lower_nospace in ["rb", "alphatauri"]:
        return "RB & AlphaTauri"
    elif lower_nospace in ["alfaromeo", "kicksauber"]:
        return "Alfa Romeo & Kick Sauber"
    else:
        return team_clean


def main():
    input_file = "performance_metrics_data.csv"

    # Create output folder if it does not exist.
    output_folder = "performance_metrics"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize accumulators for lap durations.
    team_duration_sums = {}
    team_duration_counts = {}

    # Initialize accumulators for overall max speed.
    team_speed_sums = {}
    team_speed_counts = {}

    # Initialize accumulators for wet sessions max speed.
    team_wet_speed_sums = {}
    team_wet_speed_counts = {}

    # Read the CSV file and accumulate data for each (normalized) team.
    try:
        with open(input_file, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Normalize the team name.
                team = normalize_team(row["Team"])

                # Process fastest lap duration.
                duration_str = row["Fastest Lap Duration"].strip()
                duration = parse_duration(duration_str)
                team_duration_sums[team] = team_duration_sums.get(team, 0.0) + duration
                team_duration_counts[team] = team_duration_counts.get(team, 0) + 1

                # Process overall max speed from the "st_speed" column.
                try:
                    speed = float(row["st_speed"].strip())
                    team_speed_sums[team] = team_speed_sums.get(team, 0.0) + speed
                    team_speed_counts[team] = team_speed_counts.get(team, 0) + 1
                except ValueError:
                    # Skip rows with invalid speed values.
                    continue

                # Process wet sessions: only include rows where Rainfall equals 1.
                try:
                    rainfall_val = float(row["Rainfall"].strip())
                except ValueError:
                    rainfall_val = 0.0
                if rainfall_val == 1.0:
                    try:
                        wet_speed = float(row["st_speed"].strip())
                        team_wet_speed_sums[team] = team_wet_speed_sums.get(team, 0.0) + wet_speed
                        team_wet_speed_counts[team] = team_wet_speed_counts.get(team, 0) + 1
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.")
        return
    except Exception as e:
        print("An error occurred while reading the input file:", e)
        return

    # --- Lap Duration Analysis ---
    # Calculate the average fastest lap duration for each team.
    team_avg_duration = {}
    for team in team_duration_sums:
        if team_duration_counts[team] > 0:
            team_avg_duration[team] = team_duration_sums[team] / team_duration_counts[team]

    # Write performance metrics (lap durations) to perforance_metrics.csv.
    metrics_file_path = os.path.join(output_folder, "perforance_metrics.csv")
    try:
        with open(metrics_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Team", "Average Fastest Lap Duration (s)"])
            for team, avg in team_avg_duration.items():
                writer.writerow([team, f"{avg:.3f}"])
    except Exception as e:
        print("An error occurred while writing the performance metrics file:", e)
        return

    # Determine the best (minimum) average lap duration.
    best_avg_duration = min(team_avg_duration.values(), default=None)
    if best_avg_duration is None:
        print("No lap duration data available.")
        return

    # Calculate the difference from the best for each team.
    duration_differences = {
        team: avg - best_avg_duration for team, avg in team_avg_duration.items()
    }

    # Write lap duration differences to performance_differences.csv.
    differences_file_path = os.path.join(output_folder, "performance_differences.csv")
    try:
        with open(differences_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Team", "Difference from Best (s)"])
            for team, diff in duration_differences.items():
                writer.writerow([team, f"{diff:.3f}"])
    except Exception as e:
        print("An error occurred while writing the performance differences file:", e)
        return

    # --- Overall Speed Analysis ---
    # Calculate the average max speed for each team.
    team_avg_speed = {}
    for team in team_speed_sums:
        if team_speed_counts[team] > 0:
            team_avg_speed[team] = team_speed_sums[team] / team_speed_counts[team]

    # Determine the best average speed (i.e., highest average max speed).
    best_avg_speed = max(team_avg_speed.values(), default=None)
    if best_avg_speed is None:
        print("No overall max speed data available.")
        return

    # Calculate the difference in max speed relative to the best.
    speed_differences = {
        team: best_avg_speed - avg for team, avg in team_avg_speed.items()
    }

    # Write the overall team speeds and differences into performance_speed.csv.
    speed_file_path = os.path.join(output_folder, "performance_speed.csv")
    try:
        with open(speed_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Team", "Average Max Speed", "Difference from Best"])
            for team, avg_speed in team_avg_speed.items():
                writer.writerow([team, f"{avg_speed:.3f}",
                                 f"{speed_differences[team]:.3f}"])
    except Exception as e:
        print("An error occurred while writing the performance speed file:", e)
        return

    # --- Wet Sessions Speed Analysis ---
    # Calculate the average max speed for each team in wet conditions (Rainfall == 1).
    team_avg_wet_speed = {}
    for team in team_wet_speed_sums:
        if team_wet_speed_counts[team] > 0:
            team_avg_wet_speed[team] = team_wet_speed_sums[team] / team_wet_speed_counts[team]

    # Determine the best average speed in wet conditions.
    best_avg_wet_speed = max(team_avg_wet_speed.values(), default=None)
    if best_avg_wet_speed is None:
        print("No wet session speed data available.")
    else:
        # Calculate the difference in wet speed relative to the best (highest speed wins).
        wet_speed_differences = {
            team: best_avg_wet_speed - avg
            for team, avg in team_avg_wet_speed.items()
        }

        # Write the wet session speeds and differences into performance_wet.csv.
        wet_file_path = os.path.join(output_folder, "performance_wet.csv")
        try:
            with open(wet_file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Team", "Average Wet Max Speed", "Difference from Best"])
                for team, avg_speed in team_avg_wet_speed.items():
                    writer.writerow([team, f"{avg_speed:.3f}",
                                     f"{wet_speed_differences[team]:.3f}"])
        except Exception as e:
            print("An error occurred while writing the wet performance file:", e)
            return

    print(f"Analysis complete! Files saved in the '{output_folder}' folder:")
    print(" - perforance_metrics.csv")
    print(" - performance_differences.csv")
    print(" - performance_speed.csv")
    print(" - performance_wet.csv")


if __name__ == "__main__":
    main()
