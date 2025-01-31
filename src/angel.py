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
import logging

from src import config_parser, nudge, watch

logger = logging.getLogger("angel")
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


class Angel:
    def __init__(self, args: ArgumentParser):
        self.config_path = args.config_path
        self.run_rule = args.run_rule
        self.check_interval = args.check_interval
        self.debug = args.debug

        self.alarm = nudge.Alarm(cleanup=False)
        self.watcher = watch.Watcher()
        self.configs = config_parser.Configs(self.config_path)

        if self.debug:
            logger.setLevel(logging.DEBUG)

    def check_element(self, element: config_parser.ConfigElement):
        return self.watcher.run_checks(element)

    def run_config_checks(self) -> list[tuple[list, config_parser.ConfigElement]]:
        outcome = []
        for element in self.configs():
            logger.debug(f"Running checks on {element}")
            positive = self.check_element(element)
            if positive:
                outcome.append((positive, element))
        return outcome

    def alarm_action(self, positives: list, element: config_parser.ConfigElement):
        logger.info(f"Triggering alarm for {positives}")
        self.alarm.nudge(positives, element.start_time, element.end_time)

    # Will allow more complex options for deciding runtime length
    def check_run_rules(self) -> bool:
        if self.run_rule == "single":
            return False
        if self.run_rule == "loop":
            return True

    def check_and_action(self):
        logger.info("Running checks...")
        positive_check_outcomes = self.run_config_checks()
        if positive_check_outcomes:
            for actionable in positive_check_outcomes:
                self.alarm_action(actionable[0],
                                  actionable[1])
        logger.debug("Checks completed")

    def run(self):
        self.configs.load_config()

        keep_running = True
        while keep_running:
            self.check_and_action()

            keep_running = self.check_run_rules()
            if keep_running:
                sleep_seconds = self.check_interval * 60
                logger.info(f"Sleeping for {sleep_seconds} seconds...")
                sleep(sleep_seconds)
