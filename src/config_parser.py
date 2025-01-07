"""
"What is that you fear to consume you?"

Get config from file
"""
from pathlib import Path
from typing import Union
from datetime import datetime

import yaml


# abstract configuration into a class
# class constructor
class Configs:
    def __init__(self, config: Union[dict, str]):
        self.raw_config = config
        self.configs = []

    def load_from_file(self):
        path = Path(self.raw_config)
        with open(path, 'r') as file:
            config_from_file = yaml.safe_load(file)
            return config_from_file

    # method to parse yaml file OR dict to class config
    def load_config(self):
        if isinstance(self.raw_config, str):
            config_dict = self.load_from_file()
        else:
            config_dict = self.raw_config.copy()
        for key, value_dict in config_dict.items():
            self.configs.append(ConfigElement(value_dict).parse())


# abstract each config group into a class for storage
class ConfigElement:
    def __init__(self, config_dict: dict):
        self.raw_dict = config_dict
        self.program = []
        self.start_time = None
        self.end_time = None
        self.rule = None

    def parse(self):
        for prog in self.raw_dict["program"].split(","):
            self.program.append(prog)
        self.start_time = datetime.strptime(self.raw_dict["start_time"], '%H:%M').time()
        self.end_time = datetime.strptime(self.raw_dict["end_time"], '%H:%M').time()
        self.rule = self.raw_dict["rule"] if self.raw_dict.get("rule") else "nudge"
