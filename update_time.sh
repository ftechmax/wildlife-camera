#!/bin/bash

# Check if two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start_time> <end_time>"
    exit 1
fi

start_time=$1  # e.g., "06:00"
end_time=$2    # e.g., "23:00"

# Directly set the next wake time
/sbin/hwclock --adjust # adjust the RTC to account for systematic drift
/sbin/hwclock --hctosys # set the system time from the RTC
echo 0 | sudo tee /sys/class/rtc/rtc0/wakealarm >/dev/null
echo $(date '+%s' -d "tomorrow ${start_time}") | sudo tee /sys/class/rtc/rtc0/wakealarm >/dev/null

# Update set_daily_alarm.sh
set_daily_alarm_path="/usr/local/bin/set_daily_alarm.sh"
sed -i "s/^echo \$(date '+%s' -d '.*')/echo \$(date '+%s' -d 'tomorrow $start_time')/" "$set_daily_alarm_path"

# Update crontab
(crontab -l | grep -v $set_daily_alarm_path; echo "@reboot sleep 60 && sudo /bin/bash $set_daily_alarm_path") | crontab -
(crontab -l | grep -v '/sbin/shutdown -h now'; echo "0 ${end_time:0:2} * * * sudo /sbin/shutdown -h now") | crontab -

echo "Updated wake time to $start_time and shutdown time to $end_time."
