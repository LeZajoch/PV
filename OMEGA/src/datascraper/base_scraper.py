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
        # This will hold reference driver data (from a session with complete driver info).
        self.reference_drivers = None

    @staticmethod
    def safe_field(value, default):
        """
        Return value if it is not None or empty; otherwise, return the default.
        """
        if value is None:
            return default
        if isinstance(value, str) and value.strip() == "":
            return default
        return value

    def fetch_json(self, url: str):
        """
        Fetch JSON data from the given URL using urlopen.
        Retries up to three times for HTTP 429 or 500 errors.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with urlopen(url) as response:
                    data = json.loads(response.read().decode("utf-8"))
                time.sleep(DELAY)
                return data
            except HTTPError as e:
                if e.code in [429, 500]:
                    wait_time = DELAY * (attempt + 1)
                    print(f"HTTP Error {e.code} for {url}. Waiting {wait_time} seconds before retry (attempt {attempt+1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue
                else:
                    print("HTTP error fetching", url, ":", e)
                    break
            except URLError as e:
                print("URL error fetching", url, ":", e)
                break
            except Exception as e:
                print("Error fetching", url, ":", e)
                break
        return None

    def fetch_sessions(self):
        """
        Abstract method. Subclasses must override this method.
        Returns a list of session dictionaries.
        """
        raise NotImplementedError("Subclasses must implement the fetch_sessions method!")

    def fetch_drivers(self, session_key: str):
        """
        Fetch driver information for the given session.
        """
        url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

    def fetch_laps(self, session_key: str):
        """
        Fetch lap data for the given session.
        Only laps with a duration under 120 seconds are considered.
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
        """
        url = f"https://api.openf1.org/v1/stints?session_key={session_key}"
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

    def fetch_weather(self, session_key: str):
        """
        Fetch weather data for the given session.
        """
        url = f"https://api.openf1.org/v1/weather?session_key={session_key}"
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

    def get_closest_weather(self, lap_datetime: datetime, weather_list: list):
        """
        Given a lap datetime and a list of weather records (each with a "parsed_date"),
        return a copy of the weather record closest in time to lap_datetime.
        In case of a tie, choose the record that is earlier.
        Remove the temporary "parsed_date" key before returning.
        """
        best_record = None
        best_diff = float("inf")
        for record in weather_list:
            parsed = record.get("parsed_date")
            if parsed is None:
                continue
            diff = abs((lap_datetime - parsed).total_seconds())
            if diff < best_diff:
                best_diff = diff
                best_record = record
            elif diff == best_diff:
                if record["parsed_date"] <= lap_datetime and best_record["parsed_date"] > lap_datetime:
                    best_record = record
        if best_record is not None:
            sanitized = best_record.copy()
            sanitized.pop("parsed_date", None)
            return sanitized
        return None

    def find_reference_driver_data(self):
        """
        Loop over sessions until a session with complete driver info is found.
        Complete means every driver record has non-empty driver_number, full_name, and team_name.
        Returns a dictionary mapping an identifier (e.g., "num:<driver_number>") to complete driver info.
        """
        sessions = self.fetch_sessions()
        for session in sessions:
            session_key = session.get("session_key")
            drivers_data = self.fetch_drivers(session_key)
            all_complete = True
            for driver in drivers_data:
                if not (driver.get("driver_number") and driver.get("full_name") and
                        driver.get("team_name") and driver.get("team_name").strip() != ""):
                    all_complete = False
                    break
            if all_complete and drivers_data:
                ref = {}
                for driver in drivers_data:
                    num = driver.get("driver_number")
                    name = driver.get("full_name")
                    team = driver.get("team_name")
                    if num is not None and str(num).strip() != "":
                        key = f"num:{str(num).strip()}"
                    elif name is not None and name.strip() != "":
                        key = f"name:{name.strip()}"
                    else:
                        key = None
                    if key:
                        ref[key] = {"driver_number": num, "full_name": name, "team_name": team}
                if ref:
                    print(f"Reference driver data found from session {session_key}")
                    return ref
            else:
                print(f"Session {session.get('session_key')} has incomplete driver data. Trying next session...")
        print("WARNING: No complete reference driver data found.")
        return None

    def is_session_complete(self, session_result: dict) -> bool:
        """
        Consider a session complete if its result exists and each driver's record in every team
        has a non-empty 'fastest_lap' field.
        """
        if not session_result:
            return False
        for team, drivers in session_result.items():
            for d in drivers:
                if not d.get("fastest_lap"):
                    return False
        return True

    def process_session(self, session: dict):
        """
        Process a single session:
          - Retrieve driver data and merge/fill missing fields (driver_number, full_name, team_name)
            using preceding records.
          - For any driver missing team_name, use the reference driver data (if available) to fill in.
          - Build a drivers_info mapping and group drivers by team.
          - Retrieve lap data (< 120 sec) and determine the fastest lap per driver.
          - Retrieve tire stint data and assign tire information to laps.
          - Retrieve weather data and attach, for each lap, the record whose time is closest to 'date_start'.
          - Adjust tire compound: if tire_data compound is "UNKNOWN", set to "INTERMEDIATE" if weather indicates rain; otherwise "SOFT".
        Returns a tuple (session_key, session_result), where session_result is grouped by team.
        If critical data is missing, returns an empty dictionary.
        """
        session_key = session.get("session_key")
        circuit_short_name = session.get("circuit_short_name")
        print(f"\nProcessing session: {session_key} - {circuit_short_name}")

        # --- Merge/Fill Driver Data ---
        drivers_data = self.fetch_drivers(session_key)
        if not drivers_data:
            print(f"Session {session_key}: No driver data returned.")
            return session_key, {}
        aggregated = {}
        for driver in drivers_data:
            num = driver.get("driver_number")
            name = driver.get("full_name")
            team = driver.get("team_name")
            if num is not None and str(num).strip() != "":
                key = f"num:{str(num).strip()}"
            elif name is not None and name.strip() != "":
                key = f"name:{name.strip()}"
            else:
                key = None
            if key:
                if key in aggregated:
                    existing = aggregated[key]
                    if not (num is not None and str(num).strip() != ""):
                        num = existing.get("driver_number")
                    if not (name is not None and name.strip() != ""):
                        name = existing.get("full_name")
                    if not (team is not None and team.strip() != ""):
                        team = existing.get("team_name")
                    aggregated[key] = {"driver_number": num, "full_name": name, "team_name": team}
                else:
                    aggregated[key] = {"driver_number": num, "full_name": name, "team_name": team}
                driver["driver_number"] = num
                driver["full_name"] = name
                driver["team_name"] = team

        # --- Fill Missing Team Names Using Reference Data ---
        if self.reference_drivers:
            for driver in drivers_data:
                team = driver.get("team_name")
                if not (team and team.strip() != ""):
                    num = driver.get("driver_number")
                    name = driver.get("full_name")
                    key = None
                    if num is not None and str(num).strip() != "":
                        key = f"num:{str(num).strip()}"
                    elif name is not None and name.strip() != "":
                        key = f"name:{name.strip()}"
                    if key and key in self.reference_drivers:
                        driver["team_name"] = self.reference_drivers[key].get("team_name")

        # --- Build Final Drivers Info and Group by Team ---
        drivers_info = {}
        teams = {}
        for driver in drivers_data:
            driver_num = self.safe_field(driver.get("driver_number"), "UNKNOWN")
            team_name = self.safe_field(driver.get("team_name"), "UNKNOWN TEAM")
            full_name = self.safe_field(driver.get("full_name"), "UNKNOWN DRIVER")
            drivers_info[driver_num] = {"team": team_name, "name": full_name}
            teams.setdefault(team_name, []).append(driver_num)

        # --- Process Lap Data ---
        laps_data = self.fetch_laps(session_key)
        if not laps_data:
            print(f"Session {session_key}: No lap data returned.")
            return session_key, {}
        driver_all_laps = {}
        fastest_laps = {}
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

        # --- Process Tire Stint Data ---
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

        # --- Process Weather Data ---
        weather_data = self.fetch_weather(session_key)
        if weather_data:
            for w in weather_data:
                try:
                    w["parsed_date"] = datetime.fromisoformat(w.get("date"))
                except Exception:
                    w["parsed_date"] = None
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

        # --- Update Tire Compound Based on Weather ---
        for driver_num, laps in driver_all_laps.items():
            for lap in laps:
                tire = lap.get("tire_data")
                if tire and tire.get("compound") == "UNKNOWN":
                    weather = lap.get("weather_data") or {}
                    description = (weather.get("weather") or weather.get("condition") or "").lower()
                    if "rain" in description:
                        tire["compound"] = "INTERMEDIATE"
                    else:
                        tire["compound"] = "SOFT"

        # --- Assemble Final Results Grouped by Team ---
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

    def save_results(self, results: dict):
        """
        Save the aggregated results into the folder data/scraped_data.
        """
        output_dir = os.path.join("data", "scraped_data")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"{self.output_prefix}_{self.year}.json")
        try:
            with open(output_filename, "w", encoding="utf-8") as outfile:
                json.dump(results, outfile, indent=4)
            print("Data successfully saved to", output_filename)
        except Exception as e:
            print("Error writing JSON file:", e)

    def run(self):
        """
        Main method to run the scraper:
          - Before scraping, load existing results from data/scraped_data (if any).
          - Fetch all sessions for the year and build a dictionary keyed by session_key.
          - Compare this list to the keys in the loaded results; only scrape sessions missing or incomplete.
          - Process each missing session one by one (saving after each) and gather a list of incomplete sessions.
          - Retry incomplete sessions up to 10 attempts. If after 10 attempts some remain incomplete, prompt the user to try another 10 attempts.
          - Save final aggregated results into data/scraped_data.
        """
        # Prepare output directory and file name
        output_dir = os.path.join("data", "scraped_data")
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"{self.output_prefix}_{self.year}.json")

        # Load existing results if available.
        final_results = {}
        if os.path.exists(output_filename):
            try:
                with open(output_filename, "r", encoding="utf-8") as f:
                    final_results = json.load(f)
                print("Loaded existing results from", output_filename)
            except Exception as e:
                print("Could not load existing file; starting fresh:", e)
                final_results = {}

        # Fetch complete session list for the year.
        sessions = self.fetch_sessions()
        if not sessions:
            print("No sessions found for the provided year.")
            return

        # Build a dictionary of sessions keyed by session_key (as string).
        sessions_dict = {}
        for session in sessions:
            key = session.get("session_key")
            if key is not None:
                sessions_dict[str(key)] = session

        # Determine which sessions need to be scraped (missing or incomplete).
        missing_session_keys = []
        for key in sessions_dict:
            if key not in final_results:
                missing_session_keys.append(key)
            else:
                if not self.is_session_complete(final_results[key]):
                    missing_session_keys.append(key)

        print("Total sessions from API:", len(sessions_dict))
        print("Sessions to be scraped/re-scraped:", missing_session_keys)

        incomplete_sessions = []
        for key in missing_session_keys:
            session = sessions_dict[key]
            s_key, result = self.process_session(session)
            if self.is_session_complete(result):
                final_results[s_key] = result
                print(f"Session {s_key} scraped successfully and is complete.")
            else:
                final_results[s_key] = result
                incomplete_sessions.append(session)
                print(f"Session {s_key} scraped but remains incomplete.")
            self.save_results(final_results)
            time.sleep(DELAY)

        max_attempts = 10
        attempt_counter = 0

        while incomplete_sessions and attempt_counter < max_attempts:
            print(f"\nRetry attempt {attempt_counter + 1} for {len(incomplete_sessions)} incomplete session(s).")
            still_incomplete = []
            for session in incomplete_sessions:
                s_key, result = self.process_session(session)
                if self.is_session_complete(result):
                    final_results[s_key] = result
                    print(f"Session {s_key} is now complete on retry.")
                else:
                    still_incomplete.append(session)
                time.sleep(DELAY)
            incomplete_sessions = still_incomplete
            attempt_counter += 1
            self.save_results(final_results)

        while incomplete_sessions:
            user_input = input(f"\nThere are {len(incomplete_sessions)} sessions still incomplete after {max_attempts} attempts. "
                               "Do you want to try another 10 attempts? (y/n): ").strip().lower()
            if user_input != "y":
                break
            attempt_counter = 0
            while incomplete_sessions and attempt_counter < max_attempts:
                print(f"\nAdditional attempt round {attempt_counter + 1} for {len(incomplete_sessions)} incomplete session(s).")
                still_incomplete = []
                for session in incomplete_sessions:
                    s_key, result = self.process_session(session)
                    if self.is_session_complete(result):
                        final_results[s_key] = result
                        print(f"Session {s_key} is now complete on additional retry.")
                    else:
                        still_incomplete.append(session)
                    time.sleep(DELAY)
                incomplete_sessions = still_incomplete
                attempt_counter += 1
                self.save_results(final_results)

        self.save_results(final_results)
        print("Final results have been saved.")
