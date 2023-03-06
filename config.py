import json
import logging
import requests

class Configuration:
    def __init__(self, config_file):
        self.logger = logging.getLogger(__name__)
        self.config_data = None
        if config_file.startswith('http://') or config_file.startswith('https://'):
            try:
                r = requests.get(config_file)
                self.config_data = r.json()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to load configuration file from URL '{config_file}':\n{e}")
                return
            except json.JSONDecodeError as e:
                self.logger.error(f"Configuration data from URL '{config_file}' contains invalid JSON syntax:\n{e}")
                return
        else:
            try:
                with open(config_file, 'r') as f:
                    self.config_data = json.load(f)
            except FileNotFoundError:
                self.logger.error(f"Configuration file '{config_file}' not found.")
                return
            except json.JSONDecodeError as e:
                self.logger.error(f"Configuration file '{config_file}' contains invalid JSON syntax:\n{e}")
                return
            except Exception as e:
                self.logger.error(f"Failed to load configuration file '{config_file}':\n{e}")
                return

        def dict_to_obj(data):
            if isinstance(data, dict):
                return type('ConfigObject', (), {k: dict_to_obj(v) for k, v in data.items()})
            elif isinstance(data, list):
                return [dict_to_obj(v) for v in data]
            else:
                return data

        try:
            config_obj = dict_to_obj(self.config_data)
            self.__dict__.update(config_obj.__dict__)
        except Exception as e:
            self.logger.error(f"Failed to parse configuration data:\n{e}")
            return

    def get_config_as_dict(self):
        return self.config_data

config_file = 'config.json'
config = Configuration(config_file=config_file)
