import json
import numpy as np

def getKDs(camNames):
    K={}
    D={}

    for name in camNames:
        filedict = getJsonFromFile("./static/camcalib_" + name +".json")

        #if file does not exist
        if(filedict==None):
            filedict = getJsonFromFile("./static/camcalib_default.json")

        k = np.asarray(filedict['K'], dtype=np.float32)

        
        K[name]=k
        D[name]=np.asarray(filedict['D'], dtype=np.float32)

        intrinsic = {"K":K,"D":D}

    return intrinsic

def getJsonFromFile(filename):

    try:
        f=open(filename,"r")
    
        data = json.load(f)
        f.close()

        return data

    except IOError:
      print "Error: File does not appear to exist."
      return None