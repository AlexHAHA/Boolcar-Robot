#!/usr/bin/python
# -*- coding: UTF-8
# 功能类，小车避黑区，初始化提供电机类，红外类

import time
import RPi.GPIO as GPIO

class fun_rd:
    def __init__(self, motor, hw):
        self.motor = motor
        self.hw = hw

    def road(self):
        [al, ar] = self.hw.get_status()
        if ar == GPIO.LOW and al == GPIO.LOW:
            self.motor.move_forward()
        elif ar == GPIO.HIGH and al == GPIO.LOW:
            self.motor.turn_right()
        elif al == GPIO.HIGH and ar == GPIO.LOW:
            self.motor.turn_left()
        else:
            self.motor.move_backward()
            time.sleep(0.3)
            self.motor.turn_left()
            