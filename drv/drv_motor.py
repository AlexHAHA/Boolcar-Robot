#!/usr/bin/python
# -*- coding: UTF-8

import RPi.GPIO as GPIO
import time

# 新电机驱动
# RPI3 pins defination
PIN_MOTOR_LEFTPWM = 18
PIN_MOTOR_L = 23     # pin of left


PIN_MOTOR_RIGHTPWM = 17
PIN_MOTOR_R = 24     # pin of right


class motorControl:

    def __init__(self,lp=PIN_MOTOR_LEFTPWM ,l=PIN_MOTOR_L ,rp=PIN_MOTOR_RIGHTPWM ,r=PIN_MOTOR_R ):
        self.pwm_frequency = 40
        self.speed_level_left = 40
        self.speed_level_right = 40
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN_MOTOR_LEFTPWM, GPIO.OUT)
        self.speed_left = GPIO.PWM(PIN_MOTOR_LEFTPWM, self.pwm_frequency)

        GPIO.setup(PIN_MOTOR_RIGHTPWM, GPIO.OUT)
        self.speed_right = GPIO.PWM(PIN_MOTOR_RIGHTPWM, self.pwm_frequency)

        # start generate PWM to control speed of motor
        self.speed_left.start(0)
        self.speed_right.start(0)
        GPIO.setup(PIN_MOTOR_L, GPIO.OUT)
        GPIO.output(PIN_MOTOR_L, GPIO.LOW)
        GPIO.setup(PIN_MOTOR_R, GPIO.OUT)
        GPIO.output(PIN_MOTOR_R, GPIO.LOW)


    def move_forward(self):


        GPIO.output(PIN_MOTOR_L, GPIO.HIGH)
        GPIO.output(PIN_MOTOR_R, GPIO.LOW)
        self.speed_left.ChangeDutyCycle(float(self.speed_level_left))
        self.speed_right.ChangeDutyCycle(float(self.speed_level_right))

    def move_backward(self):

        GPIO.output(PIN_MOTOR_L, GPIO.LOW)
        GPIO.output(PIN_MOTOR_R, GPIO.HIGH)
        self.speed_left.ChangeDutyCycle(float(self.speed_level_left))
        self.speed_right.ChangeDutyCycle(float(self.speed_level_right))

    def turn_left(self,mode=0):

        
        if mode==1:
            GPIO.output(PIN_MOTOR_L, GPIO.HIGH)
            GPIO.output(PIN_MOTOR_R, GPIO.LOW)
            self.speed_left.ChangeDutyCycle(float(self.speed_level_left*0.1))
            self.speed_right.ChangeDutyCycle(float(self.speed_level_right))
        else:
            GPIO.output(PIN_MOTOR_L, GPIO.LOW)
            GPIO.output(PIN_MOTOR_R, GPIO.LOW)
            self.speed_left.ChangeDutyCycle(float(self.speed_level_left))
            self.speed_right.ChangeDutyCycle(float(self.speed_level_right))

    def turn_right(self,mode=0):
        
        if mode==1:
            GPIO.output(PIN_MOTOR_L, GPIO.HIGH)
            GPIO.output(PIN_MOTOR_R, GPIO.LOW)
            self.speed_left.ChangeDutyCycle(float(self.speed_level_left))
            self.speed_right.ChangeDutyCycle(float(self.speed_level_right*0.1))
        else:
            GPIO.output(PIN_MOTOR_L, GPIO.HIGH)
            GPIO.output(PIN_MOTOR_R, GPIO.HIGH)
            self.speed_left.ChangeDutyCycle(float(self.speed_level_left))
            self.speed_right.ChangeDutyCycle(float(self.speed_level_right))

    def change_speed_left(self, speed_level):
        self.speed_level_left = speed_level

    def change_speed_right(self, speed_level):
        self.speed_level_right = speed_level


    def stop(self):
        self.speed_left.ChangeDutyCycle(0)
        self.speed_right.ChangeDutyCycle(0)

    def get_speed_level(self):
        return(self.speed_level_left, self.speed_level_right)

    def destroy(self):
        GPIO.cleanup()
