import logging
from unittest import TestCase, main
from unittest.mock import patch, MagicMock, call

from src import angel


class TestAngel(TestCase):

    @patch('src.nudge.Alarm')
    @patch('src.watch.Watcher')
    @patch('src.config_parser.Configs')
    def setUp(self, configs_mock, watcher_mock, alarm_mock):
        argpars_mock = MagicMock
        test_path = "some/file/path"
        test_rule = "single"
        test_interval = 5
        argpars_mock.config_path = test_path
        argpars_mock.run_rule = test_rule
        argpars_mock.check_interval = test_interval
        argpars_mock.debug = False

        self.test_angel = angel.Angel(argpars_mock)

    @patch('src.angel.logger')
    @patch('src.nudge.Alarm')
    @patch('src.watch.Watcher')
    @patch('src.config_parser.Configs')
    def test_init(self, configs_mock, watcher_mock, alarm_mock, logger_mock):
        # Case 1: Debug False (default)
        argpars_mock = MagicMock
        test_path = "some/file/path"
        test_rule = "loop"
        test_interval = 15
        argpars_mock.config_path =test_path
        argpars_mock.run_rule = test_rule
        argpars_mock.check_interval = test_interval
        argpars_mock.debug = False

        configs_return = "fake_configs_instance"
        configs_mock.return_value = configs_return
        watcher_return = "fake_watcher_instance"
        watcher_mock.return_value = watcher_return
        alarm_return = "fake_alarm_instance"
        alarm_mock.return_value = alarm_return

        init_test_angel = angel.Angel(argpars_mock)

        self.assertEqual(init_test_angel.config_path, test_path)
        self.assertEqual(init_test_angel.run_rule, test_rule)
        self.assertEqual(init_test_angel.check_interval, test_interval)
        self.assertEqual(init_test_angel.configs, configs_return)
        self.assertEqual(init_test_angel.watcher, watcher_return)
        self.assertEqual(init_test_angel.alarm, alarm_return)

        logger_mock.assert_not_called()
        configs_mock.assert_called_with(test_path)
        watcher_mock.assert_called_once()
        alarm_mock.assert_called_once()

        # Case 2: Debug
        argpars_mock = MagicMock
        test_path = "some/file/path"
        test_rule = "loop"
        test_interval = 15
        argpars_mock.config_path =test_path
        argpars_mock.run_rule = test_rule
        argpars_mock.check_interval = test_interval
        argpars_mock.debug = True

        configs_return = "fake_configs_instance"
        configs_mock.return_value = configs_return
        watcher_return = "fake_watcher_instance"
        watcher_mock.return_value = watcher_return
        alarm_return = "fake_alarm_instance"
        alarm_mock.return_value = alarm_return

        init_test_angel = angel.Angel(argpars_mock)

        self.assertEqual(init_test_angel.config_path, test_path)
        self.assertEqual(init_test_angel.run_rule, test_rule)
        self.assertEqual(init_test_angel.check_interval, test_interval)
        self.assertEqual(init_test_angel.configs, configs_return)
        self.assertEqual(init_test_angel.watcher, watcher_return)
        self.assertEqual(init_test_angel.alarm, alarm_return)

        logger_mock.setLevel.assert_called_with(logging.DEBUG)
        configs_mock.assert_called_with(test_path)
        self.assertEqual(watcher_mock.call_count, 2)
        self.assertEqual(alarm_mock.call_count, 2)

    def test_check_element(self):
        # Case 1: returns a single running progrem
        fake_element_1 = "fake_config_element_1"
        program_running_1 = ["firefox"]
        self.test_angel.watcher.run_checks.return_value = program_running_1
        results_1 = self.test_angel.check_element(fake_element_1)
        self.test_angel.watcher.run_checks.assert_called_with(fake_element_1)
        self.assertEqual(results_1, program_running_1)

        # Case 2: returns multiple running programs
        fake_element_2 = "fake_config_element_2"
        program_running_2 = ["firefox", "Spotify"]
        self.test_angel.watcher.run_checks.return_value = program_running_2
        results_2 = self.test_angel.check_element(fake_element_2)
        self.test_angel.watcher.run_checks.assert_called_with(fake_element_2)
        self.assertEqual(results_2, program_running_2)

        # Case 3: returns nothing
        fake_element_3 = "fake_config_element_3"
        program_running_3 = []
        self.test_angel.watcher.run_checks.return_value = program_running_3
        results_3 = self.test_angel.check_element(fake_element_3)
        self.test_angel.watcher.run_checks.assert_called_with(fake_element_3)
        self.assertEqual(results_3, program_running_3)

    def test_run_config_checks(self):
        checks = ["fake_cf_element_1", "fake_cf_element_2", "fake_cf_element_3"]
        self.test_angel.configs.return_value = checks

        # Case 1: Nothing is running
        with patch.object(self.test_angel, 'check_element') as mock_check_element:
            mock_check_element.return_value = []
            output = self.test_angel.run_config_checks()

            mock_check_element.assert_any_call(checks[0])
            mock_check_element.assert_any_call(checks[1])
            mock_check_element.assert_any_call(checks[2])

            self.assertEqual(output,[])

        # Case 2: One program is running
        with patch.object(self.test_angel, 'check_element') as mock_check_element:
            mock_check_element.side_effect = [[], ["firefox"], []]
            output_2 = self.test_angel.run_config_checks()

            mock_check_element.assert_any_call(checks[0])
            mock_check_element.assert_any_call(checks[1])
            mock_check_element.assert_any_call(checks[2])

            self.assertEqual(output_2, [(["firefox"], "fake_cf_element_2")])

        # Case 3: Multiple programs running
        with patch.object(self.test_angel, 'check_element') as mock_check_element:
            mock_check_element.side_effect = [[], ["firefox", "Chrome"], ["stellaris"]]
            output_2 = self.test_angel.run_config_checks()

            mock_check_element.assert_any_call(checks[0])
            mock_check_element.assert_any_call(checks[1])
            mock_check_element.assert_any_call(checks[2])

            self.assertEqual(output_2, [(["firefox", "Chrome"], "fake_cf_element_2"),
                                        (["stellaris"], "fake_cf_element_3")])

    def test_alarm_action(self):
        mock_element = MagicMock
        start_time = "21:00"
        end_time = "08:30"
        positives = ["firefox", "Chrome"]
        mock_element.start_time = start_time
        mock_element.end_time = end_time

        self.test_angel.alarm_action(positives, mock_element)
        self.test_angel.alarm.nudge.assert_called_with(positives, start_time, end_time)

    def test_check_run_rules(self):
        # Case 1: single run only
        self.test_angel.run_rule = "single"
        expected_value = False

        continue_loop = self.test_angel.check_run_rules()
        self.assertEqual(expected_value, continue_loop)

        # Case 2: keep looping
        self.test_angel.run_rule = "loop"
        expected_value = True

        continue_loop = self.test_angel.check_run_rules()
        self.assertEqual(expected_value, continue_loop)

    def test_check_and_action(self):
        # Case 1: no positive checks
        with patch.object(self.test_angel, 'run_config_checks') as config_checks_mock:
            config_checks_mock.return_value = []

            with patch.object(self.test_angel, 'alarm_action') as alarm_action_mock:
                self.test_angel.check_and_action()
                config_checks_mock.assert_called_once()
                alarm_action_mock.assert_not_called()

        # Case 2: one positive check
        with patch.object(self.test_angel, 'run_config_checks') as config_checks_mock:
            config_mock = MagicMock()
            start_time = "21:30"
            end_time = "09:00"
            config_mock.start_time = start_time
            config_mock.end_time = end_time
            config_checks_mock.return_value = [(["firefox"], config_mock)]

            with patch.object(self.test_angel, 'alarm_action') as alarm_action_mock:
                self.test_angel.check_and_action()
                config_checks_mock.assert_called_once()
                alarm_action_mock.assert_called_with(["firefox"], config_mock)

        # Case 3: multiple positive checks
        with patch.object(self.test_angel, 'run_config_checks') as config_checks_mock:
            config_mock = MagicMock()
            start_time = "21:30"
            end_time = "09:00"
            config_mock.start_time = start_time
            config_mock.end_time = end_time
            config_mock_2 = MagicMock()
            start_time_2 = "20:30"
            end_time_2 = "06:00"
            config_mock_2.start_time = start_time_2
            config_mock_2.end_time = end_time_2
            config_checks_mock.return_value = [(["firefox"], config_mock),
                                               (["Edge", "Spotify"], config_mock_2)]

            with patch.object(self.test_angel, 'alarm_action') as alarm_action_mock:
                self.test_angel.check_and_action()
                config_checks_mock.assert_called_once()
                alarm_action_mock.assert_any_call(["firefox"], config_mock)
                alarm_action_mock.assert_any_call(["Edge", "Spotify"], config_mock_2)

    @patch('src.angel.sleep')
    def test_run(self, mock_sleep):
        # Case 1: Single run
        with patch.object(self.test_angel, 'check_and_action') as check_and_action_mock:
            with patch.object(self.test_angel, 'check_run_rules') as check_run_rules_mock:
                check_run_rules_mock.return_value = False

                self.test_angel.run()
                mock_sleep.assert_not_called()
                check_and_action_mock.assert_called_once()
                check_run_rules_mock.assert_called_once()

        # Case 2: Looping
        expected_sleep_length = self.test_angel.check_interval * 60 # default is 5 * 60 -> 300
        with patch.object(self.test_angel, 'check_and_action') as check_and_action_mock:
            with patch.object(self.test_angel, 'check_run_rules') as check_run_rules_mock:
                # Modelling 5 reruns -> Run six times total
                check_run_rules_mock.side_effect = [True, True, True, True, True, False]

                self.test_angel.run()
                mock_sleep.assert_called_with(expected_sleep_length)
                self.assertEqual(mock_sleep.call_count, 5)
                self.assertEqual(check_and_action_mock.call_count, 6)
                self.assertEqual(check_run_rules_mock.call_count, 6)


if __name__ == '__main__':
    main()
