#!/usr/bin/python3
# -*- coding: UTF-8

#boolcar class 
#can complete base behavior : move, ranging and track

#import drv.drv_gps as gp
#import drv.drv_hmc5883 as hmc
import drv.drv_servo as tj  #According to demand
import drv.drv_infrared as hw
import drv.drv_motor as mc
import drv.drv_ultrasonic as csb
import time
import _thread
import signal
import sys
from socket import *



class boolcar():
    def __init__(self):
        self.wake()
        self.null=0
        self.left=1
        self.right=2
        self.both=3
        signal.signal(signal.SIGINT, self.__private_handler)
        
    def __del__(self):
        self.sleep()
    
#小车行动相关
    def go_front(self,sec=0):
        if self.flag:
            self.__private_motor.move_forward()
            self.status="go ahead"
            self.write(self.status)
            if sec>0:
                self.wait(sec)

    def go_back(self,sec=0):
        if self.flag:
            self.__private_motor.move_backward()
            self.status="go back"
            self.write(self.status)
            if sec>0:
                self.wait(sec)

    def go_left(self,mode=0):
        if self.flag:
            if mode==-1:
                self.__private_motor.turn_left(1)
                self.status="go left"
            else:
                self.__private_motor.turn_left()
                self.status="left"
            self.write(self.status)
            if mode>0:
                self.wait(mode)

    def go_right(self,mode=0):
        if self.flag:
            if mode==-1:
                self.__private_motor.turn_right(1)
                self.status="go right"
            else:    
                self.__private_motor.turn_right()
                self.status="right"
            self.write(self.status)
            if mode>0:
                self.wait(mode)


    def stop(self,sec=0):
        if self.flag:
            self.__private_motor.stop()
            self.status="stop"
            self.write(self.status)
            if sec>0:
                self.wait(sec)


    def slow(self,speed=5):
        if self.flag:
            if self.speed>5:
                self.speed-=speed
                self.__private_motor.change_speed_left(0.8*self.speed)
                self.__private_motor.change_speed_right(0.8*self.speed)
                self.status="slow down to"+str(self.speed)
                self.write(self.status)
            else:
                print("can't be more slow")

    def quick(self,speed=5):
        if self.flag:
            if self.speed<95:
                self.speed+=speed
                self.__private_motor.change_speed_left(0.8*self.speed)
                self.__private_motor.change_speed_right(0.8*self.speed)
                self.status="speed up to"+str(self.speed)
                self.write(self.status)
            else:
                print("can't be more quick")

    def rotate_bottom(self,ang=90):
        past=self.__private_sor.get_angle()
        if ang>0 and ang<180 and ang!=past[0]:
            self.__private_sor.change_angle(1,ang)
            self.status="rotate bottom steering to "+str(ang)+"°"
            self.write(self.status)
        else:
            print("left input invalid ")  

    def rotate_above(self,ang=90): 
        past=self.__private_sor.get_angle() 
        if ang>0 and ang<180 and ang!=past[1]:
            self.__private_sor.change_angle(2,ang)
            self.status="rotate above steering to "+str(ang)+"°"
            self.write(self.status)
        else:
            print("input invalid ")                
                
