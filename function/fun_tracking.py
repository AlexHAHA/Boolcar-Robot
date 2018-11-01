#!/usr/bin/python
# -*- coding: UTF-8
# 功能类，小车循迹，初始化提供电机，红外


import time
import RPi.GPIO as GPIO


class fun_trk:
    def __init__(self, motor, hw):
        self.motor = motor
        self.hw = hw

    def tracking(self):
        [al, ar] = self.hw.get_status()
        if ar == GPIO.LOW and al == GPIO.LOW:
            self.motor.stop()
        elif ar == GPIO.HIGH and al == GPIO.LOW:
            self.motor.turn_left()
        elif al == GPIO.HIGH and ar == GPIO.LOW:
            self.motor.turn_right()
        else:
            self.motor.move_forward()
