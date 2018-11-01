#!/usr/bin/python
# -*- coding: UTF-8

#功能：小车贴边跑，初始化提供电机，超声波，贴边距离，红外避障，避障红外
import time
import thread

class fun_stk:
    def __init__(self, motor,cs,dis,ob,hw):
        self.ultrasonic=cs
        self.motor = motor
        self.dis = dis
        self.ob=ob
        self.hw=hw
        # pid
        self.dis_ctr_P = 0.01
        self.dis_ctr_I = 0.1
        self.pwm_left_out = 50
        self.pwm_right_out = 50
        self.cu=0
    def sec(self):
        while 1:
            if self.cu == 2:
                self.sti()
            else:
                pass
            time.sleep(0.2)

    def fir(self):
        while 1:
            if self.cu == 1:
                self.ob.obstruction()
            else:
                pass
            time.sleep(0.2)
    
    def setd(self):
        while 1:
            if self.hw.get_status() != [1, 1]:
                self.cu = 1
            else:
                self.cu = 2
            time.sleep(0.1)

    def sti(self):
        self.pwm_left_out = 50
        self.pwm_right_out = 50
        current_distance=self.ultrasonic.get_dis()
        err=current_distance-self.dis

        if err<-10:
            self.motor.turn_right()
            t1=self.dis_ctr_P*abs(err)
            if t1>1.5:
                t1=1.5
            time.sleep(t1)
            self.motor.move_forward()
            t2=self.dis_ctr_I*abs(err)
            if t2>5:
                t2=5
            time.sleep(t2)
            self.motor.turn_left()
            time.sleep(t1)
        
        elif err>10:
            self.motor.turn_left()
            t1=self.dis_ctr_P*err
            if t1>2:
                t1=2
            time.sleep(t1)
            self.motor.move_forward()
            t2=self.dis_ctr_I*err
            if t2>5:
                t2=5
            time.sleep(t2)
            self.motor.turn_right()
            time.sleep(t1)        

        else:
            self.motor.move_forward()

    def stickers(self):
        thread.start_new_thread(self.setd, ())
        thread.start_new_thread(self.fir, ())
        thread.start_new_thread(self.sec, ())




            
            
    






