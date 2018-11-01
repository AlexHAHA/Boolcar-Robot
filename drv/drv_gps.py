#!/usr/bin/python
# -*- coding: UTF-8
import RPi.GPIO as GPIO
from gps.gps_class import GPS
import time

# gps驱动


class gps:
    def __init__(self):
        self.gps_data = GPS(device='/dev/ttyS0')
        self.gps_data.start()

    def get_gps(self):
        time.sleep(0.01)
        gpsnow = [self.gps_data.lat, self.gps_data.lon]
        return gpsnow
