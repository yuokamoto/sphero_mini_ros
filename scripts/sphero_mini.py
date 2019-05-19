#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sphero_mini.py
#
# Created on: May 15, 2019
#     Author: Yu Okamoto
# Brief: sphero mini ros driver

# import math
# import numpy as np
import time
import sys
import signal

import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist, Pose, Vector3

from sphero_mini_lib.sphero_mini import sphero_mini

LOOP_FREQ = 5
LOOP_DT = 0.05

class SpheroMiniROSDriver(object):
    ''' sub scribe topic and publish after safety check
    '''

    def __init__(self, MAC):
        self._sphero_mini = sphero_mini(MAC, verbosity = 2)
        self._sphero_mini.stabilization(True)
        self._sphero_mini.configureSensorMask(IMU_yaw = True)
        self._sphero_mini.configureSensorStream()

        self._cmd_vel = Twist()
        self._cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self._cmd_vel_sub_cb)
        self._set_led_sub = rospy.Subscriber('set_led', Vector3, self._set_led_sub_cb)
        self._pose_pub = rospy.Publisher('pose', Pose, queue_size=10)
    
    def signal_handler(self, sig, frame):
        print('exit sphero_mini ROS node')
        self._sphero_mini.sleep()
        self._sphero_mini.disconnect()
        sys.exit(0)

    def _set_led_sub_cb(self, msg):
        if msg.x + msg.y + msg.z > 255:
            print('Sum of rgb should be less than 255, r:{}, g:{}, b:{}'
                ,round(msg.x), round(msg.y), round(msg.z))
            return 
        self._sphero_mini.setLEDColor(round(msg.x), round(msg.y), round(msg.z))
        
    def _cmd_vel_sub_cb(self, msg):
        self._cmd_vel = msg
        print('cmd vel sub', msg)

    def spin(self):
        count = 0
        r = rospy.Rate(LOOP_FREQ)
        while not rospy.is_shutdown():
            if count > 100:
                count = 0
                # self._pose_pub.publish(Pose())

            else:
                yaw = self._sphero_mini.IMU_yaw
                self._sphero_mini.setLEDColor(round(0),round(0),round(0))
                print("Yaw angle: {}".format(round(yaw, 3)))
                
            count += 1
            r.sleep()
        

def main():
    rospy.init_node('sphero_mini')
    MAC = rospy.get_param('~mac')
    node = SpheroMiniROSDriver(MAC)

    signal.signal(signal.SIGINT, node.signal_handler)

    node.spin()

if __name__ == '__main__':
    main()