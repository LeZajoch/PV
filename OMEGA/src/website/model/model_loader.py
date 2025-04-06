import pickle
import numpy as np
import os


class F1PredictionModel:
    """
    F1PredictionModel loads a pre-trained machine learning model to predict F1 lap times
    based on various performance and weather-related features.
    """

    def __init__(self):
        """
        Initialize the model by loading the pre-trained Random Forest model from disk.
        """
        # Define the model path relative to this file.
        model_path = os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl')
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def predict(self, features):
        """
        Predict the lap time based on input features.

        The input features dictionary must include:
          - 'st_speed': Straight-line speed.
          - 'compound': Tire compound (e.g., 'Soft', 'Hard', etc.).
          - 'air_temperature': Air temperature.
          - 'rainfall': Rainfall amount.
          - 'wind_direction': Wind direction.
          - 'wind_speed': Wind speed.

        The tire compound is one-hot encoded before being passed to the ML model.

        Args:
            features (dict): Input features for prediction.

        Returns:
            float: Predicted lap time, rounded to three decimal places.
        """
        # One-hot encode the tire compound.
        compound_HARD = 1 if features['compound'] == 'Hard' else 0
        compound_INTERMEDIATE = 1 if features['compound'] == 'Intermediate' else 0
        compound_MEDIUM = 1 if features['compound'] == 'Medium' else 0
        compound_SOFT = 1 if features['compound'] == 'Soft' else 0

        # Build the feature array expected by the ML model.
        X = np.array([
            float(features['st_speed']),
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

        # Make prediction using the loaded ML model.
        try:
            predicted_lap_time = self.model.predict(X)[0]
            return round(predicted_lap_time, 3)
        except Exception as e:
            print(f"Prediction error: {e}")
            # Return a default value if prediction fails.
            return 90.0
