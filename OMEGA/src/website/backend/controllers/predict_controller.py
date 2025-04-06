import sys
import os
import math
import pandas as pd

# Add the parent directory to sys.path to import the model
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from OMEGA.src.website.model.model_loader import F1PredictionModel


class PredictController:
    def __init__(self):
        self.model = F1PredictionModel()

        # Define paths to CSV files - fixed path resolution
        # Go up to src directory (3 levels up from controllers)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.metrics_dir = os.path.join(self.base_dir, 'datascraper', 'data', 'performance_logic',
                                        'performance_metrics')

        # Print paths for debugging
        print(f"Base directory: {self.base_dir}")
        print(f"Metrics directory: {self.metrics_dir}")

        self.differences_path = os.path.join(self.metrics_dir, 'performance_differences.csv')
        self.speed_path = os.path.join(self.metrics_dir, 'performance_speed.csv')
        self.wet_path = os.path.join(self.metrics_dir, 'performance_wet.csv')

        # Verify file existence
        print(f"Differences file exists: {os.path.exists(self.differences_path)}")
        print(f"Speed file exists: {os.path.exists(self.speed_path)}")
        print(f"Wet file exists: {os.path.exists(self.wet_path)}")

    def predict_performance(self, data):
        """
        Process incoming data and return team performance predictions

        Args:
            data (dict): User input data with race conditions

        Returns:
            dict: Prediction results with team performances
        """
        # Validate input data
        required_fields = ['st_speed', 'compound', 'air_temperature', 'rainfall',
                           'wind_direction', 'wind_speed']

        for field in required_fields:
            if field not in data:
                return {"error": f"Missing required field: {field}"}, 400

        try:
            # Get base lap time prediction from model
            base_lap_time = self.model.predict(data)

            # Convert lap time to performance score (faster = higher score)
            # 85s = 100%, 95s = 90% (arbitrary scale)
            base_performance = 100 - (base_lap_time - 85) * 1.0

            # Generate team-specific predictions
            teams = self._get_team_predictions(base_performance, data)

            # Create race conditions summary
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

            # Return formatted response
            return {
                "teams": teams,
                "raceConditions": race_conditions,
                "trackName": "F1 Grand Prix"
            }, 200

        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}, 500

    def _get_team_predictions(self, base_performance, conditions):
        """
        Generate team-specific predictions based on conditions and CSV data only

        Args:
            base_performance (float): Base performance value from model
            conditions (dict): Race conditions

        Returns:
            list: Team performance predictions
        """
        # Define team base data (names, logos, and IDs only)
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

        # Map team names to their CSV lookup names
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

        # Load CSV data
        try:
            # Load performance differences (for baseModifier)
            diff_df = pd.read_csv(self.differences_path)
            diff_df.columns = [col.strip() for col in diff_df.columns]

            # Load speed data (for powerUnit)
            speed_df = pd.read_csv(self.speed_path)
            speed_df.columns = [col.strip() for col in speed_df.columns]

            # Load wet performance data
            wet_df = pd.read_csv(self.wet_path)
            wet_df.columns = [col.strip() for col in wet_df.columns]

            # Calculate normalized scores (0-100) for speed and wet performance
            max_speed = speed_df['Average Max Speed'].max()
            min_speed = speed_df['Average Max Speed'].min()
            speed_range = max_speed - min_speed

            max_wet_speed = wet_df['Average Wet Max Speed'].max()
            min_wet_speed = wet_df['Average Wet Max Speed'].min()
            wet_range = max_wet_speed - min_wet_speed

            # Print debug info
            print(f"Speed range: {min_speed} - {max_speed}")
            print(f"Wet speed range: {min_wet_speed} - {max_wet_speed}")

        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return []  # Empty list if data can't be loaded

        # Create team predictions based on CSV data only
        teams = []
        for team_data in team_base_data:
            csv_team_name = team_name_map.get(team_data["name"], team_data["name"])

            # Get metrics from CSV files
            base_modifier = self._get_base_modifier(diff_df, csv_team_name)
            power_unit = self._get_power_score(speed_df, csv_team_name, min_speed, speed_range)
            wet_performance = self._get_wet_score(wet_df, csv_team_name, min_wet_speed, wet_range)

            # Create team with metrics
            team = {
                **team_data,
                "baseModifier": base_modifier,
                "powerUnit": power_unit,
                "wetPerformance": wet_performance
            }

            # Calculate performance modifier based only on conditions and metrics
            # No team-specific hardcoded advantages
            performanceModifier = self._calculate_performance_modifier(team, conditions)

            # Calculate final performance
            team["finalPerformance"] = round(base_performance * team["baseModifier"] + performanceModifier, 1)
            teams.append(team)

        # Sort teams by performance
        teams.sort(key=lambda x: x["finalPerformance"], reverse=True)

        # Calculate advantage relative to top team
        topPerformance = teams[0]["finalPerformance"]
        for team in teams:
            if team["finalPerformance"] == topPerformance:
                team["advantage"] = "BASELINE"
            else:
                team["advantage"] = f"{round(team['finalPerformance'] - topPerformance, 1)}%"

        return teams

    def _calculate_performance_modifier(self, team, conditions):
        """Calculate performance modifier based only on conditions and metrics"""
        performanceModifier = 0

        # Tire compound effects - based only on metrics
        if conditions['compound'] == "Soft":
            # Teams with good power unit do well with softs
            tireEffect = (team["powerUnit"] - 80) / 200
            performanceModifier += tireEffect
        elif conditions['compound'] == "Hard":
            # No team-specific adjustments, just general effects
            hardEffect = (90 - team["powerUnit"]) / 200  # Higher adjustment for lower power teams
            performanceModifier += hardEffect
        elif conditions['compound'] in ["Wet", "Intermediate"]:
            # Teams with good wet performance do better
            wetEffect = (team["wetPerformance"] - 80) / 100
            performanceModifier += wetEffect

        # Temperature effects - based on conditions only
        air_temp = float(conditions['air_temperature'])
        if air_temp > 30:
            # High temps affect all teams equally
            tempEffect = (air_temp - 30) / 100
            performanceModifier += tempEffect
        elif air_temp < 15:
            # Low temps affect all teams equally
            tempEffect = (15 - air_temp) / 100
            performanceModifier += tempEffect

        # Rain effects - based on wet performance metric
        rainfall = float(conditions['rainfall'])
        if rainfall > 0:
            # Teams with better wet weather performance
            rainEffect = (rainfall * team["wetPerformance"]) / 1000
            performanceModifier += rainEffect

        # Straight line speed effects - based on power unit metric
        st_speed = float(conditions['st_speed'])
        if st_speed > 330:
            # Teams with better power unit benefit
            powerEffect = (team["powerUnit"] - 80) / 200
            performanceModifier += powerEffect

        return performanceModifier

    def _get_base_modifier(self, df, team_name):
        """Get base modifier from difference data (difference + 1)"""
        try:
            team_row = df[df['Team'] == team_name]
            if not team_row.empty:
                diff_value = team_row['Difference from Best (s)'].values[0]
                # Higher difference means slower, so we invert the effect
                # We want base modifier to be highest for best team (lowest difference)
                return 1 + (1 - min(1, diff_value)) / 100  # Small adjustment to keep close to 1.0
            return 1.0  # Default if team not found
        except Exception as e:
            print(f"Error getting base modifier for {team_name}: {e}")
            return 1.0

    def _get_power_score(self, df, team_name, min_speed, speed_range):
        """Get power unit score (0-100) based on max speed data"""
        try:
            team_row = df[df['Team'] == team_name]
            if not team_row.empty and speed_range > 0:
                speed_value = team_row['Average Max Speed'].values[0]
                # Normalize to 0-100 range
                normalized_score = ((speed_value - min_speed) / speed_range) * 100
                # Scale to 80-100 range for better gameplay balance
                return 80 + (normalized_score * 20 / 100)
            return 90  # Default if team not found or range is zero
        except Exception as e:
            print(f"Error getting power score for {team_name}: {e}")
            return 90

    def _get_wet_score(self, df, team_name, min_wet_speed, wet_range):
        """Get wet performance score (0-100) based on wet max speed data"""
        try:
            team_row = df[df['Team'] == team_name]
            if not team_row.empty and wet_range > 0:
                wet_speed_value = team_row['Average Wet Max Speed'].values[0]
                # Normalize to 0-100 range
                normalized_score = ((wet_speed_value - min_wet_speed) / wet_range) * 100
                # Scale to 75-100 range for better gameplay balance
                return 75 + (normalized_score * 25 / 100)
            return 85  # Default if team not found or range is zero
        except Exception as e:
            print(f"Error getting wet score for {team_name}: {e}")
            return 85
