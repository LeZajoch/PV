#!/usr/bin/env python3
import json
import time
import os
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime

# Global delay (in seconds) between API requests.
DELAY = 1

class BaseScraper:
    def __init__(self, year: str):
        self.year = year
        # This output_prefix will be used to build the output file name.
        self.output_prefix = "output"

    def fetch_json(self, url: str):
        """
        Fetch JSON data from the given URL using urllib.
        A delay is introduced after every request to avoid hitting rate limits.
        """
        try:
            with urlopen(url) as response:
                data = json.loads(response.read().decode("utf-8"))
            time.sleep(DELAY)
            return data
        except HTTPError as e:
            print("HTTP error fetching", url, ":", e)
        except URLError as e:
            print("URL error fetching", url, ":", e)
        except Exception as e:
            print("Error fetching", url, ":", e)
        time.sleep(DELAY)
        return None

    def fetch_sessions(self):
        """
        Abstract method to fetch sessions.
        Subclasses must override this method.
        """
        raise NotImplementedError(
            "Subclasses must implement the fetch_sessions method!"
        )

    def fetch_drivers(self, session_key: str):
        """
        Fetch driver information for the given session.
        """
        url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

    def fetch_laps(self, session_key: str):
        """
        Fetch lap data for a given session.
        Only laps with duration under 120 seconds are of interest.
        """
        url = (
            f"https://api.openf1.org/v1/laps?session_key={session_key}"
            "&is_pit_out_lap=false&lap_duration%3C=120"
        )
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

    def fetch_tires(self, session_key: str):
        """
        Fetch tire stint data for the given session.
        Tire data will include tire compound details along with lap range
        information (if provided via lap_start and lap_end).
        """
        url = f"https://api.openf1.org/v1/stints?session_key={session_key}"
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

    def fetch_weather(self, session_key: str):
        """
        Fetch weather data for the given session.
        Weather data should include a timestamp in the "date" field.
        """
        url = f"https://api.openf1.org/v1/weather?session_key={session_key}"
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

    def get_closest_weather(self, lap_datetime: datetime, weather_list: list):
        """
        Given a lap's datetime and a list of weather records (each containing a
        parsed_date key), return a copy of the weather record whose timestamp is closest to
        lap_datetime. If two records are equally close, choose the one that is earlier.
        The returned record will be stripped of the temporary 'parsed_date' key.
        """
        best_record = None
        best_diff = float('inf')
        for record in weather_list:
            parsed = record.get("parsed_date")
            if parsed is None:
                continue
            diff = abs((lap_datetime - parsed).total_seconds())
            if diff < best_diff:
                best_diff = diff
                best_record = record
            elif diff == best_diff:
                # In case of a tie, choose the record that occurs before the lap time.
                if record["parsed_date"] <= lap_datetime and best_record["parsed_date"] > lap_datetime:
                    best_record = record
        if best_record is not None:
            sanitized = best_record.copy()
            sanitized.pop("parsed_date", None)
            return sanitized
        return None

    def process_session(self, session: dict):
        """
        Process a single session:
          - Retrieve driver data and group drivers by team.
          - Retrieve lap data, recording all laps under 120 seconds and identifying
            the fastest lap per driver.
          - Retrieve tire stint data and assign tire information to laps (duplicating it
            into all laps if a lap range is specified).
          - Retrieve weather data and, for each lap, assign the weather observation
            closest in time to the lap's date_start (if two are equally close, choose
            the one before the lap's time).
        Returns a tuple (session_key, session_result), where session_result is a dictionary
        keyed by team.
        """
        session_key = session.get("session_key")
        circuit_short_name = session.get("circuit_short_name")
        print(f"Processing session: {session_key}" + f" - {circuit_short_name}")

        # Process driver data.
        drivers_data = self.fetch_drivers(session_key)
        drivers_info = {}
        teams = {}
        for driver in drivers_data:
            driver_num = driver.get("driver_number")
            if driver_num is None:
                continue
            team = driver.get("team_name", "Unknown Team")
            name = driver.get("full_name", "Unknown Driver")
            drivers_info[driver_num] = {"team": team, "name": name}
            teams.setdefault(team, []).append(driver_num)

        # Process lap data.
        laps_data = self.fetch_laps(session_key)
        driver_all_laps = {}  # All eligible laps per driver.
        fastest_laps = {}     # Fastest lap per driver.
        for lap in laps_data:
            driver_num = lap.get("driver_number")
            if driver_num is None:
                continue
            lap_duration = lap.get("lap_duration")
            if lap_duration is None:
                continue
            try:
                lap_duration_val = float(lap_duration)
            except (ValueError, TypeError):
                continue

            if lap_duration_val < 120:
                lap_copy = lap.copy()
                lap_copy["lap_duration"] = lap_duration_val
                driver_all_laps.setdefault(driver_num, []).append(lap_copy)
                if (driver_num not in fastest_laps or
                        lap_duration_val < fastest_laps[driver_num]["lap_duration"]):
                    fastest_laps[driver_num] = lap_copy

        # Process tire stint data.
        stints = self.fetch_tires(session_key)
        if stints:
            for stint in stints:
                driver_num = stint.get("driver_number")
                if driver_num is None or driver_num not in driver_all_laps:
                    continue
                lap_start = stint.get("lap_start")
                lap_end = stint.get("lap_end")
                if lap_start is not None and lap_end is not None:
                    try:
                        start = int(lap_start)
                        end = int(lap_end)
                    except (ValueError, TypeError):
                        continue
                    for lap in driver_all_laps.get(driver_num, []):
                        try:
                            lnum = int(lap.get("lap_number"))
                        except (ValueError, TypeError):
                            continue
                        if start <= lnum <= end:
                            lap["tire_data"] = stint
                else:
                    # If no range is provided, check if a specific lap is indicated.
                    specific_lap = stint.get("lap_number")
                    if specific_lap is not None:
                        try:
                            specific_lap = int(specific_lap)
                        except (ValueError, TypeError):
                            continue
                        for lap in driver_all_laps.get(driver_num, []):
                            try:
                                lnum = int(lap.get("lap_number"))
                            except (ValueError, TypeError):
                                continue
                            if lnum == specific_lap:
                                lap["tire_data"] = stint

        # Process weather data.
        weather_data = self.fetch_weather(session_key)
        if weather_data:
            # Parse the weather 'date' field to a datetime object for comparison.
            for w in weather_data:
                try:
                    w["parsed_date"] = datetime.fromisoformat(w.get("date"))
                except Exception:
                    w["parsed_date"] = None
            # For each lap, assign the closest weather observation.
            for driver_num, laps in driver_all_laps.items():
                for lap in laps:
                    lap_start_str = lap.get("date_start")
                    if not lap_start_str:
                        continue
                    try:
                        lap_dt = datetime.fromisoformat(lap_start_str)
                    except Exception:
                        continue
                    closest_weather = self.get_closest_weather(lap_dt, weather_data)
                    lap["weather_data"] = closest_weather

        # Assemble the final results grouped by team.
        session_result = {}
        for team, driver_nums in teams.items():
            team_drivers = []
            for num in driver_nums:
                driver_record = {
                    "driver_number": num,
                    "name": drivers_info[num]["name"],
                    "fastest_lap": fastest_laps.get(num),
                    "laps": driver_all_laps.get(num, [])
                }
                team_drivers.append(driver_record)
            session_result[team] = team_drivers

        return session_key, session_result

    def run(self):
        """
        Main method to run the scraper:
          - Fetch sessions.
          - Process each session.
          - Save the results into the "scraped_data" folder.
        """
        sessions = self.fetch_sessions()
        if not sessions:
            print("No sessions found for the provided year.")
            return

        final_results = {}
        for session in sessions:
            session_key, session_output = self.process_session(session)
            final_results[session_key] = session_output

        output_dir = "scraped_data"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"{self.output_prefix}_{self.year}.json")
        try:
            with open(output_filename, "w") as outfile:
                json.dump(final_results, outfile, indent=4)
            print("Data successfully saved to", output_filename)
        except Exception as e:
            print("Error writing JSON file:", e)
