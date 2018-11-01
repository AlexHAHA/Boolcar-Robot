#!/usr/bin/python
# -*- coding: UTF-8
# 功能类，小车超声波避障，初始化提供电机，红外


import time
import RPi.GPIO as GPIO


class fun_ult_ob:
    def __init__(self, motor, cs):
        self.motor = motor
        self.cs = cs

    def obstruction(self):
        dis = self.cs.get_dis()
        if dis < 30:
            self.motor.move_backward()
            time.sleep(0.3)
            self.motor.turn_left()
        else:
            self.motor.move_forward()
