import configparser
import logging
import logging.config
import os
import re
import subprocess


# Generic System Execution Methods
def execute(command):
    '''
    Executes the given command on the file system and converts it to plain text
    :param command: command to be executed on the file system
    :return: The output from the command as a string
    '''
    logging.debug("Executing Command '%s'" % (command,))
    return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode().strip()


# System Wide Metrics
def get_system_temp():
    '''
    Gets the System temperature in C by executing the command 'getsysinfo systmp'
    :return: The System temp in C as an int
    '''
    logging.debug("Getting System Temperature")
    return int(re.sub("\\sC/\\d+\\sF", "", execute("getsysinfo systmp")))


def get_cpu_temp():
    '''
    Gets the CPU temperature in C by executing 'getsysinfo cputmp'
    :return: The CPU temp in C as an int
    '''
    logging.debug("Getting CPU Temperature")
    return int(re.sub("\\sC/\\d+\\sF", "", execute("getsysinfo cputmp")))


# Fan Specific Controls
def get_fan_count():
    '''
    Gets the number of fans present on the system by executing 'getsysinfo sysfannum'
    :return: The Fan count as an int
    '''
    logging.debug("Getting Fan Count")
    return int(execute("getsysinfo sysfannum"))


def get_fan_rpm(fan):
    '''
    Gets the RPM of the given fan by executing 'getsysinfo sysfan $FAN_INDEX'
    :param fan: Which fan RPM should be checked
    :return: The Fan RPM
    '''
    logging.debug("Getting Fan RPM")
    return int(re.sub("\\sRPM", "", execute("getsysinfo sysfan %s" % (fan,))))


def set_fan_profile(fan, profile):
    '''
    Sets the active fan profile on the system by executing 'hal_app --se_sys_set_fan_mode obj_index=$FAN_INDEX,mode=0-7'
    :param fan: Which fan should be changed, starting from an index of 0
    :param profile: Which profile to activated, 0 being the quietest, 7 being the loudest
    :return: N/A
    '''
    logging.debug("Setting Fan %s to Profile %s" % (fan, profile))
    execute("hal_app --se_sys_set_fan_mode obj_index=%s,mode=%s" % (fan - 1, profile))


def set_all_fans_profile(profile):
    '''
    Sets all fans on the system to the given profile
    :param profile: Which profile to activated, 0 being the quietest, 7 being the loudest
    :return: N/A
    '''
    logging.debug("Setting all fans to Profile %s" % (profile,))
    for i in range(1, get_fan_count() + 1):
        set_fan_profile(i, profile)


def get_all_fans_rpm():
    logging.debug("Getting all fans RPM")
    rpms = []
    for i in range(1, get_fan_count() + 1):
        rpms.append(get_fan_rpm(i))
    return rpms


class Profile:
    '''
    Profile represents a fan curve, the constructor takes 8 parameters which map to the
    relevant modes on the QNAP OS where 0 is the quietest and 7 is the loudest
    '''

    def __init__(self, lowest, low, medium_low, medium, medium_high, high, very_high, highest):
        '''

        :param lowest: Temp in C (as integer) at which to active profile 0
        :param low: Temp in C (as integer) at which to active profile 1
        :param medium_low: Temp in C (as integer) at which to active profile 2
        :param medium: Temp in C (as integer) at which to active profile 3
        :param medium_high: Temp in C (as integer) at which to active profile 4
        :param high: Temp in C (as integer) at which to active profile 5
        :param very_high: Temp in C (as integer) at which to active profile 6
        :param highest: Temp in C (as integer) at which to active profile 7
        '''
        self.lowest = int(lowest)
        self.low = int(low)
        self.medium_low = int(medium_low)
        self.medium = int(medium)
        self.medium_high = int(medium_high)
        self.high = int(high)
        self.very_high = int(very_high)
        self.highest = int(highest)
        logging.info("Activated Profile with thresholds: 0:%s 1:%s 2:%s 3:%s 4:%s 5:%s 6:%s 7:%s" % (
            self.lowest, self.low, self.medium_low, self.medium, self.medium_high,
            self.high, self.very_high, self.highest
        ))

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
    config.read(os.path.dirname(os.path.realpath(__file__)) + "/settings.ini")
    logging.config.fileConfig(os.path.dirname(os.path.realpath(__file__)) + "/settings.ini")
    logging.info("Starting Fan Control")
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
    try:
        current_cpu_temp = get_cpu_temp()
        logging.debug("Current CPU temp is %s" % (current_cpu_temp,))
        current_system_temp = get_system_temp()
        logging.debug("Current System temp is %s" % (current_system_temp,))
        target_fan_profile = profile.get_fan_mode(current_system_temp)
        logging.debug("Setting System Fan Profile to %s" % (target_fan_profile,))
        set_all_fans_profile(target_fan_profile)
        logging.info("CPU_TEMP:%s|SYS_TEMP:%s|PROFILE:%s" % (current_cpu_temp, current_system_temp, target_fan_profile))
        logging.info("Fan Speeds: %s" % (",".join(str(rpm) for rpm in get_all_fans_rpm()),))
    except Exception as e:
        logging.error("An Exception occurred while setting the profile, activating profile 7!")
        logging.error(e)
        set_all_fans_profile(7)
