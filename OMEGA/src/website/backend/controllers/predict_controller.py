import sys
import os
import pandas as pd

# Adjust sys.path to ensure that the F1PredictionModel can be imported.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from OMEGA.src.website.model.model_loader import F1PredictionModel


class PredictController:
    """
    PredictController handles the performance prediction for F1 teams using a pre-trained model
    and additional performance metrics stored in CSV files.
    """

    def __init__(self):
        """
        Initialize the PredictController by loading the prediction model and setting up
        the directory paths for performance metrics CSV files.
        """
        # Load the pre-trained F1 prediction model.
        self.model = F1PredictionModel()

        # Set the base directory four levels up from the current file.
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        # Define the directory path where performance metrics CSV files are stored.
        self.metrics_dir = os.path.join(self.base_dir, 'datascraper', 'data', 'performance_logic',
                                        'performance_metrics')

        # Debug: Print the base and metrics directory paths.
        print(f"Base directory: {self.base_dir}")
        print(f"Metrics directory: {self.metrics_dir}")

        # Define paths for each performance metrics CSV file.
        self.differences_path = os.path.join(self.metrics_dir, 'performance_differences.csv')
        self.speed_path = os.path.join(self.metrics_dir, 'performance_speed.csv')
        self.wet_path = os.path.join(self.metrics_dir, 'performance_wet.csv')

        # Verify file existence and print status for debugging.
        print(f"Differences file exists: {os.path.exists(self.differences_path)}")
        print(f"Speed file exists: {os.path.exists(self.speed_path)}")
        print(f"Wet file exists: {os.path.exists(self.wet_path)}")

    def predict_performance(self, data):
        """
        Predict performance for a given set of lap and weather conditions.

        Args:
            data (dict): Dictionary containing input features such as 'st_speed', 'compound',
                         'air_temperature', 'rainfall', 'wind_direction', and 'wind_speed'.

        Returns:
            tuple: A tuple with a response dictionary and an HTTP status code.
        """
        # Check for all required fields in the input data.
        required_fields = ['st_speed', 'compound', 'air_temperature', 'rainfall',
                           'wind_direction', 'wind_speed']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400

        try:
            # Predict the base lap time using the pre-trained model.
            base_lap_time = self.model.predict(data)

            # Convert lap time to a performance score (lower lap time equals higher performance).
            # Arbitrary scale: 85s = 100%, 95s = 90%
            base_performance = 100 - (base_lap_time - 85) * 1.0

            # Get team-specific predictions based on the base performance and conditions.
            teams = self._get_team_predictions(base_performance, data)

            # Create a summary of the race conditions.
            race_conditions = {
                "trackTemp": str(float(data['air_temperature']) + 10),
                "airTemp": data['air_temperature'],
                "humidity": str(round(50 + (float(data['air_temperature']) / 100 * 30), 1)),
                "windSpeed": data['wind_speed'],
                "windDirection": data['wind_direction'],
                "rainfall": data['rainfall'],
                "compound": data['compound'],
                "predictedLapTime": str(base_lap_time)
            }

            # Return a formatted response with team predictions and race conditions.
            return {
                "teams": teams,
                "raceConditions": race_conditions,
                "trackName": "F1 Comparator"
            }, 200

        except Exception as e:
            # Return an error response if prediction fails.
            return {"error": f"Prediction failed: {str(e)}"}, 500

    def _get_team_predictions(self, base_performance, conditions):
        """
        Calculate team performance predictions based on base performance and additional CSV metrics.

        Args:
            base_performance (float): The base performance score computed from lap time.
            conditions (dict): Input conditions used for further performance adjustments.

        Returns:
            list: A sorted list of team dictionaries with their performance scores.
        """
        # Define basic information for each team.
        team_base_data = [
            {
                "id": 1,
                "name": "Red Bull Racing",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/red-bull-racing-logo.png.transform/2col/image.png",
            },
            {
                "id": 2,
                "name": "Ferrari",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/ferrari-logo.png.transform/2col/image.png",
            },
            {
                "id": 3,
                "name": "Mercedes",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/mercedes-logo.png.transform/2col/image.png",
            },
            {
                "id": 4,
                "name": "McLaren",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/mclaren-logo.png.transform/2col/image.png",
            },
            {
                "id": 5,
                "name": "Aston Martin",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/aston-martin-logo.png.transform/2col/image.png",
            },
            {
                "id": 6,
                "name": "Alpine F1 Team",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/alpine-logo.png.transform/2col/image.png",
            },
            {
                "id": 7,
                "name": "Williams",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/williams-logo.png.transform/2col/image.png",
            },
            {
                "id": 8,
                "name": "AlphaTauri",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/alphatauri-logo.png.transform/2col/image.png",
            },
            {
                "id": 9,
                "name": "Alfa Romeo",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/alfa-romeo-logo.png.transform/2col/image.png",
            },
            {
                "id": 10,
                "name": "Haas F1 Team",
                "logo": "https://www.formula1.com/content/dam/fom-website/teams/2023/haas-f1-team-logo.png.transform/2col/image.png",
            }
        ]

        # Map team names to the CSV lookup names used in the performance metrics.
        team_name_map = {
            "Red Bull Racing": "Red Bull Racing",
            "Ferrari": "Ferrari",
            "Mercedes": "Mercedes",
            "McLaren": "McLaren",
            "Aston Martin": "Aston Martin",
            "Alpine F1 Team": "Alpine",
            "Williams": "Williams",
            "AlphaTauri": "RB & AlphaTauri",
            "Alfa Romeo": "Alfa Romeo & Kick Sauber",
            "Haas F1 Team": "Haas F1 Team"
        }

        try:
            # Load performance metrics CSVs.
            diff_df = pd.read_csv(self.differences_path)
            diff_df.columns = [col.strip() for col in diff_df.columns]

            speed_df = pd.read_csv(self.speed_path)
            speed_df.columns = [col.strip() for col in speed_df.columns]

            wet_df = pd.read_csv(self.wet_path)
            wet_df.columns = [col.strip() for col in wet_df.columns]

            # Calculate speed ranges for normalization.
            max_speed = speed_df['Average Max Speed'].max()
            min_speed = speed_df['Average Max Speed'].min()
            speed_range = max_speed - min_speed

            max_wet_speed = wet_df['Average Wet Max Speed'].max()
            min_wet_speed = wet_df['Average Wet Max Speed'].min()
            wet_range = max_wet_speed - min_wet_speed

            # Debug: Print speed ranges.
            print(f"Speed range: {min_speed} - {max_speed}")
            print(f"Wet speed range: {min_wet_speed} - {max_wet_speed}")

        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return []  # Return empty list if data can't be loaded

        teams = []
        # Process each team's data and compute performance adjustments.
        for team_data in team_base_data:
            csv_team_name = team_name_map.get(team_data["name"], team_data["name"])

            # Retrieve modifiers from the CSV data.
            base_modifier = self._get_base_modifier(diff_df, csv_team_name)
            power_unit = self._get_power_score(speed_df, csv_team_name, min_speed, speed_range)
            wet_performance = self._get_wet_score(wet_df, csv_team_name, min_wet_speed, wet_range)

            # Build team dictionary with base and CSV-derived metrics.
            team = {
                **team_data,
                "baseModifier": base_modifier,
                "powerUnit": power_unit,
                "wetPerformance": wet_performance
            }

            # Calculate additional performance modifier based on race conditions.
            performanceModifier = self._calculate_performance_modifier(team, conditions)
            team["finalPerformance"] = round(base_performance * team["baseModifier"] + performanceModifier, 1)
            teams.append(team)

        # Sort teams based on final performance score in descending order.
        teams.sort(key=lambda x: x["finalPerformance"], reverse=True)

        # Calculate advantage compared to the top performing team.
        topPerformance = teams[0]["finalPerformance"]
        for team in teams:
            if team["finalPerformance"] == topPerformance:
                team["advantage"] = "BASELINE"
            else:
                team["advantage"] = f"{round(team['finalPerformance'] - topPerformance, 1)}%"

        return teams

    def _calculate_performance_modifier(self, team, conditions):
        """
        Calculate a performance modifier for a team based on tire compound and weather conditions.

        Args:
            team (dict): Team data including power unit and wet performance metrics.
            conditions (dict): Race conditions from input data.

        Returns:
            float: The calculated performance modifier.
        """
        performanceModifier = 0

        # Adjust modifier based on tire compound.
        if conditions['compound'] == "Soft":
            tireEffect = (team["powerUnit"] - 80) / 200
            performanceModifier += tireEffect
        elif conditions['compound'] == "Hard":
            hardEffect = (90 - team["powerUnit"]) / 200
            performanceModifier += hardEffect
        elif conditions['compound'] in ["Wet", "Intermediate"]:
            wetEffect = (team["wetPerformance"] - 80) / 100
            performanceModifier += wetEffect

        # Adjust based on air temperature.
        air_temp = float(conditions['air_temperature'])
        if air_temp > 30:
            tempEffect = (air_temp - 30) / 100
            performanceModifier += tempEffect
        elif air_temp < 15:
            tempEffect = (15 - air_temp) / 100
            performanceModifier += tempEffect

        # Adjust based on rainfall.
        rainfall = float(conditions['rainfall'])
        if rainfall > 0:
            rainEffect = (rainfall * team["wetPerformance"]) / 1000
            performanceModifier += rainEffect

        # Adjust based on straight-line speed.
        st_speed = float(conditions['st_speed'])
        if st_speed > 330:
            powerEffect = (team["powerUnit"] - 80) / 200
            performanceModifier += powerEffect

        return performanceModifier

    def _get_base_modifier(self, df, team_name):
        """
        Retrieve the base modifier for a team from the differences CSV.

        Args:
            df (DataFrame): The DataFrame containing performance differences.
            team_name (str): The name of the team (as used in the CSV).

        Returns:
            float: The base modifier for the team.
        """
        try:
            team_row = df[df['Team'] == team_name]
            if not team_row.empty:
                diff_value = team_row['Difference from Best (s)'].values[0]
                return 1 + (1 - min(1, diff_value)) / 100
            return 1.0
        except Exception as e:
            print(f"Error getting base modifier for {team_name}: {e}")
            return 1.0

    def _get_power_score(self, df, team_name, min_speed, speed_range):
        """
        Calculate the normalized power score for a team based on max speed data.

        Args:
            df (DataFrame): The DataFrame with average max speed data.
            team_name (str): The team name for lookup.
            min_speed (float): The minimum speed in the dataset.
            speed_range (float): The range of speeds in the dataset.

        Returns:
            float: The calculated power score.
        """
        try:
            team_row = df[df['Team'] == team_name]
            if not team_row.empty and speed_range > 0:
                speed_value = team_row['Average Max Speed'].values[0]
                normalized_score = ((speed_value - min_speed) / speed_range) * 100
                return 80 + (normalized_score * 20 / 100)
            return 90
        except Exception as e:
            print(f"Error getting power score for {team_name}: {e}")
            return 90

    def _get_wet_score(self, df, team_name, min_wet_speed, wet_range):
        """
        Calculate the normalized wet performance score for a team based on wet speed data.

        Args:
            df (DataFrame): The DataFrame with average wet max speed data.
            team_name (str): The team name for lookup.
            min_wet_speed (float): The minimum wet speed in the dataset.
            wet_range (float): The range of wet speeds in the dataset.

        Returns:
            float: The calculated wet performance score.
        """
        try:
            team_row = df[df['Team'] == team_name]
            if not team_row.empty and wet_range > 0:
                wet_speed_value = team_row['Average Wet Max Speed'].values[0]
                normalized_score = ((wet_speed_value - min_wet_speed) / wet_range) * 100
                return 75 + (normalized_score * 25 / 100)
            return 85
        except Exception as e:
            print(f"Error getting wet score for {team_name}: {e}")
            return 85
