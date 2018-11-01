#!/usr/bin/python
# -*- coding: UTF-8

#功能类，利用红外传感器避障，初始化提供电机类，红外线类
import time
import RPi.GPIO as GPIO


class fun_in_ob:
    def __init__(self, motor, hw):
        self.motor = motor
        self.hw = hw

    def obstruction(self):
        [al, ar] = self.hw.get_status()
        if ((ar == GPIO.LOW) and (al == GPIO.LOW)):
            self.motor.move_backward()
            time.sleep(0.3)
            self.motor.turn_left()
            print "back"
        elif ((ar == GPIO.HIGH) and (al == GPIO.LOW)):
            self.motor.turn_right()
            print "right"
        elif ((ar == GPIO.LOW) and (al == GPIO.HIGH)):
            self.motor.turn_left()
            print "left"
        else:
            self.motor.move_forward()
            print "go"