#小车感知相关
    def range(self,flag=True):
        if self.flag:
            a=self.__private_ult.get_dis()
            if flag:
                self.status="get distance:"+str(a)+"cm"
                self.write(self.status)
            return a
        return -1

    def find(self,flag=True):
        if self.flag:
            a=self.__private_A_inf.get_status()
            if a[0]+a[1]:
                if a[0]+a[1]-1:
                    c=0
                elif a[1]:
                    c=1
                else:
                    c=2
            else:
                c=3    
            if flag:
                self.status="get object:"+str(c)
                self.write(self.status)
            return c
        return -1
    def track(self,flag=True):
        if self.flag:
            a=self.__private_B_inf.get_status()
            if a[0]+a[1]:
                if a[0]+a[1]-1:
                    c=0
                elif a[1]:
                    c=1
                else:
                    c=2
            else:
                c=3  
            if flag:
                self.status="get groud:"+str(c)
                self.write(self.status)
            return c
        return -1

    def connect(self,tag=0):
        udp_gui_host = '192.168.12.202'
        udp_gui_port = 8888
        udp_car = socket(AF_INET, SOCK_DGRAM)
        # bind all ip within the localnetwork
        udp_car.bind(('0.0.0.0', 8888))
        flag_connect = False
        data_msg = [0,0,0]
        self.status="begin connect"
        self.write(self.status)
        print("car_server has open")

        while self.flag:
            data_re, (udp_gui_host, udp_gui_port) = udp_car.recvfrom(1024)
            data=data_re.decode('utf-8')
            if data:
                flag_connect = True  
                if data=="over":
                    self.sleep()
                    break
                data_m=data[0:len(data)-1]
                data_s=data[len(data)-1]
                if tag==0:
                    self.__private_remotectl_handler(data_m)
                else:
                    tag(data_m)
                if data_s=="1":
                    self.quick()
                elif data_s=="2":
                    self.slow()
                elif data_s=="3":
                    self.rotate_above(65)
                elif data_s=="4":
                    self.rotate_above(110)
                else:
                    pass    
                print("[%s:%s] connect" % (udp_gui_host, udp_gui_port))
                print(data)
            else:
                flag_connect = False
                self.stop()
            if flag_connect:
                time.sleep(0.1)
                data_msg[0] = self.track(False)
                data_msg[1]=self.speed
            # buf = pickle.dumps(data_msg)
                buf = str(data_msg)
                print("server begin send")
                udp_car.sendto(buf.encode('utf-8'), (udp_gui_host, udp_gui_port))
        self.status="connect over"
        self.write(self.status)



#小车系统相关   
    def wait(self,t):
        time.sleep(t)
        self.status="wait for:"+str(t)+"s"
        self.write(self.status)

    def write(self,status):
        self.__private_file.write(time.asctime( time.localtime(time.time()) )+": " +self.status+"\n")
        self.__private_file.flush()

    def sleep(self,ok=0):
        print("system close")
        self.stop()
        self.flag=False
        if ok==0:
            self.status="system normally close"
        elif ok==1:
            self.status="system self close"
        else:
            self.status="system unkown close"          
        self.write(self.status)
        time.sleep(1)
        self.__private_motor.destroy()

    def wake(self,flag=0):
        self.__private_motor=mc.motorControl()
        self.__private_A_inf=hw.infrared(7,8)
        self.__private_B_inf=hw.infrared(16,12)
        self.__private_ult=csb.ultrasonic(20,21)
        self.__private_sor=tj.servo(5,6)
        self.__private_file = open("log.txt" ,"a")
        if flag:
            _thread.start_new_thread(self.__private_alarm,())
        self.flag=True
        self.speed=40
        if flag>1:
            self.status="system rebegin"
        else:           
            self.status="system begin"
        self.__private_motor.change_speed_left(0.8*self.speed)
        self.__private_motor.change_speed_right(0.8*self.speed)
        print("ready ok,next to work")
        self.__private_file.write("\n\n------------------------\n")
        self.write(self.status)

    def set(self,ti=0):
        if ti>0:
            _thread.start_new_thread(self.__private_set,(ti,))
        else:
            print("time is invaild")
            self.sleep()


#一些私有方法
    def __private_alarm(self):
        while self.flag:
            if self.find(False):
                print ("have something around")
                self.sleep()
            time.sleep(3)

    def __private_set(self,ti):
        time.sleep(ti)
        self.sleep()


    def __private_remotectl_handler(self,data):
        if len(data)<12:
            print("command error")
        elif data == "[1, 0, 0, 0]":  # 匹配的字符串
            self.go_front()  # 执行的函数
        elif data == "[0, 1, 0, 0]":
            self.go_back()
        elif data == "[0, 0, 1, 0]":
            self.go_left()
        elif data == "[0, 0, 0, 1]":
            self.go_right()
        elif data == "[0, 0, 0, 0]":
            self.stop()
        elif data == "[1, 0, 1, 0]":
            self.go_left(-1)
        elif data == "[1, 0, 0, 1]":
            self.go_right(-1)
        else:
            pass

    def __private_handler(self, signum, frame):
        self.sleep()
        sys.exit()
