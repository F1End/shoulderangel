"""
"An angel perched upon your shoulder, urging you to know when it's time to stop."

This module connects the other elements to orchestrate the process.
1. Load config (when you should not use which applications?)
2. Check if any runs at specified config times
3. Runs alarm if #2 returns something.

This module should be fully independent of OS.
"""
from argparse import ArgumentParser
from time import sleep

from src import config_parser, nudge, watch

# Abstratct all into a central class
class Angel:

    def __init__(self, args: ArgumentParser):
        self.config_path = args.config_path
        self.run_rule = args.run_rule
        self.check_interval = args.check_interval

        self.alarm = nudge.Alarm()
        self.watcher = watch.Watcher()
        self.configs = config_parser.Configs(self.config_path)

    def check_element(self, element: config_parser.ConfigElement):
        return self.watcher.run_checks(element)

    def run_config_checks(self) -> list[tuple[list, config_parser.ConfigElement]]:
        outcome = []
        for element in self.configs():
            positive = self.check_element(element)
            if positive:
                outcome.append((positive, element))
        return outcome

    def alarm_action(self, positives: list, element: config_parser.ConfigElement):
        self.alarm.nudge(positives, element.start_time, element.end_time)

    # Will allow more complex options for deciding runtime length
    def check_run_rules(self) -> bool:
        if self.run_rule == "single":
            return False
        if self.run_rule == "loop":
            return True

    def check_and_action(self):
        positive_check_outcomes = self.run_config_checks()
        if positive_check_outcomes:
            for actionable in positive_check_outcomes:
                self.alarm_action(actionable[0],
                                  actionable[1].start_time,
                                  actionable[1].end_time)

    def run(self):
        keep_running = True
        while keep_running:
            self.check_and_action()

            sleep(self.check_interval * 60)
            keep_running = self.check_run_rules()
