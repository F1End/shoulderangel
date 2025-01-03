import unittest
from src import config_parser


class TestConfigParser(unittest.TestCase):
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
        file_path1 = "\\tests\\resources\\test_config_1_simple.yaml"
        configs_instance.raw_config = file_path1
        expected = {"set1": {
            "program": "firefox",
            "start_time": 2300,
            "end_time": 900,
            "rule": "nudge"}
        }
        output = configs_instance.load_from_file()
        self.assertEqual(expected, output)

        # Case 2: Multiple simple configs
        file_path2 = "\\tests\\resources\\test_config_2_multi_simple.yaml"
        configs_instance.raw_config = file_path2
        expected = {"set1": {
            "program": "firefox",
            "start_time": 2300,
            "end_time": 900,
            "rule": "nudge"},
                    "set2": {
            "program": "chrome",
            "start_time": 2300,
            "end_time": 900,
            "rule": "nudge"},
                    "set3": {
            "program": "wow",
            "start_time": 2330,
            "end_time": 600,
            "rule": "nudge"}
        }
        output = configs_instance.load_from_file()
        self.assertEqual(expected, output)

        # Case 3: Complex config (multiple programs)
        file_path3 = "\\tests\\resources\\test_config_3_complex.yaml"
        configs_instance.raw_config = file_path3
        expected = {"set1": {
            "program": ["firefox", "chrome", "wow"],
            "start_time": 2300,
            "end_time": 900,
            "rule": "nudge"}
        }
        output = configs_instance.load_from_file()
        self.assertEqual(expected, output)

        # Case 4: Multiple complex configs, including defaulting value
        file_path4 = "\\tests\\resources\\test_config_4_multi_complex.yaml"
        configs_instance.raw_config = file_path4
        expected = {"set1": {
            "program": ["firefox", "chrome", "edge"],
            "start_time": 2300,
            "end_time": 900,
            "rule": "nudge"},
                    "set2": {
            "program": ["stellaris", "wow"],
            "start_time": 2330,
            "end_time": 600,
            "rule": "nudge"},
                    "set3": {
            "program": ["vlc", "mediamonkey"],
            "start_time": 0,
            "end_time": 600}
        }
        output = configs_instance.load_from_file()
        self.assertEqual(expected, output)

        # Case 5: Invalid file
        file_path5 = "\\tests\\resources\\test_config_5_invalid_file.yaml"
        configs_instance.raw_config = file_path5
        self.assertRaises(TypeError, configs_instance.load_from_file())

        # Case 6: Invalid path
        file_path6 = "\\tests\\resources\\test_config_nothinghere.yaml"
        configs_instance.raw_config = file_path6
        self.assertRaises(TypeError, configs_instance.load_from_file())

    def test_load_config(self):
        pass


class TestConfigElement(unittest.TestCase):
    def test_init(self):
        pass

    def test_verify_time(self):
        pass


if __name__ == '__main__':
    unittest.main()
