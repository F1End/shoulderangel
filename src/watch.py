"""
"I see thee and thy deeds..."
Module that checks whether flagged applications run at specified hour
"""
from datetime import datetime
from platform import system

import psutil

from src.config_parser import ConfigElement


class Watcher():
    def __init__(self):
        self.system = system()

    def run_checks(self, config: ConfigElement) -> list:
        if self.check_time(config):
            return self.check_running(config.program)
        else:
            return []

    def check_time(self, config: ConfigElement) -> bool:
        current_time = datetime.now().time()

        # If start and end times are identical, run check all day
        whole_day = (config.start_time == config.end_time)
        if whole_day:
            return True

        # Time comparison is different when timespan crosses midnight (00:00)
        start_and_end_same_day = config.start_time < config.end_time
        if start_and_end_same_day:
            return (config.start_time < current_time < config.end_time)
        else:
            return (current_time < config.end_time or config.start_time < current_time)

    def check_running(self, programs: list[str]) -> list:
        tested_positive = []
        all_running_programs = [process.info['name'].lower() for process in psutil.process_iter(['name'])]
        for program in programs:
            program_name = str(program.lower() + ".exe") if self.system == "Windows" else program.lower()
            if program_name in all_running_programs:
                tested_positive.append(program)
        return tested_positive
