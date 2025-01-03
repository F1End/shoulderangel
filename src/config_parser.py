"""
"What is that you fear to consume you?"

Get config from file
"""
from typing import Union
import yaml


# abstract configuration into a class
# class constructor
class Configs:
    def __init__(self, config: Union[dict, str]):
        self.raw_config = config
        self.configs = []

    def load_from_file(self):
        raise NotImplemented

# method to parse yaml file OR dict to class config
    def load_config(self):
        raise NotImplemented

# abstract each config group into a class for storage
class ConfigElement:
    def __init__(self, program: str, start_time, end_time, rule: str = "nudge"):
        self.program = program
        self.start_time = start_time if self._verify_time(start_time)\
            else Exception(f"Invalid start time: '{start_time}' for program(s) {program}")
        self.end_time = end_time if self._verify_time(end_time)\
            else Exception(f"Invalid end time: '{end_time}' for program(s) {program}")
        self.rule = rule

    @staticmethod
    def _verify_time(time: int) -> bool:
        """
        Making sure that time is convertible to datetime,
        to raise exception during loading bad config,
        not when it gets called downstream
        :return: bool
        """
        pass
