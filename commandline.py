import threading
import cv2
import Queue as queue
import datetime
import time

import visu
import open3d

def worker(statev,rospy):
    x=""
    count = 0
    while x!="q":
        x= raw_input("Enter command")
        if "pc" in x:
            
            #print("wow")
            ola = x.split(" ")
            if(len(ola)==1):
                visu.draw_geometry([statev.pc])
            else:
                time.sleep(int(ola[1]))
                visu.draw_geometry([statev.pc])
        elif "lol" in x:
            print("2 cams calc")
            statev.CalcRT2()
            rospy.signal_shutdown('Quit')
            break
        elif "R" in x:
            print("calculating R")
            statev.CalcRthenStartT()
        elif "T" in x:
            print("calculating t")
            statev.CalcT()
            rospy.signal_shutdown('Quit')
            break
        else:
            print("invalid command")

    return


def Start(statev,rospy):

    t1 = threading.Thread(target=worker,args=(statev,rospy,))
    t1.start()