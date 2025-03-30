#!/usr/bin/env python3
import json
import time
import os
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# Set the delay (in seconds) between requests.
DELAY = 1


def fetch_json(url: str):
    """
    Fetch JSON data from the given URL using urllib.
    A delay is introduced after each request.
    """
    try:
        with urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
        # Delay to avoid triggering rate limits.
        time.sleep(DELAY)
        return data
    except HTTPError as e:
        print("HTTP error fetching", url, ":", e)
    except URLError as e:
        print("URL error fetching", url, ":", e)
    except Exception as e:
        print("Error fetching", url, ":", e)
    # On error, delay before returning.
    time.sleep(DELAY)
    return None


def fetch_sessions(year: str):
    """
    Fetch qualifying sessions for the provided year.
    """
    url = f"https://api.openf1.org/v1/sessions?session_name=Qualifying&year={year}"
    data = fetch_json(url)
    # API returns a list.
    return data if isinstance(data, list) else []


def fetch_drivers(session_key: str):
    """
    Fetch driver information for the given session.
    """
    url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
    data = fetch_json(url)
    return data if isinstance(data, list) else []


def fetch_laps(session_key: str):
    """
    Fetch laps for the given session with provided filters.
    The URL uses URL-encoded parameters for lap_duration.
    """
    url = (
        f"https://api.openf1.org/v1/laps?session_key={session_key}"
        "&is_pit_out_lap=false&lap_duration%3C=120"
    )
    data = fetch_json(url)
    return data if isinstance(data, list) else []


def process_session(session: dict):
    """
    Process one session:
      - Get drivers (using driver_number as unique id) and group them by team (team_name).
      - Fetch lap records for the session and, for each driver,
        store all laps with a lap duration under 120 seconds and mark the fastest lap.
    Returns a tuple (session_key, session_result).
    """
    session_key = session.get("session_key")
    print(f"Processing session: {session_key}")

    # Fetch driver info and group drivers by team.
    drivers_data = fetch_drivers(session_key)
    drivers_info = {}
    teams = {}
    for driver in drivers_data:
        # Use driver_number as unique identifier.
        driver_num = driver.get("driver_number")
        if driver_num is None:
            continue

        # Use "team_name" and "full_name" from the API response.
        team = driver.get("team_name", "Unknown Team")
        name = driver.get("full_name", "Unknown Driver")
        drivers_info[driver_num] = {"team": team, "name": name}
        teams.setdefault(team, []).append(driver_num)

    # Fetch laps and collect all laps under 120 seconds.
    laps_data = fetch_laps(session_key)
    driver_all_laps = {}  # Record all qualifying laps per driver.
    fastest_laps = {}  # Record the fastest lap per driver.
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

        # Record only laps that are under 120 seconds.
        if lap_duration_val < 120:
            lap_copy = lap.copy()
            lap_copy["lap_duration"] = lap_duration_val
            driver_all_laps.setdefault(driver_num, []).append(lap_copy)
            if (driver_num not in fastest_laps or
                    lap_duration_val < fastest_laps[driver_num]["lap_duration"]):
                fastest_laps[driver_num] = lap_copy

    # Assemble the results grouping drivers by team.
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


def main():
    year = input("Enter a year (e.g. 2023): ").strip()
    try:
        int(year)
    except ValueError:
        print("Invalid year entered!")
        return

    sessions = fetch_sessions(year)
    if not sessions:
        print("No sessions found for the provided year.")
        return

    final_results = {}
    for session in sessions:
        session_key, session_output = process_session(session)
        final_results[session_key] = session_output

    # Ensure that the scraped_data directory exists
    output_dir = "scraped_data"
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, f"fast_laps_{year}.json")

    try:
        with open(output_filename, "w") as outfile:
            json.dump(final_results, outfile, indent=4)
        print("Data successfully saved to", output_filename)
    except Exception as e:
        print("Error writing JSON file:", e)


if __name__ == "__main__":
    main()
