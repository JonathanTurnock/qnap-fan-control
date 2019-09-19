import configparser
import re
import subprocess


# Generic System Execution Methods
def execute(command):
    return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode()


# System Wide Metrics
def get_system_temp():
    return int(re.sub("\\sC/\\d+\\sF", "", execute("getsysinfo systmp")))


def get_cpu_temp():
    return int(re.sub("\\sC/\\d+\\sF", "", execute("getsysinfo cputmp")))


# Fan Specific Controls
def get_fan_count():
    return int(execute("getsysinfo sysfannum"))


def set_fan_profile(fan, profile):
    execute("hal_app --se_sys_set_fan_mode obj_index=%s,mode=%s" % (fan, profile))


def set_all_fans_profile(profile):
    for i in range(0, get_fan_count() - 1):
        set_fan_profile(i, profile)


class Profile:
    def __init__(self, lowest, low, medium_low, medium, medium_high, high, very_high, highest):
        self.lowest = lowest
        self.low = low
        self.medium_low = medium_low
        self.medium = medium
        self.medium_high = medium_high
        self.high = high
        self.very_high = very_high
        self.highest = highest

    def get_fan_mode(self, current_temp):
        if current_temp <= self.lowest:
            return 0
        elif current_temp <= self.low:
            return 1
        elif current_temp <= self.medium_low:
            return 2
        elif current_temp <= self.medium:
            return 3
        elif current_temp <= self.medium_high:
            return 4
        elif current_temp <= self.high:
            return 5
        elif current_temp <= self.very_high:
            return 6
        elif current_temp <= self.highest:
            return 7
        else:
            return 7


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.ini")
    profile = Profile(
        int(config["PROFILE"]["0"]),
        int(config["PROFILE"]["1"]),
        int(config["PROFILE"]["2"]),
        int(config["PROFILE"]["3"]),
        int(config["PROFILE"]["4"]),
        int(config["PROFILE"]["5"]),
        int(config["PROFILE"]["6"]),
        int(config["PROFILE"]["7"])
    )
    current_system_temp = get_system_temp()
    target_fan_profile = profile.get_fan_mode(current_system_temp)
    set_all_fans_profile(target_fan_profile)
