#!/usr/bin/env python

import rospy
import move
import numpy
from geometry_msgs.msg import Twist

def perform_drive(data):
    if not data.angular.z:
        if data.linear.x >= -0.5 and data.linear.x <= 0.5:
            if data.linear.x == 0.0:
                move.motorStop()
            elif data.linear.x > 0.0:
                speed = int(valueMap(data.linear.x, 0.01, 0.5, 0.0, 100.0))
                move.move(speed, 'forward', 'no', 1)
            elif data.linear.x < 0.0:
                speed = int(valueMap(data.linear.x, -0.01, -0.5, 0.0, 100.0))
                print(speed)
                move.move(speed, 'backward', 'no', 1)
        else:
            move.motorStop()
    else:
        if data.angular.z >= -4.25 and data.angular.z <= 4.25 and data.linear.x >= -0.5 and data.linear.x <= 0.5:
            if data.angular.z == 0.0 and data.linear.x == 0.0:
                move.motorStop()
            elif data.angular.z == 0.0:
                move.motorStop()
            elif data.angular.z > 0.0:
                speed = int(valueMap(data.angular.z, 0.01, 4.25, 0.0, 100.0))
                move.move(speed, 'no', 'left', 1)
            elif data.angular.z < 0.0:
                speed = int(valueMap(data.angular.z, -0.01, -4.25, 0.0, 100.0))
                move.move(speed, 'no', 'right', 1)
            elif data.angular.z > 0.0 and data.linear.x > 0.0:
                radius = int(valueMap(data.angular.z, 0.01, 4.25, 0.0, 1.0))
                move.move(100, 'forward', 'left', radius)
            elif data.angular.z < 0.0 and data.linear.x > 0.0:
                radius = int(valueMap(data.angular.z, -0.01, -4.25, 0.0, 1.0))
                move.move(100, 'forward', 'right', radius)
            elif data.angular.z > 0.0 and data.linear.x < 0.0:
                radius = int(valueMap(data.angular.z, 0.01, 4.25, 0.0, 1.0))
                move.move(100, 'backward', 'left', radius)
            elif data.angular.z < 0.0 and data.linear.x < 0.0:
                radius = int(valueMap(data.angular.z, -0.01, -4.25, 0.0, 1.0))
                move.move(100, 'backward', 'right', radius)
        else:
            move.motorStop()
            
            
            
def valueMap(value, v_min, v_max, d_min, d_max):
    mappedValue = (value - v_min) * ((d_max - d_min) / (v_max - v_min)) + d_min
    return mappedValue

def drive():
    rospy.init_node('drive', anonymous=True)
    rospy.Subscriber('cmd_drive', Twist, perform_drive)
    
    rospy.spin()
    
if __name__ == '__main__':
    try:
        move.setup()
        drive()
    except rospy.ROSInterruptException:
        motorStop()
        GPIO.cleanup()
        pass
        