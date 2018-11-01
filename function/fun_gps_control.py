#!/usr/bin/python
# -*- coding: UTF-8
import time
import math
class fun_gps_magn:
    def __init__(self,motor,gps,magn):
        self.motor = motor
        self.gps = gps
        self.magn =magn
        # 导航控制参数
        self.angle_err_last=0
        self.angle_control_value=0
        
        self.angle_ctr_D_val=0

        self.angle_ctr_P=0.008
        self.angle_ctr_D=0.001
        self.pos_ctr_P=4.5
        self.err_y_integer = 0
        self.pwm_left_out = 30
        self.pwm_right_out = 30
        self.angle_adjust=-208
        self.pos_ctr_val=0
        self.pos_set=0
    def autopilot1(self,pos_set):  # 向指定的地点跑
        self.pos_set=pos_set
        pos=self.gps.get_gps()
        print "current_pos:",pos
            
        car_yaw = self.magn.heading()
        #print "car angle",car_yaw
        car_yaw=360-car_yaw
        car_yaw=car_yaw+self.angle_adjust
        if(car_yaw<0):
            car_yaw=car_yaw+360
        elif(car_yaw>=360):
            car_yaw=car_yaw-360
        else:
            pass
        print "deal car angle:",car_yaw

        if(pos!=[0,0]):
         #   print "have GPS signal"
            pos[0]=float(pos[0])*0.01745329251994329576923690768489
            pos[1]=float(pos[1])*0.01745329251994329576923690768489
            self.pos_set[0]=self.pos_set[0]*0.01745329251994329576923690768489
            self.pos_set[1]=self.pos_set[1]*0.01745329251994329576923690768489
            #print "x:",pos[0] - self.pos_set[0]
            #print "y1",self.pos_set[0]
            #print "y2",pos[0]
            
            err_y = (pos[0]-self.pos_set[0])*6371000.0
            err_x = (-pos[1] + self.pos_set[1])*math.cos((pos[0]+self.pos_set[0])/2)*6371000.0
            if(err_y==0):
                err_y=0.0000000000000001
            else:
                pass
            #print "err_x",err_x
            #print "err_y",err_y
            target_angle=math.atan(err_x/err_y )/math.pi*180
           
            #print "target angle before deal with",target_angle
            if (err_x<0)and(err_y<0):
                target_angle=target_angle
            elif(err_x<0)and(err_y>0):
                target_angle=target_angle+180
            elif(err_x>0)and(err_y<0):
                target_angle=target_angle+360
            elif(err_x>0)and(err_y>0):
                target_angle=target_angle+180
            else:
                pass
            print "target angle:",target_angle

            norm_pos_err=math.sqrt(err_x*err_x+err_y*err_y)
            self.pos_ctr_val=self.pos_ctr_P*norm_pos_err

           # self.pos_ctr_val=100
            print "pos_ctr_val:",self.pos_ctr_val

            angle_err=car_yaw-target_angle
            if(angle_err>180):
                angle_err=angle_err-360
            elif(angle_err<-180):
                angle_err=angle_err+360
            else:
                pass
            print "car angle erro:",angle_err
            self.angle_ctr_D_val=angle_err-self.angle_err_last
            self.angle_err_last= angle_err

            self.angle_control_value= angle_err*self.angle_ctr_P+self.angle_ctr_D_val*self.angle_ctr_D
            print "angle control value:",self.angle_control_value
            if(abs(angle_err)>5):
                if self.pos_ctr_val<12:
                    return 1
                else:
                    pass
                if(self.angle_control_value>0):
                   # if self.pos_ctr_val<25:
                      #  self.motor.change_speed_left(pos_ctr_val+8)
                       # self.motor.change_speed_right(pos_ctr_val+8)
                   # else:
                    self.motor.change_speed_left(40)
                    self.motor.change_speed_right(40)
                    print "turn left"
                    self.motor.turn_left()
                    
                    time.sleep(self.angle_control_value)
                    #self.motor.stop()
                else:
                    #if self.pos_ctr_val<25:
                     #   self.motor.change_speed_left(pos_ctr_val+8)
                     #   self.motor.change_speed_right(pos_ctr_val+8)
                    #else:
                    self.motor.change_speed_left(40)
                    self.motor.change_speed_right(40)
                    print "turn right"
                    self.motor.turn_right()
                    
                    time.sleep(abs(self.angle_control_value))
                    #self.motor.stop()
            else:
                print "angle adjust is ok"
                self.motor.change_speed_left(65)
                self.motor.change_speed_right(65)
                self.motor.move_forward()
                self.angle_err_last=0
                time.sleep(3)
                #self.motor.stop()
                if self.pos_ctr_val<12:
                    return 1
                else:
                    pass

        else:            
            print "have no GPS signal"
            time.sleep(2)

    def angle_control(self,target_ctr_angle):
        print "begin parking"
        car_angle=self.magn.heading()
        car_angle=360-car_angle
        angle_err=car_angle-target_ctr_angle
        if(angle_err>180):
            angle_err=angle_err-360
        elif(angle_err<-180):
            angle_err=angle_err+360
        else:
            pass
        print "park car angle erro:",angle_err
        self.angle_ctr_D_val=angle_err-self.angle_err_last
        self.angle_err_last= angle_err
        self.angle_control_value= angle_err*self.angle_ctr_P+self.angle_ctr_D_val*self.angle_ctr_D
        if(abs(angle_err)>4):
            if(self.angle_control_value>0):
                self.motor.change_speed_left(40)
                self.motor.change_speed_right(40)
                print "turn left"
                self.motor.turn_left()
                    
                time.sleep(self.angle_control_value)
                
            else:
                self.motor.change_speed_left(40)
                self.motor.change_speed_right(40)
                print "turn right"
                self.motor.turn_right()
                    
                time.sleep(abs(self.angle_control_value))
        else:
            self.angle_err_last=0
            print "parking angle adjust is ok"
            self.motor.stop()
            return 1
             
            
