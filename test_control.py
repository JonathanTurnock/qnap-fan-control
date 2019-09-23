from unittest import TestCase
from unittest.mock import Mock

import control


class TestGet_system_temp(TestCase):
    def setUp(self):
        control.execute = Mock()

    def test_get_system_temp(self):
        control.execute.return_value = "27 C/81 F"
        assert control.get_system_temp() == 27

    def test_get_cpu_temp(self):
        control.execute.return_value = "54 C/129 F"
        assert control.get_cpu_temp() == 54

    def test_get_fan_count(self):
        control.execute.return_value = "4"
        assert control.get_fan_count() == 4

    def test_get_fan_rpm(self):
        control.execute.return_value = "6200 RPM"
        assert control.get_fan_rpm(1) == 6200

    def test_profile_returns_correct_mode_at_65(self):
        profile = control.Profile(40, 50, 60, 70, 75, 80, 85, 90)
        assert profile.get_fan_mode(65) == 3

    def test_profile_returns_correct_mode_at_30(self):
        profile = control.Profile(40, 50, 60, 70, 75, 80, 85, 90)
        assert profile.get_fan_mode(30) == 0

    def test_profile_returns_correct_mode_at_90(self):
        profile = control.Profile(40, 50, 60, 70, 75, 80, 85, 90)
        assert profile.get_fan_mode(90) == 7
