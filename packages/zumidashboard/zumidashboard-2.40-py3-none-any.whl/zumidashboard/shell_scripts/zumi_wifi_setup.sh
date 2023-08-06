#!/bin/bash

killall wpa_supplicant
wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf
dhclient wlan0

while true
do
  sleep 100
done