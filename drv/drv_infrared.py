#!/usr/bin/python
# -*- coding: UTF-8

# 红外驱动，可获取红外线的状态

import RPi.GPIO as GPIO
import time


class infrared:  # GPIO1-左，GPIO2-右
    def __init__(self, GPIO1, GPIO2):
        self.left = GPIO1
        self.right = GPIO2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_status(self):
        return [GPIO.input(self.left), GPIO.input(self.right)]

    def destroy(self):
        GPIO.cleanup()
