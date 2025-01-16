from unittest import TestCase, main
from unittest.mock import patch

from src import nudge


class MyTestCase(TestCase):
    @patch('src.nudge.ctypes.windll.user32.MessageBoxW')
    def test_nudge(self, msgbox_mock):
        # Case 1: single program
        program = ["firefox"]
        start_time = "21:00"
        end_time = "08:30"
        expected_title = "A nudge from your shoulder :)"
        expected_msg = f"""Hey my friend!\nI see you are using {program[0]}.""" + \
                       f"""You did not want to do this between {start_time} and {end_time}.\n""" + \
                       f"""Are you sure this is the best use of your time?"""
        nudge.Alarm.nudge(program, start_time, end_time)
        msgbox_mock.assert_called_with(0, expected_msg, expected_title, 0)

        # Case 2: multiple programs
        program = ["firefox", "chrome", "edge"]
        start_time = "21:00"
        end_time = "08:30"
        expected_title = "A nudge from your shoulder :)"
        expected_msg = f"""Hey my friend!\nI see you are using {program[0]}, {program[1]}, {program[2]}.""" + \
                       f"""You did not want to do this between {start_time} and {end_time}.\n""" + \
                       f"""Are you sure this is the best use of your time?"""
        nudge.Alarm.nudge(program, start_time, end_time)
        msgbox_mock.assert_called_with(0, expected_msg, expected_title, 0)


if __name__ == '__main__':
    main()
