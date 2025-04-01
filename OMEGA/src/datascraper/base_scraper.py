import json
import time
import os
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# Global delay (in seconds) between API requests.
DELAY = 1

class BaseScraper:
    def __init__(self, year: str):
        self.year = year
        # Each subclass should set an output_prefix appropriate to its sessions.
        self.output_prefix = "output"

    def fetch_json(self, url: str):
        """
        Fetch JSON data from the given URL using urllib. Introduces a delay after each
        request to help avoid rate limitations.
        """
        try:
            with urlopen(url) as response:
                data = json.loads(response.read().decode("utf-8"))
            # Delay to avoid overloading the API.
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
        Abstract method to fetch sessions. Subclasses must override this method.
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
        Fetch lap data for the given session using URL-encoded query parameters.
        Only laps with duration under 120 seconds are returned.
        """
        url = (
            f"https://api.openf1.org/v1/laps?session_key={session_key}"
            "&is_pit_out_lap=false&lap_duration%3C=120"
        )
        data = self.fetch_json(url)
        return data if isinstance(data, list) else []

    def process_session(self, session: dict):
        """
        Process a single session:
          - Retrieve driver data and group drivers by team.
          - Retrieve lap data; for each driver record all laps under 120 seconds and
            identify the fastest lap.
        Returns a tuple (session_key, session_result) where session_result is a dictionary
        keyed by team.
        """
        session_key = session.get("session_key")
        circuit_short_name = session.get("circuit_short_name")
        print(f"Processing session: {session_key}" + f" {circuit_short_name}")

        # Fetch and organize drivers by team.
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

        # Fetch laps and record qualifying laps.
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

            # Only record laps under 120 seconds.
            if lap_duration_val < 120:
                lap_copy = lap.copy()
                lap_copy["lap_duration"] = lap_duration_val
                driver_all_laps.setdefault(driver_num, []).append(lap_copy)
                if (driver_num not in fastest_laps or
                        lap_duration_val < fastest_laps[driver_num]["lap_duration"]):
                    fastest_laps[driver_num] = lap_copy

        # Assemble the results grouped by team.
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
          - Save the results into the `scraped_data` folder.
        """
        sessions = self.fetch_sessions()
        if not sessions:
            print("No sessions found for the provided year.")
            return

        final_results = {}
        for session in sessions:
            session_key, session_output = self.process_session(session)
            final_results[session_key] = session_output

        # Ensure the output directory exists.
        output_dir = "scraped_data"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"{self.output_prefix}_{self.year}.json")
        try:
            with open(output_filename, "w") as outfile:
                json.dump(final_results, outfile, indent=4)
            print("Data successfully saved to", output_filename)
        except Exception as e:
            print("Error writing JSON file:", e)
