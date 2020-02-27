#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist


def driveControl():
    pub = rospy.Publisher('cmd_drive', Twist, queue_size=10)
    rospy.init_node('driveControl', anonymous=True)
    rate = rospy.Rate(5)

    while not rospy.is_shutdown():
        cmd_msg = Twist()

        cmd_msg.linear.x = 0.0
        cmd_msg.angular.z = 0.0
        rospy.loginfo(cmd_msg)
        pub.publish(cmd_msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        driveControl()
    except rospy.ROSInterruptException:
        pass
