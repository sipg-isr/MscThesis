"""
CamPoseGetter.py

This module contains the a class receives all the images and observations of the cameras, and calculates stuff with it
"""

import numpy as np
import cv2
import aruco
import probdefs
import observationgenner as obsGen


class CamPoseGetter(object):
    def __init__(self,N_cams,arucoData,arucoModel,intrinsics,calc,Rcam=None):
      
        #number of camera
        self.N_cams = N_cams

        #Array where several camera images will be concatenated into
        self.images =  np.zeros((480,640*N_cams,3),dtype=np.uint8)

        #list of empty lists where observations will be saved (first dim tells camera, second dim is the observations for that cam)
        self.Allobs = [ [] for i in range(self.N_cams) ]

        #intrinsic Params
        self.intrinsics = intrinsics

        self.arucoData=arucoData

        #get aruco model
        self.R = arucoModel['R']

        #self.R = synth

        self.t = []

        for tt in arucoModel['t']:
            self.t.append(np.squeeze(tt))

        #Array where several camera images will be concatenated into
        self.images =  np.zeros((480,640*N_cams,3),dtype=np.uint8)

        
        #self.t = arucoModel['t']
        #print(self.t)
        #print("t is above")

        #0 is for R problem definition
        #1 is for t problem definition
        self.calc = calc    

        if(self.calc==0):
            print("R problem Definition")
        elif(self.calc==1):
            print("t problem Definition")
        else:
            print("SOMETHING WENT WRONG")

        #known camera rotations (if they exist)
        self.Rcam = Rcam

        #A.T A initialized
        self.ATA = np.zeros((N_cams*3,N_cams*3))

        #A.T b initialized
        self.ATb = np.zeros((N_cams*3,1)) 

        self.count=0

        self.lol=np.zeros((3,3))

        self.arucoData['idmap'] = markerIdMapper(arucoData['ids'])
        

    def markerIdMapper(arr):

    IdMap={}
    print(type(IdMap))
    for i in range(0,len(arr)):
        IdMap[str(arr[i])]=i
        print(type(IdMap))

    
    return IdMap
    
    def callback(self,*args):

        print(self.N_cams)
        print(len(args))
        print("YEET")

        #iterate throguh cameras
        for i in range(0,self.N_cams):
            img = roscv.rosImg2RGB(args[i])

            #get observations of this camera, and image with the detected markers and referentials shown
            obs, img = obsGen.Cam2ArucoObsMaker2(img,self.intrinsics['K'][i],self.intrinsics['D'][i],arucoData)

            #set image
            self.images[0:480,i*640:i*640+640,0:3]=img

            #get new observations of that camera
            self.Allobs[camId]=obs  # WRONG SHOULD IT BE concantenate lists OR =?

        #Generate Pairs from all of the camera observations
        obsR , obsT = obsGen.GenerateCameraPairObs(self.Allobs,self.R,self.t)

        #rotation problem
        if self.calc == 0:

            A = probdefs.rotationProbDef(obsR,self.N_cams)
            self.ATA = self.ATA + np.dot(A.T,A)

            if(self.N_cams)==2:
                self.lol = self.lol+probdefs.rotationProbDefN2(obsR,self.N_cams)
                self.count=self.count+1
        
        #translation problem
        elif self.calc ==1:

            
            A,b =  probdefs.translationProbDef(obsT,self.Rcam,self.N_cams)

            self.ATA = self.ATA + np.dot(A.T,A)
            self.ATb = self.ATb + np.dot(A.T,b)

        #set them all as unready
        self.gatherReady = np.zeros((self.N_cams),dtype=np.uint8)

        #clear observations
        self.Allobs = [ [] for i in range(self.N_cams) ]

        self.showImg()


    def showImg(self):
        '''Displays images from all cameras
        '''
        
        cv2.imshow("Image window ",self.images)           
        cv2.waitKey(1)
        

    def GatherImg(self,camId,img,obs):
        '''Gathers Images and observations from a specific camera

        Args:
            camId:from which camera this is coming
            img: the image that the camera is transmitting
            obs: the observations extracted from the image
        '''
        
        #set image
        self.images[0:480,camId*640:camId*640+640,0:3]=img
        
        #increment statistic
        self.gatherCounter[camId] = self.gatherCounter[camId] +1
        
        #set is as fetched
        self.gatherReady[camId]=1

        #get new observations of that camera
        self.Allobs[camId]=self.Allobs[camId] +obs  # WRONG SHOULD IT BE concantenate lists OR =?

        #if all camera have sent something
        if(np.sum(self.gatherReady)== self.N_cams):
            
            #Generate Pairs from all of the camera observations
            obsR , obsT = obsGen.GenerateCameraPairObs(self.Allobs,self.R,self.t)

            #rotation problem
            if self.calc == 0:

                A = probdefs.rotationProbDef(obsR,self.N_cams)
                self.ATA = self.ATA + np.dot(A.T,A)

                if(self.N_cams)==2:
                    self.lol = self.lol+probdefs.rotationProbDefN2(obsR,self.N_cams)
                    self.count=self.count+1
            
            #translation problem
            elif self.calc ==1:

                
                A,b =  probdefs.translationProbDef(obsT,self.Rcam,self.N_cams)

                self.ATA = self.ATA + np.dot(A.T,A)
                self.ATb = self.ATb + np.dot(A.T,b)

            #set them all as unready
            self.gatherReady = np.zeros((self.N_cams),dtype=np.uint8)

            #clear observations
            self.Allobs = [ [] for i in range(self.N_cams) ]


        



    



            

            
            
        
        




   