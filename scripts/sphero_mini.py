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
import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist

from sphero_mini_lib.sphero_mini import sphero_mini
from sphero_mini_lib.sphero_mini import sphero_mini

import time


LOOP_FREQ = 20
LOOP_DT = 0.05



class SpheroMiniROSDriver(object):
    ''' sub scribe topic and publish after safety check
    '''

    def __init__(self, tello):

        self._cmd_vel = Twist()
        
        self._cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self._cmd_vel_sub_cb)
        self._pose_pub = rospy.Publisher('pose', Pose, queue_size=10)
    
    def _cmd_vel_sub_cb(self, msg):
        self._cmd_vel = msg


    def spin(self):
        count = 0
        r = rospy.Rate(LOOP_FREQ)
        while not rospy.is_shutdown():
            if count > 100:
                count = 0
                self._tello.send_command('command')  
            else:
                pass

            count += 1
            r.sleep()
        

def main():
    sphero_mini = sphero_mini('', 8889) 

    rospy.init_node('tello_control')
    node = TelloROSDriver(tello)
    node.spin()

if __name__ == '__main__':
    main()