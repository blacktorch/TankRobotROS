#!/usr/bin/env python

import rospy
import socket
import threading
import drive
from geometry_msgs.msg import Twist

message = "0.0,0.0"


def remote_server(sema):
    global message
    message = "0.0,0.0"

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('192.168.1.160', 12345))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()

        try:
            print("connected to: {}".format(addr))

            while True:
                sema.acquire()
                data = conn.recv(32)
                if not data:
                    break
                message = str(data)

                conn.send(bytes("Data received \n"))
                sema.release()
        finally:
            conn.close()
            print('client disconnected')


def controller(sema):
    pub = rospy.Publisher('cmd_drive', Twist, queue_size=10)
    rate = rospy.Rate(5)

    while not rospy.is_shutdown():
        cmd_msg = Twist()

        sema.acquire()

        params = message.split(",")

        print(params)

        z = float(params[0])
        x = float(params[1])

        if z < 0.0:
            cmd_msg.angular.z = drive.valueMap(z, -0.001, -1.0, 0.01, 4.25)
        elif z > 0.0:
            cmd_msg.angular.z = drive.valueMap(z, 0.001, 1.0, -0.01, -4.25)
        else:
            cmd_msg.angular.z = 0.0

        if x < 0.0:
            cmd_msg.linear.x = drive.valueMap(x, -0.001, -1.0, 0.01, 0.5)
        elif x > 0.0:
            cmd_msg.linear.x = drive.valueMap(x, 0.001, 1.0, -0.01, -0.5)
        else:
            cmd_msg.linear.x = 0.0

        rospy.loginfo(cmd_msg)
        pub.publish(cmd_msg)

        sema.release()
        rate.sleep()


def remote_controller():
    rospy.init_node('remoteDriveControl', anonymous=True)

    controllerSemaphore = threading.Semaphore()
    serverSemaphore = threading.Semaphore()

    serverThread = threading.Thread(target=remote_server, args=serverSemaphore)
    serverThread.start()

    controllerThread = threading.Thread(target=controller, args=controllerSemaphore)
    controllerThread.start()


if __name__ == '__main__':
    try:
        remote_controller()
    except rospy.ROSInterruptException:
        pass
