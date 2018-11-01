#!/usr/bin/python
# -*- coding: UTF-8

# 超声波驱动，可以获取测距值

import RPi.GPIO as GPIO
import time


class ultrasonic:  # GPIO1-T，GPIO2-E
    def __init__(self, GPIO1, GPIO2):
        self.t = GPIO1
        self.e = GPIO2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO1, GPIO.OUT)
        GPIO.setup(GPIO2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(GPIO1, GPIO.LOW)

    def get_dis(self):
        GPIO.output(self.t, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.t, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self.t, GPIO.LOW)
        while (not(GPIO.input(self.e) == 1)):
            pass
        start = time.clock() * 1000000
        while (not(GPIO.input(self.e) == 0)):
            pass
        stop = time.clock() * 1000000
        dis = (stop - start) / 1000000 * 34000 / 2
        return dis

    def destroy(self):
        GPIO.cleanup()
