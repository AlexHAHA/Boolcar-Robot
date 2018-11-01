#!/usr/bin/python
# -*- coding: UTF-8

# 舵机驱动，可以获取此时舵机的角度，也可以改变舵机的角度

import RPi.GPIO as GPIO
import time


class servo:
    def __init__(self, GPIO1, GPIO2):  # gpio1-水平角 gpio2-俯仰角
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO1, GPIO.OUT)
        GPIO.setup(GPIO2, GPIO.OUT)
        self.horizontal_angle = GPIO.PWM(GPIO1, 50)
        self.pitch_angle = GPIO.PWM(GPIO2, 50)
        self.horizontal_angle.start(7.5)
        self.pitch_angle.start(7.5)
        self.h_angle = 90
        self.p_angle = 90

    def get_angle(self):
        return [self.h_angle, self.p_angle]

    def change_angle(self, num, angle):
        if num == 1:
            self.h_angle = angle
            self.horizontal_angle.ChangeDutyCycle(angle * 10 / 180 + 2.5)
        else:
            self.p_angle = angle
            self.pitch_angle.ChangeDutyCycle(angle * 10 / 180 + 2.5)
        time.sleep(1)

    def angle_set(self, angle_yaw,angle_pitch):
        self.h_angle = angle_yaw
        self.horizontal_angle.ChangeDutyCycle(angle_yaw * 10 / 180 + 2.5)

        self.p_angle = angle_pitch
        self.pitch_angle.ChangeDutyCycle(angle_pitch * 10 / 180 + 2.5)


    def destroy(self):
        GPIO.cleanup()
