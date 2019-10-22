from unittest import TestCase
from unittest.mock import Mock, call, patch

import control


class TestShellExecutor(TestCase):

    def test_given_hello_world_when_execute_expect_hello_world(self):
        self.assertEqual(control.execute("echo 'hello world'"), "hello world")


class TestShellParsers(TestCase):

    @patch('control.execute', Mock(return_value="27 C/81 F"))
    def test_get_system_temp(self):
        self.assertEqual(27, control.get_system_temp())

    @patch('control.execute', Mock(return_value="54 C/129 F"))
    def test_get_cpu_temp(self):
        self.assertEqual(54, control.get_cpu_temp())

    @patch('control.execute', Mock(return_value="4"))
    def test_get_fan_count(self):
        self.assertEqual(4, control.get_fan_count())

    @patch('control.execute', Mock(return_value="6200 RPM"))
    def test_get_fan_rpm(self):
        self.assertEqual(6200, control.get_fan_rpm(1))

    @patch('control.execute', Mock(return_value=""))
    def test_set_fan_profile(self):
        control.set_fan_profile(1, 1)
        control.execute.assert_called_once_with("hal_app --se_sys_set_fan_mode obj_index=0,mode=1")


class TestProfile(TestCase):

    def test_profile_returns_correct_mode_at_65(self):
        profile = control.Profile(40, 50, 60, 70, 75, 80, 85, 90)
        assert profile.get_fan_mode(65) == 3

    def test_profile_returns_correct_mode_at_30(self):
        profile = control.Profile(40, 50, 60, 70, 75, 80, 85, 90)
        assert profile.get_fan_mode(30) == 0

    def test_profile_returns_correct_mode_at_90(self):
        profile = control.Profile(40, 50, 60, 70, 75, 80, 85, 90)
        assert profile.get_fan_mode(90) == 7


class TestSetAllFansProfile(TestCase):

    @patch('control.get_fan_count', Mock(return_value=3))
    @patch('control.set_fan_profile', Mock())
    def test_given_three_fans_when_set_all_fans_profile_then_expect_three_calls_to_set_fan_profile(self):
        # When
        mock_profile = Mock()
        control.set_all_fans_profile(mock_profile)

        # Then
        expected_calls = [call(1, mock_profile), call(2, mock_profile), call(3, mock_profile)]
        control.set_fan_profile.assert_has_calls(expected_calls)


class TestGetAllFansRpm(TestCase):

    @patch('control.get_fan_count', Mock(return_value=3))
    @patch('control.get_fan_rpm', Mock(return_value=5000))
    def test_given_three_fans_when_get_all_fans_rpm_then_expect_three_rpm_values(self):
        # When
        rpms = control.get_all_fans_rpm()

        # Then
        expected_calls = [call(1), call(2), call(3)]
        control.get_fan_rpm.assert_has_calls(expected_calls)
        self.assertEqual(rpms, [5000, 5000, 5000])
