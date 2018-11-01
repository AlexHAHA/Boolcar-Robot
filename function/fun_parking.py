#!/usr/bin/python
# -*- coding: UTF-8

# 功能类，用pid控制小车距离20cm停车，初始化提供电机类，超声波类


import time


class fun_parking:
    def __init__(self, motor, cs):
        self.motor = motor
        self.cs = cs
        # pid
        self.n1 = 0
        self.n2 = 0
        self.uv = 0
        self.a0=100
        self.a1=100
        self.a2=100

    def parking(self):  
        a = self.cs.get_dis() - 40
        c =abs(a)
        if c<0.5 and self.a0<0.5 and self.a1<0.5 and self.a2<0.5:
            self.motor.stop()
            return 0
        self.a0=c
        self.a1=self.a0
        self.a2=self.a1
        y1 = a *0.5
        y2 = (a - self.n1) * 0.2
        y3 = (a - 2 * self.n1 + self.n2) * 0.2
        v2 = y1 + y2 + y3
        v = v2 + self.uv
        if v > 30:
            v = 30
        elif v < -30:
            v = -30
        self.motor.change_speed_left(abs(v)+20)
        self.motor.change_speed_right(abs(v)+20)
        self.n1 = a
        self.n2 = self.n1
        self.uv = v2
        if v > 0:
            self.motor.move_forward()
        else:
            self.motor.move_backward()
        if c>30:
            time.sleep(1)
        else:
            time.sleep(0.02 * c)
        return 1
