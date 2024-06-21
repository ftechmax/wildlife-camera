#!/bin/bash

/sbin/hwclock --hctosys
echo 0 | sudo tee /sys/class/rtc/rtc0/wakealarm >/dev/null
echo $(date '+%s' -d 'tomorrow 08:00') | sudo tee /sys/class/rtc/rtc0/wakealarm >/dev/null
