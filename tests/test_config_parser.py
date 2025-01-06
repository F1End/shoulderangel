from unittest import TestCase, main
from unittest.mock import MagicMock,patch

from yaml import parser

from src import config_parser




class TestConfigParser(TestCase):
    def test_init(self):
        # Case 1: Configs is called with path input
        input_path = "some/path/to/config.yaml"
        test_configs = config_parser.Configs(input_path)
        default_configs = []
        self.assertEqual(test_configs.raw_config, input_path)
        self.assertEqual(test_configs.configs, default_configs)

        # Case 2: Configs is called with dict input
        input_dict = {"program": "firefox", "start_time": "2200", "end_time": "0800", "rule": "Nudge"}
        test_configs2 = config_parser.Configs(input_dict)
        default_configs
        self.assertEqual(test_configs2.raw_config, input_dict)
        self.assertEqual(test_configs2.configs, default_configs)

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
        configs_instance.load_config()
        load_file_mock.assert_called_once()
        for key, config_value_dict in mock_yaml_parsed.items():
            configelement_mock.assert_called_with(config_value_dict)

        # Case 2: dict passed
        input2 = {"set1": {
            "program": "firefox",
            "start_time": "23:00",
            "end_time": "09:00",
            "rule": "nudge"}}
        configs_instance.raw_config = input2
        configs_instance.load_config()
        load_file_mock.assert_called_once()


class TestConfigElement(TestCase):
    def test_init(self):
        pass

    def test_verify_time(self):
        pass


if __name__ == '__main__':
    main()
