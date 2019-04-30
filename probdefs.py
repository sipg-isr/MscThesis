"""
probdefs.py

This module contains all the problem definitions
"""

import numpy as np


def rotationProbDef(observations,N):
    '''Problem Definition for getting Rotations between a set of referentials

    Ident*x = A*x <=> (Ident-A)x=0

    Args:   
        observations(dict): dictionary containing all the observation to build the problem with
        N(int): Number of rotations to determine

    Returns:
        Ident-A (numpy.array(3*N_obs,N*3): Matrix of the equation Cx=0 where x are the stacked rotations to be determined 
    '''

    #creates the left matrix in the problem formulation
    Ident = np.zeros((len(observations)*3,N*3))


    #creates the right matrix in the problem formulatin
    A = np.zeros((len(observations)*3,N*3))
            
    cnt = 0
    for obs in observations:
        

        if obs['to'] > 12 or obs['from'] > 12:
            print("skippity: weird index found")
            continue

        #fills the matrices according to the observed pairs
        Ident[cnt*3:cnt*3+3,obs['to']*3:obs['to']*3+3]= np.eye(3)
        A[cnt*3:cnt*3+3,obs['from']*3:obs['from']*3+3]= obs['R']

        #print("from camera:"+str(obs['from'])+" to camera:"+str(obs['to']))
        #print(obs['R'])
        #raw_input()

        cnt=cnt+1

    return Ident - A




def translationProbDef(observations,rotRel,N):
    '''Problem Definition for getting Rotations between a set of referentials

    (Ident-A)x=b

    Args:   
        observations - observations fecthed from the camera or synthetic
        rotRel - rotatios relative to the world
        N - number of markers

    Returns:
        Ident-A (numpy.array(3*N_obs,N*3): Matrix of the equation (Ident-A)x=b where x are the stacked translations to be determined 
        b (numpy array) : List 

    '''


    #creates the left matrix in the problem formulation
    Ident = np.zeros((len(observations)*3,N*3))

    #creates the right matrix in the problem formulatin
    A = np.zeros((len(observations)*3,N*3))

    #initializes b
    b = np.zeros((len(observations)*3,1))
            
    cnt = 0

    #for each observation set up a line (3 of them actually) of the problem definition
    for obs in observations:


        if obs['to'] > 12 or obs['from'] > 12:
            print("skippity: weird index found")
            continue

        #See problem definition in my thesis in order to understand this black magic
        Ident[cnt*3:cnt*3+3,obs['to']*3:obs['to']*3+3]= np.eye(3)
        A[cnt*3:cnt*3+3,obs['from']*3:obs['from']*3+3]=  np.eye(3)
        
        b[cnt*3:cnt*3+3,0]=-np.dot( rotRel[obs['to']],obs['t'])

        cnt=cnt+1
    
    return Ident - A ,b
