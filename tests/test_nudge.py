from unittest import TestCase, main
from unittest.mock import patch, MagicMock

from src import nudge


class TestAlarm(TestCase):
    def test_init(self):
        # Case 1: default settings
        alarm = nudge.Alarm()
        self.assertEqual(alarm.cleanup, True)

        # Case 2: non-default
        alarm = nudge.Alarm(False)
        self.assertEqual(alarm.cleanup, False)

    @patch('src.nudge.tk.Tk')
    @patch('src.nudge.messagebox')
    def test_pop_msg(self, msgbox_mock, tk_mock):
        # Case 1: Cleanup is True
        tk_instance = MagicMock()
        tk_mock.return_value = tk_instance
        title = "Some title for the msgbox"
        msg = "Some message for the msgbox"

        alarm_instance = nudge.Alarm()
        alarm_instance.pop_msg(title, msg)

        tk_mock.assert_called_once()
        tk_instance.withdraw.assert_called_once()
        msgbox_mock.showinfo.assert_called_with(title, msg)
        tk_instance.destroy.assert_called_once()

        # Case 2: Cleanup is False
        tk_instance_2 = MagicMock()
        tk_mock.return_value = tk_instance_2
        title = "Some title for the msgbox"
        msg = "Some message for the msgbox"
        non_default_clenaup = False

        alarm_instance = nudge.Alarm(non_default_clenaup)
        alarm_instance.pop_msg(title, msg)

        self.assertEqual(tk_mock.call_count, 2)  # as called once for Case 1
        tk_instance_2.withdraw.assert_called_once()
        msgbox_mock.showinfo.assert_called_with(title, msg)
        tk_instance_2.destroy.assert_not_called()

    @patch('src.nudge.Alarm.pop_msg')
    def test_nudge(self, popmsg_mock):
        # Case 1: single program
        program = ["firefox"]
        start_time = "21:00"
        end_time = "08:30"
        expected_title = "A nudge from your shoulder :)"
        expected_msg_1 = f"""Hey my friend!\nI see you are using {program[0]}.""" + \
                         f"""You did not want to do this between {start_time} and {end_time}.\n""" + \
                         f"""Are you sure this is the best use of your time?"""
        alarm1 = nudge.Alarm()
        alarm1.nudge(program, start_time, end_time)
        popmsg_mock.assert_called_with(expected_title, expected_msg_1)

        # Case 2: multiple programs
        program = ["firefox", "chrome", "edge"]
        start_time = "21:00"
        end_time = "08:30"
        expected_title = "A nudge from your shoulder :)"
        expected_msg_2 = f"""Hey my friend!\nI see you are using {program[0]}, {program[1]}, {program[2]}.""" + \
                         f"""You did not want to do this between {start_time} and {end_time}.\n""" + \
                         f"""Are you sure this is the best use of your time?"""
        alarm2 = nudge.Alarm()
        alarm2.nudge(program, start_time, end_time)
        popmsg_mock.assert_called_with(expected_title, expected_msg_2)


if __name__ == '__main__':
    main()
