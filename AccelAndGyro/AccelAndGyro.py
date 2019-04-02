#!/usr/bin/python

import smbus
import math
import time
 
# Register addresses
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Convert two 8-bit numbers to a 16-bit number
def dataConv(data1, data2):
        value = data1 | (data2 << 8)
        if(value & (1 << 16 - 1)):
            value -= (1<<16)
        return value

def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) for revision 1
address = 0x68       # via i2cdetect
 
# Activate module
bus.write_byte_data(address, power_mgmt_1, 0)
time.sleep(0.5)

print "Acceleration sensor :"
print "---------------------"

data = bus.read_i2c_block_data(0x68, 0x3b, 6)
 
acceleration_xout = dataConv(data[1], data[0])
acceleration_yout = dataConv(data[3], data[2])
acceleration_zout = dataConv(data[5], data[4])
 
acceleration_xout_normalized = acceleration_xout / 16384.0
acceleration_yout_normalized = acceleration_yout / 16384.0
acceleration_zout_normalized = acceleration_zout / 16384.0

print "acceleration_xout: ", ("%6d" % acceleration_xout), " normalized: ", acceleration_xout_normalized
print "acceleration_yout: ", ("%6d" % acceleration_yout), " normalized: ", acceleration_yout_normalized
print "acceleration_zout: ", ("%6d" % acceleration_zout), " normalized: ", acceleration_zout_normalized

print
print "Rotation around X axis (deg.): " , get_x_rotation(acceleration_xout_normalized, acceleration_yout_normalized, acceleration_zout_normalized), " deg."
print "Rotation around Y axis (deg.): " , get_y_rotation(acceleration_xout_normalized, acceleration_yout_normalized, acceleration_zout_normalized), " deg."

print
print
print "Gyroscope sensor :"
print "------------------"

data = bus.read_i2c_block_data(0x68, 0x43, 6)

gyroscope_xout = dataConv(data[1], data[0])
gyroscope_yout = dataConv(data[3], data[2])
gyroscope_zout = dataConv(data[5], data[4])

gyroscope_xout_normalized = gyroscope_xout / 131
gyroscope_yout_normalized = gyroscope_yout / 131
gyroscope_zout_normalized = gyroscope_zout / 131

print "Angular velocity around x axis: ", ("%5d" % gyroscope_xout), " normalized: ", gyroscope_xout_normalized 
print "Angular velocity around y axis: ", ("%5d" % gyroscope_yout), " normalized: ", gyroscope_yout_normalized
print "Angular velocity around z axis: ", ("%5d" % gyroscope_zout), " normalized: ", gyroscope_zout_normalized
 


