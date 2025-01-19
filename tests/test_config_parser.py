from unittest import TestCase, main
from unittest.mock import patch
from datetime import datetime

from yaml import parser

from src import config_parser


class TestConfigParser(TestCase):
    def test_init(self):
        # Case 1: Configs is called with path input
        input_path = "some/path/to/config.yaml"
        test_configs = config_parser.Configs(input_path)
        default_configs = []
        self.assertEqual(test_configs.raw_config, input_path)
        self.assertEqual(test_configs.rules, default_configs)

        # Case 2: Configs is called with dict input
        input_dict = {"program": "firefox", "start_time": "2200", "end_time": "0800", "rule": "Nudge"}
        test_configs2 = config_parser.Configs(input_dict)
        default_configs
        self.assertEqual(test_configs2.raw_config, input_dict)
        self.assertEqual(test_configs2.rules, default_configs)

        # Case 3: Called without input and fails
        self.assertRaises(TypeError, config_parser.Configs)

    def test_load_from_file(self):
        # Creating instance
        configs_instance = config_parser.Configs("Some-path")

        # Case 1: Simple config of one program
        file_path1 = "resources/test_config_1_simple.yaml"
        configs_instance.raw_config = file_path1
        expected = {"set1": {
            "program": "firefox",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"}
        }
        output = configs_instance.load_from_file()
        self.assertEqual(expected, output)

        # Case 2: Multiple simple configs
        file_path2 = "resources\\test_config_2_multi_simple.yaml"
        configs_instance.raw_config = file_path2
        expected = {"set1": {
            "program": "firefox",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"},
                    "set2": {
            "program": "chrome",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"},
                    "set3": {
            "program": "wow",
            "start_time": "23:30",
            "end_time": "06:00",
            "rule": "nudge"}
        }
        output = configs_instance.load_from_file()
        self.assertEqual(expected, output)

        # Case 3: Complex config (multiple programs)
        file_path3 = "resources/test_config_3_complex.yaml"
        configs_instance.raw_config = file_path3
        expected = {"set1": {
            "program": "firefox,chrome,wow",
            "start_time": "23:00",
            "end_time": "09:00"}
        }
        output = configs_instance.load_from_file()
        self.assertEqual(expected, output)

        # Case 4: Multiple complex configs, including defaulting value
        file_path4 = "resources/test_config_4_multi_complex.yaml"
        configs_instance.raw_config = file_path4
        expected = {"set1": {
            "program": "firefox,chrome,edge",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"},
                    "set2": {
            "program": "stellaris,wow",
            "start_time": "23:30",
            "end_time": "06:00",
            "rule": "nudge"},
                    "set3": {
            "program": "vlc,mediamonkey",
            "start_time": "00:00",
            "end_time": "06:00"}
        }
        output = configs_instance.load_from_file()
        self.assertEqual(expected, output)

        # Case 5: Invalid file
        file_path5 = "resources/test_config_5_invalid_file.yaml"
        configs_instance.raw_config = file_path5
        with self.assertRaises(parser.ParserError):
            configs_instance.load_from_file()

        # Case 6: Invalid path
        file_path6 = "resources/test_config_nothinghere.yaml"
        configs_instance.raw_config = file_path6
        with self.assertRaises(FileNotFoundError):
            configs_instance.load_from_file()

    @patch('src.config_parser.ConfigElement')
    @patch('src.config_parser.Configs.load_from_file')
    def test_load_config(self, load_file_mock, configelement_mock):
        # Creating instance
        configs_instance = config_parser.Configs("Some-path")

        # Case 1: File path passed (as str)
        input1 = 'some_file_path_string'
        configs_instance.raw_config = input1
        mock_yaml_parsed = {"set1": {
            "program": "firefox,chrome,edge",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"},
                    "set2": {
            "program": "stellaris,wow",
            "start_time": "23:30",
            "end_time": "06:00",
            "rule": "nudge"},
                    "set3": {
            "program": "vlc,mediamonkey",
            "start_time": "00:00",
            "end_time": "06:00"}
        }
        load_file_mock.return_value = mock_yaml_parsed

        # call for case 1
        configs_instance.load_config()

        load_file_mock.assert_called_once()
        for key, config_value_dict in mock_yaml_parsed.items():
            configelement_mock.assert_any_call(config_value_dict)
        configelement_mock.parse.call_count == 3

        # Case 2: dict passed
        input2 = {"set1": {
            "program": "firefox",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"}}
        configs_instance.raw_config = input2

        # call for case 2
        configs_instance.load_config()

        load_file_mock.assert_called_once()
        configelement_mock.assert_called_with(input2["set1"])

    def test__call__(self):
        input_path = "some/path/to/config.yaml"
        test_ruleset = [{"set1": {
            "program": "firefox",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"}}]
        expected = test_ruleset

        test_configs = config_parser.Configs(input_path)
        test_configs.rules = test_ruleset
        called = test_configs()
        self.assertEqual(called, expected)



class TestConfigElement(TestCase):
    def test_init(self):
        input_dict = {
            "program": "firefox",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"}
        expected_program = []
        expected_start, expected_end, expected_rule = None, None, None

        test_element = config_parser.ConfigElement(input_dict)
        self.assertEqual(test_element.raw_dict, input_dict)
        self.assertEqual(test_element.program, expected_program)
        self.assertEqual(test_element.start_time, expected_start)
        self.assertEqual(test_element.end_time, expected_end)
        self.assertEqual(test_element.rule, expected_rule)

    def test_parse(self):
        # Case 1: Single program entered
        input_dict_1 = {
            "program": "firefox",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"}
        expected_program_1 = ["firefox"]
        expected_start_1 = datetime.strptime(input_dict_1["start_time"], '%H:%M').time()
        expected_end_1 = datetime.strptime(input_dict_1["end_time"], '%H:%M').time()
        expected_rule_1 = input_dict_1["rule"]

        test_element_1 = config_parser.ConfigElement(input_dict_1)
        test_element_1.parse()

        self.assertEqual(test_element_1.raw_dict, input_dict_1)
        self.assertEqual(test_element_1.program, expected_program_1)
        self.assertEqual(test_element_1.start_time, expected_start_1)
        self.assertEqual(test_element_1.end_time, expected_end_1)
        self.assertEqual(test_element_1.rule, expected_rule_1)

        # Case 2: Multiple programs
        input_dict_2 = {
            "program": "firefox,chrome,edge",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"}
        expected_program_2 = ["firefox", "chrome", "edge"]
        expected_start_2 = datetime.strptime(input_dict_2["start_time"], '%H:%M').time()
        expected_end_2 = datetime.strptime(input_dict_2["end_time"], '%H:%M').time()
        expected_rule_2 = input_dict_2["rule"]

        test_element_2 = config_parser.ConfigElement(input_dict_2)
        test_element_2.parse()

        self.assertEqual(test_element_2.raw_dict, input_dict_2)
        self.assertEqual(test_element_2.program, expected_program_2)
        self.assertEqual(test_element_2.start_time, expected_start_2)
        self.assertEqual(test_element_2.end_time, expected_end_2)
        self.assertEqual(test_element_2.rule, expected_rule_2)

        # Case 3: Rule is not entered -> default to "nudge"
        input_dict_3 = {
            "program": "firefox",
            "start_time": "23:00",
            "end_time": "09:00"}
        expected_program_3 = ["firefox"]
        expected_start_3 = datetime.strptime(input_dict_3["start_time"], '%H:%M').time()
        expected_end_3 = datetime.strptime(input_dict_3["end_time"], '%H:%M').time()
        expected_rule_3 = "nudge"

        test_element_3 = config_parser.ConfigElement(input_dict_3)
        test_element_3.parse()

        self.assertEqual(test_element_3.raw_dict, input_dict_3)
        self.assertEqual(test_element_3.program, expected_program_3)
        self.assertEqual(test_element_3.start_time, expected_start_3)
        self.assertEqual(test_element_3.end_time, expected_end_3)
        self.assertEqual(test_element_3.rule, expected_rule_3)


if __name__ == '__main__':
    main()
