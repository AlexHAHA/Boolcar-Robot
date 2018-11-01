import smbus
import math
import time

temp_x=0;
temp_y=0;
class HMC5883:
    # sensor range : [number,digital resolution(mG/LSb)]
    __scales = {
        0.88: [0, 0.73],
        1.30: [1, 0.92],
        1.90: [2, 1.22],
        2.50: [3, 1.52],
        4.00: [4, 2.27],
        4.70: [5, 2.56],
        5.60: [6, 3.03],
        8.10: [7, 4.35]
    }
   
    def __init__(self, port=1, address=0x1E, gauss=1.3, declination=(0, 0)):
        self.bus = smbus.SMBus(port)
        self.address = address

        (degrees, minutes) = declination
        self.__declDegrees = degrees
        self.__declMinutes = minutes
        self.__declination = (degrees + minutes / 60) * math.pi / 180

        (reg, self.__scale) = self.__scales[gauss]
        # samples averaged = 8; output rate = 15
        self.bus.write_byte_data(self.address, 0x00, 0x70)
        # scale
        self.bus.write_byte_data(self.address, 0x01, reg << 5)
        # continous measurement
        self.bus.write_byte_data(self.address, 0x02, 0x00)

    def declination(self):
        return (self.__declDegrees, self.__declMinutes)

    def twos_complement(self, val, length):
        # convert tows compliment to integer
        if(val & (1 << length - 1)):
            val = val - (1 << length)
        return val

    def __convert(self, data, offset):
        val = self.twos_complement(data[offset] << 8 | data[offset + 1], 16)
        if val == -4096:
            return None
        return round(val * self.__scale, 4)

    def axes(self):
        data = self.bus.read_i2c_block_data(self.address, 0x00)
        x = self.__convert(data, 3)
        y = self.__convert(data, 7)
        z = self.__convert(data, 5)
        
        x_offset = (330-620.76)/2+35
        y_offset = (385.4-381.48)/2
        x_gain=1
        y_gain=(385.4+381.48)/(330+620.76)
        x=x_gain*(x-x_offset)
        y=y_gain*(y-y_offset)
        return(x, y, z)

    def axes_gauss(self):
        data = self.axes()
        return data * self.__scale

    def heading(self):
        global temp_x,temp_y
        (x, y, z) = self.axes()
        headingRad = math.atan2(y, x)
        headingRad += self.__declination
        temp_x=x
        temp_y=y
        if headingRad < 0:
            headingRad += 2 * math.pi
        elif headingRad > 2 * math.pi:
            headingRad -= 2 * math.pi
        headingDeg = headingRad * 180 / math.pi
        return headingDeg

    def degrees(self, headingDeg):
        degrees = math.floor(float(headingDeg))
        minutes = round((headingDeg - degrees) * 60)
        return (degrees, minutes)

    def __str__(self):
        (x, y, z) = self.axes()
        return "Axis X: " + str(x) + "\n" \
               "Axis Y: " + str(y) + "\n" \
               "Axis Z: " + str(z) + "\n" \
               "Declination: " + self.degrees(self.declination()) + "\n" \
               "Heading: " + self.degrees(self.heading()) + "\n"
    def angle_adjust_fun(self):
        return self.heading()-360


cout=0
if __name__ == "__main__":
    compass = HMC5883(gauss=4.7)
    temp_max_x=0
    temp_min_x=0
    temp_max_y=0
    temp_min_y=0
    while 0:
        
        c=compass.axes()
        if(temp_max_x<c[0]):
            temp_max_x=c[0]
        if(temp_min_x>c[0]):
            temp_min_x=c[0]
        
        if(temp_max_y<c[1]):
            temp_max_y=c[1]
        if(temp_min_y>c[1]):
            temp_min_y=c[1]
        cout=cout+1
        print "x:",c[0]
        print "y:",c[1]
        time.sleep(0.05)
        if(cout>1500):
            cout=0
            print "max_x:",temp_max_x
            print "min_x:",temp_min_x
            print "max_y:",temp_max_y
            print "min_y:",temp_min_y
            break
    while 1:
        print compass.heading()-268
        #print "x:",temp_x
        #print "y",temp_y
        time.sleep(2)
        
