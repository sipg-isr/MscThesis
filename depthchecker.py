#HERE WILL BE the v1, but organized in a good fashion
import ArucoInfoGetter
import rospy
import algos
import pickler as pickle
import message_filters

from sensor_msgs.msg import Image
import cv2
import open3d
import numpy as np
import visu
import matmanip as mmnip
import time
import rosinterface as IRos
import pointclouder

import aruco

import commandline

import StateManager

import json

import open3d

import pickler2 as pickle

import FileIO

import sys


def main(argv):
    

    
    freq=70

    camNames = IRos.getAllPluggedCameras()
    camName = camNames[0]

    camName="ervilhamigalhas"

    #fetch K of existing cameras on the files
    intrinsics = FileIO.getKDs(camNames)

    rospy.init_node('ora_ora_ora_ORAA', anonymous=True)

    arucoData = FileIO.getJsonFromFile("./static/ArucoWand.json")

    arucoData['IdMap'] = aruco.markerIdMapper(arucoData['ids'])

    arucoModel = FileIO.getFromPickle("pickles/wowww_raven_24-05-2019_02:12:35.pickle")

    pcer = PCGetter(camName,intrinsics,arucoModel,arucoData)

    camSub=[]
    #getting subscirpters to use message fitlers on

    camSub.append(message_filters.Subscriber(camName+"/rgb/image_color", Image))
    camSub.append(message_filters.Subscriber(camName+"/depth_registered/image_raw", Image))


    ts = message_filters.ApproximateTimeSynchronizer(camSub,10, 1.0/freq, allow_headerless=True)
    ts.registerCallback(pcer.callback)
    print("callbacks registered")




    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shut")


    print(filename)


class PCGetter(object):

    def __init__(self,camName,intrinsics,arucoModel,arucoData):
        print("initiated")

        self.camName = camName
        
        #intrinsic Params
        self.intrinsics = intrinsics

        self.arucoModel = arucoModel

        self.arucoData = arucoData

    def callback(self,*args):


        rgb = IRos.rosImg2RGB(args[0])
        depth_reg = IRos.rosImg2Depth(args[1])

        

        #cv2.imshow("wowee",rgb)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        K = self.intrinsics['K'][self.camName]

        #finds markers
        det_corners, ids, rejected = aruco.FindMarkers(rgb, K)

        

        sphs = []

        
        #GET CORNERS' XYZ
        if ids is not None:

            #print("shape ids")
            #print(ids.shape)
            ids = np.squeeze(ids)
            #print(ids.shape)
            #print(len(ids))

            #because there are 4 corners per detected aruco
            image_points=np.zeros((4*len(ids),2))

            points3D=np.zeros((4*len(ids),3))

            print("ids are")
            print(ids)

            for i in range(len(ids)):
                #print(det_corners[i])


                #print(self.arucoData['IdMap'])

                mappedID = self.arucoData['IdMap'][str(int(ids[i]))]

                
                #FROM CORNERS TO RGB
                #FROM CORNERS TO RGB
                corn1 = mmnip.Transform([self.arucoData['size']/2,-self.arucoData['size']/2,0],self.arucoModel['R'][mappedID],self.arucoModel['T'][mappedID])
                corn2 = mmnip.Transform([self.arucoData['size']/2,self.arucoData['size']/2,0],self.arucoModel['R'][mappedID],self.arucoModel['T'][mappedID])
                corn3 = mmnip.Transform([-self.arucoData['size']/2,self.arucoData['size']/2,0],self.arucoModel['R'][mappedID],self.arucoModel['T'][mappedID])
                corn4 = mmnip.Transform([-self.arucoData['size']/2,-self.arucoData['size']/2,0],self.arucoModel['R'][mappedID],self.arucoModel['T'][mappedID])
    
                corn3D = np.vstack((corn1,corn2,corn3,corn4))

                #image_points = np.flip(image_points,axis=1)

                #print("3D corners")
                #print(corn3D.shape)
                #print(det_corners[i])
                points3D[i*4:i*4+4,:] = corn3D
                image_points[i*4:i*4+4,:]=np.squeeze(det_corners[i])
                


            #print("ONE IS HERE")
            #print(image_points)
            #print(points3D)


            retval, orvec, otvec = cv2.solvePnP(points3D,image_points,K,None, flags = cv2.SOLVEPNP_ITERATIVE)

            rvec,_ = cv2.Rodrigues(orvec)

            sphere1 = open3d.create_mesh_sphere(0.01)
            H = mmnip.Rt2Homo(rvec,otvec.T)
          

            sphere1.transform(H)
            sphere1.paint_uniform_color([1,0,0])
            sphs.append(sphere1)
            refe = open3d.create_mesh_coordinate_frame(0.1, origin = [0, 0, 0])
            refe.transform(H)   #Transform it according tom p
            sphs.append(refe)

            
            
            #print(retval)
            #print(orvec)
            #print(otvec)


        #copy image
        hello = rgb.astype(np.uint8).copy() 

        #draw maerkers
        hello = cv2.aruco.drawDetectedMarkers(hello,det_corners,ids)

        cv2.imshow("wow",hello)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        pointsu = np.empty((3,0))
        

        for cor in det_corners:
        
            for i in range(0,4):
                    
                point = mmnip.singlePixe2xyz(depth_reg,cor[0,i,:],K)
                
                point = np.expand_dims(point,axis=1)
                
                sphere = open3d.create_mesh_sphere(0.006)
                H = np.eye(4)
                H[0:3,3]=point.T

                sphere.transform(H)
                sphere.paint_uniform_color([1,0,1])

                sphs.append(sphere)
                pointsu=np.hstack((pointsu,point))

        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(det_corners,0.0875,K,np.array([0,0,0,0])) #739 works
    

        tvecs=np.squeeze(tvecs)

        for i in range(0,tvecs.shape[0]):

            sphere = open3d.create_mesh_sphere(0.006)
            H = np.eye(4)
            H[0:3,3]=tvecs[i,:]

            sphere.transform(H)
            sphere.paint_uniform_color([0,0,1])

            sphs.append(sphere)

        

        #points,colors = mmnip.depthimg2xyz(depth_reg,rgb,self.intrinsics['K'][self.camNames[camId]])
        points = mmnip.depthimg2xyz2(depth_reg,K)
        points = points.reshape((480*640, 3))


        
        #print(colors.shape)
        rgb1 = rgb.reshape((480*640, 3))#colors
        
        pc = pointclouder.Points2Cloud(points,rgb1)

        pc2 = pointclouder.Points2Cloud(pointsu.T)

        pc2.paint_uniform_color([1,0,1])
        

        open3d.draw_geometries([pc]+sphs)


            


if __name__ == '__main__':
    main(sys.argv)