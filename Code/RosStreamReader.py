
import numpy as np
import cv2
from libs import *

import message_filters

import os

from sensor_msgs.msg import Image

import threading

import rospy


class RosStreamReader():
    def __init__(self,state,camNames=None,freq=20):


        self.state=state

        self.freq = freq

        self.camNames=camNames

        if self.camNames is None:
            self.camNames = IRos.getAllPluggedCameras()

        self.N_cams = len(self.camNames)

        self.data={'names':self.camNames,'rgb':[],'depth':[]}

        camSub = []





        rospy.init_node('do_u_kno_di_wae', anonymous=True)

        #getting subscirpters to use message fitlers on
        for name in self.camNames:
            camSub.append(message_filters.Subscriber(name+"/rgb/image_color", Image))
            camSub.append(message_filters.Subscriber(name+"/depth_registered/image_raw", Image))




        ts = message_filters.ApproximateTimeSynchronizer(camSub,20, 1.0/freq, allow_headerless=True)
        ts.registerCallback(self.callback)

        print("Callback Registered")

        print("ENTERED THE THRAED")
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("shut")

        print("STOP SIGNALL")
        


    def callback(self,*args):
        print("Entered Callback")
        print(len(args))
        data={'names':self.camNames,'rgb':[],'depth':[]}

        for camId in range(0,self.N_cams):
            img = IRos.rosImg2RGB(args[camId*2])
            depth = IRos.rosImg2Depth(args[camId*2+1])

            data['rgb'].append(img)
            data['depth'].append(depth)
    
        self.data=data
        self.state.data=data
        self.state.nextIsAvailable=True


    def next(self):

        print("HEYYDOING THE NEXT")

        return self.data      

