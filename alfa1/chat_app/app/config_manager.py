import yaml
import os


class ConfigManager:
    """
    Singleton class to manage configuration settings from config.yaml
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._config = {}
        return cls._instance

    def load_config(self, path="config.yaml"):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Configuration file not found at path: {path}")
        with open(path, 'r') as f:
            self._config = yaml.safe_load(f)

    def get(self, key, default=None):
        keys = key.split(".")
        val = self._config
        for k in keys:
            val = val.get(k, default)
            if val is None:
                return default
        return val
