import pickle
import numpy as np
import os


class F1PredictionModel:
    def __init__(self):
        # Path to the model file
        model_path = os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl')
        # Load the model
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def predict(self, features):
        """
        Make a prediction using the loaded model

        Args:
            features (dict): Dictionary containing:
                - st_speed: Straight-line speed (km/h)
                - compound: Tire compound (string)
                - air_temperature: Air temperature (°C)
                - rainfall: Rainfall (mm)
                - wind_direction: Wind direction (degrees)
                - wind_speed: Wind speed (km/h)

        Returns:
            float: Predicted fastest lap duration
        """
        # One-hot encode the compound
        compound_HARD = 1 if features['compound'] == 'Hard' else 0
        compound_INTERMEDIATE = 1 if features['compound'] == 'Intermediate' else 0
        compound_MEDIUM = 1 if features['compound'] == 'Medium' else 0
        compound_SOFT = 1 if features['compound'] == 'Soft' else 0

        # Prepare features in the order expected by the model
        X = np.array([
            float(features['st_speed']),
            # Duration sectors are not available from input, will be predicted separately or estimated
            0.0,  # duration_sector_1 placeholder
            0.0,  # duration_sector_2 placeholder
            0.0,  # duration_sector_3 placeholder
            float(features['air_temperature']),
            float(features['rainfall']),
            float(features['wind_direction']),
            float(features['wind_speed']),
            compound_HARD,
            compound_INTERMEDIATE,
            compound_MEDIUM,
            compound_SOFT
        ]).reshape(1, -1)

        # Make prediction using the actual ML model
        try:
            predicted_lap_time = self.model.predict(X)[0]
            return round(predicted_lap_time, 3)
        except Exception as e:
            print(f"Prediction error: {e}")
            return 90.0  # Default value if prediction fails
