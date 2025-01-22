from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from datetime import datetime
from platform import system

from src import watch


class TestWatch(TestCase):

    @patch('src.watch.system')
    def test_watcher_init(self, system_mock):
        test_instance = watch.Watcher()
        system_mock.assert_called_once()

    @patch('src.watch.Watcher.check_time')
    @patch('src.watch.Watcher.check_running')
    def test_run_checks(self, running_mock, time_mock):
        test_instance = watch.Watcher()

        # Case 1: check time returns True
        config_mock_1 = MagicMock()
        time_mock.return_value = True

        _ = test_instance.run_checks(config_mock_1)
        time_mock.assert_called_with(config_mock_1)
        running_mock.assert_called_once()

        # Case 2: check time returns False
        config_mock_2 = MagicMock()
        time_mock.return_value = False

        _ = test_instance.run_checks(config_mock_2)
        time_mock.assert_called_with(config_mock_2)
        running_mock.assert_called_once()

    @patch('src.watch.datetime')
    def test_check_time(self, datetime_mock):
        initiated_watcher = watch.Watcher()

        # Case 1: Start and end time on same day, True
        start_time_1 = datetime.strptime("11:00", '%H:%M').time()
        end_time_1 = datetime.strptime("17:00", '%H:%M').time()

        configmock_1 = MagicMock()
        configmock_1.start_time = start_time_1
        configmock_1.end_time = end_time_1

        current_time_1 = datetime.strptime("13:35", '%H:%M').time()
        datetime_mock.now().time.return_value = current_time_1
        expected_1 = True

        checked_1 = initiated_watcher.check_time(configmock_1)
        self.assertEqual(expected_1, checked_1)

        # Case 2: Start and end time on same day, False
        start_time_2 = datetime.strptime("11:00", '%H:%M').time()
        end_time_2 = datetime.strptime("17:00", '%H:%M').time()

        configmock_2 = MagicMock()
        configmock_2.start_time = start_time_2
        configmock_2.end_time = end_time_2

        current_time_2 = datetime.strptime("18:35", '%H:%M').time()
        datetime_mock.now().time.return_value = current_time_2
        expected_2 = False

        checked_2 = initiated_watcher.check_time(configmock_2)
        self.assertEqual(expected_2, checked_2)

        # Case 3: End time slides to next day, True, now() before midnight
        start_time_3 = datetime.strptime("19:00", '%H:%M').time()
        end_time_3 = datetime.strptime("07:00", '%H:%M').time()

        configmock_3 = MagicMock()
        configmock_3.start_time = start_time_3
        configmock_3.end_time = end_time_3

        current_time_3 = datetime.strptime("21:35", '%H:%M').time()
        datetime_mock.now().time.return_value = current_time_3
        expected_3 = True

        checked_3 = initiated_watcher.check_time(configmock_3)
        self.assertEqual(expected_3, checked_3)

        # Case 4: End time slides to next day, True, now() after midnight
        start_time_4 = datetime.strptime("19:00", '%H:%M').time()
        end_time_4 = datetime.strptime("07:00", '%H:%M').time()

        configmock_4 = MagicMock()
        configmock_4.start_time = start_time_4
        configmock_4.end_time = end_time_4

        current_time_4 = datetime.strptime("06:35", '%H:%M').time()
        datetime_mock.now().time.return_value = current_time_4
        expected_4 = True

        checked_4 = initiated_watcher.check_time(configmock_4)
        self.assertEqual(expected_4, checked_4)

        # Case 5: End time slides to next day, False
        start_time_5 = datetime.strptime("19:00", '%H:%M').time()
        end_time_5 = datetime.strptime("07:00", '%H:%M').time()

        configmock_5 = MagicMock()
        configmock_5.start_time = start_time_5
        configmock_5.end_time = end_time_5

        current_time_5 = datetime.strptime("09:35", '%H:%M').time()
        datetime_mock.now().time.return_value = current_time_5
        expected_5 = False

        checked_5 = initiated_watcher.check_time(configmock_5)
        self.assertEqual(expected_5, checked_5)

    @patch('src.watch.psutil')
    def test_check_running(self, psutil_mock):
        # setup
        test_instance = watch.Watcher()
        windows_extension = ".exe" if system() == "Windows" else ""

        # Case 1: single program, running
        programs_1 = ["firefox"]
        running_1 = [f"firefox{windows_extension}", f"unsecapp{windows_extension}",
                     f"NisSrv{windows_extension}", f"svchost{windows_extension}",
                     f"aw-qt{windows_extension}", f"HotkeyMonitor{windows_extension}"]
        expected_1 = ["firefox"]
        running_mocks_1 = []
        for name in running_1:
            mock = MagicMock()
            mock.info = {'name': name}
            running_mocks_1.append(mock)
        psutil_mock.process_iter.return_value = running_mocks_1
        found_1 = test_instance.check_running(programs_1)
        self.assertEqual(found_1, expected_1)

        # Case 2: single program, not running
        programs_2 = ["firefox"]
        running_2 = [f"unsecapp{windows_extension}",
                     f"NisSrv{windows_extension}", f"svchost{windows_extension}",
                     f"aw-qt{windows_extension}", f"HotkeyMonitor{windows_extension}"]
        expected_2 = []
        running_mocks_2 = []
        for name in running_2:
            mock = MagicMock()
            mock.info = {'name': name}
            running_mocks_2.append(mock)
        psutil_mock.process_iter.return_value = running_mocks_2
        found_2 = test_instance.check_running(programs_2)
        self.assertEqual(found_2, expected_2)

        # Case 3: multiple programs, all running
        programs_3 = ["firefox", "chrome", "spotify"]
        running_3 = [f"firefox{windows_extension}", f"unsecapp{windows_extension}",
                     f"NisSrv{windows_extension}", f"svchost{windows_extension}",
                     f"aw-qt{windows_extension}", f"HotkeyMonitor{windows_extension}",
                     f"Spotify{windows_extension}", f"chrome{windows_extension}"]
        expected_3 = ["firefox", "chrome", "spotify"]
        running_mocks_3 = []
        for name in running_3:
            mock = MagicMock()
            mock.info = {'name': name}
            running_mocks_3.append(mock)
        psutil_mock.process_iter.return_value = running_mocks_3
        found_3 = test_instance.check_running(programs_3)
        self.assertEqual(found_3, expected_3)

        # Case 4: multiple programs, some running, uppercase val included
        programs_4 = ["firefox", "cHrome", "spotify"]
        running_4 = [f"firefox{windows_extension}", f"unsecapp{windows_extension}",
                     f"NisSrv{windows_extension}", f"svchost{windows_extension}",
                     f"aw-qt{windows_extension}", f"HotkeyMonitor{windows_extension}",
                     f"Spotify{windows_extension}"]
        expected_4 = ["firefox", "spotify"]
        running_mocks_4 = []
        for name in running_4:
            mock = MagicMock()
            mock.info = {'name': name}
            running_mocks_4.append(mock)
        psutil_mock.process_iter.return_value = running_mocks_4
        found_4 = test_instance.check_running(programs_4)
        self.assertEqual(found_4, expected_4)

        # Case 5: multiple programs, one running
        programs_5 = ["firefox", "chrome", "spotify"]
        running_5 = [f"firefox{windows_extension}", f"unsecapp{windows_extension}",
                     f"NisSrv{windows_extension}", f"svchost{windows_extension}",
                     f"aw-qt{windows_extension}", f"HotkeyMonitor{windows_extension}"]
        expected_5 = ["firefox"]
        running_mocks_5 = []
        for name in running_5:
            mock = MagicMock()
            mock.info = {'name': name}
            running_mocks_5.append(mock)
        psutil_mock.process_iter.return_value = running_mocks_5
        found_5 = test_instance.check_running(programs_5)
        self.assertEqual(found_5, expected_5)

        # Case 6: multiple programs, none running
        programs_6 = ["firefox", "chrome", "spotify"]
        running_6 = [f"unsecapp{windows_extension}",
                     f"NisSrv{windows_extension}", f"svchost{windows_extension}",
                     f"aw-qt{windows_extension}", f"HotkeyMonitor{windows_extension}"]
        expected_6 = []
        running_mocks_6 = []
        for name in running_6:
            mock = MagicMock()
            mock.info = {'name': name}
            running_mocks_6.append(mock)
        psutil_mock.process_iter.return_value = running_mocks_6
        found_6 = test_instance.check_running(programs_6)
        self.assertEqual(found_6, expected_6)


if __name__ == '__main__':
    main()
