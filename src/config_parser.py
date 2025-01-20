"""
"What is that you fear to consume you?"

Get config from file
"""
from pathlib import Path
from typing import Union
from datetime import datetime
from typing import Self

import yaml


# abstract configuration into a class
# class constructor
class Configs:
    def __init__(self, config: Union[dict, str]):
        self.raw_config = config
        self.rules = []

    def load_from_file(self) -> dict:
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
            config_element = ConfigElement(value_dict).parse()
            self.rules.append(config_element)

    def __call__(self):
        return self.rules


# abstract each config group into a class for storage
class ConfigElement:
    def __init__(self, config_dict: dict):
        self.raw_dict = config_dict
        self.program = []
        self.start_time = None
        self.end_time = None
        self.rule = None

    def parse(self) -> Self:
        for prog in self.raw_dict["program"].split(","):
            self.program.append(prog)
        self.start_time = datetime.strptime(self.raw_dict["start_time"], '%H:%M').time()
        self.end_time = datetime.strptime(self.raw_dict["end_time"], '%H:%M').time()
        self.rule = self.raw_dict["rule"] if self.raw_dict.get("rule") else "nudge"

        return self

    def __str__(self):
        return str(f"ConfigElement {self.raw_dict}")
