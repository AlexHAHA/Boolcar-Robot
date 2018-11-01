#!/usr/bin/python
# -*- coding: UTF-8

#小车红外线寻迹程序

import boolcar
car=boolcar.boolcar()

while car.flag:
    if car.track==car.null:
        car.go_front()
    elif car.track==car.left:
        car.go_right()
    elif car.track==car.right:
        car.go_left()
    elif car.track==car.both:
        car.go_back()
    car.wait(0.2)