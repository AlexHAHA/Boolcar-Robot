#!/usr/bin/python
# -*- coding: UTF-8

#测试文件旨在测试所有硬件是否正常工作



import boolcar
car=boolcar.boolcar()

for mun in range(1,5):
    print("step:",mun)
    if mun==1:
        while car.track()%2==0:
            car.wait(0.5)
            print("please cover tracking infrared left")
        print("ok")
        while car.track()<2:
            car.wait(0.5)
            print("please cover tracking infrared right")
        print("ok")
        print("tracking infrared test finish")
    elif mun==2:
        car.go_front(3)
        car.go_back(3)
        car.go_left(3)
        car.go_right(3)
        car.stop()
        print("motor test finish")
    elif mun==3:
        for i in range(0,10):
            print("distance:",car.range())
            car.wait(0.5)
            print("ultrasonic test finish")
    elif mun==4:
        car.rotate_bottom(10)
        car.wait(0.5)
        car.rotate_bottom(170)
        car.wait(0.5)
        car.rotate_bottom(90)
        car.wait(0.5)
        car.rotate_above(10)
        car.wait(0.5)
        car.rotate_above(170)
        car.wait(0.5)
        car.rotate_above(90)
        print("steering test finish")
    else:
        print("no more")
        print("test over")  
car.sleep()