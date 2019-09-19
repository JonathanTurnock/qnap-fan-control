# System Commands
## Overall System Temperature
Gets the Overall System Temperature measurement
```
getsysinfo systmp
```
Returns
```
27 C/81 F
```
## Overall CPU Temperature
Gets the overall CPU temperature measurement
```
getsysinfo cputmp
```
Returns
```
27 C/81 F
```

# Fan Commands
## Get Number of Fans
Gets the number of Fans installed in the system
```
getsysinfo sysfannum
```

## Get Fan Speed
Gets the Speed of the fan where FAN_INDEX is the fan to take the measurement from
```
getsysinfo sysfan $FAN_INDEX
```

## Set Fan Mode
Sets the fan mode, where FAN_INDEX is the fan to adjust and mode between 0 and 7.
0 Being the lowest RPM setting and 7 being the highest.
```
hal_app --se_sys_set_fan_mode obj_index=$FAN_INDEX-1,mode=0-7
```

# Hard Disk
## Get Number of HDDs
Gets the number of HDDs installed in the system
```
getsysinfo hdnum
```

## Get Disk Temperature
Gets the temperature of an individual HDD in the system where DISK_INDEX is the disk to take the measure from
```
getsysinfo hdtmp $DISK_INDEX
```