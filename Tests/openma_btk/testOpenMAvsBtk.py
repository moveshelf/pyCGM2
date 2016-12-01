# -*- coding: utf-8 -*-
"""
Created on Thu Dec 01 12:20:50 2016

@author: Fabien Leboeuf ( Salford Univ, UK)
"""


import pdb
import logging
import matplotlib.pyplot as plt 

try:
    import pyCGM2.pyCGM2_CONFIG
    pyCGM2.pyCGM2_CONFIG.setLoggingLevel(logging.INFO)
    pyCGM2.pyCGM2_CONFIG.addOpenma()

except ImportError:
    logging.error("[pyCGM2] : pyCGM2 module not in your python path")

    
# openMA
import ma.io
import ma.body
import ma.instrument

# btk
import btk

# pyCGM2
from pyCGM2.Core.Tools import btkTools, trialTools 


class openmaVsBtk_test(): 

    @classmethod
    def smartAppendMarker(cls):  
 
        MAIN_PATH = pyCGM2.pyCGM2_CONFIG.TEST_DATA_PATH + "operations\\miscellaneous\\"
        filename = "static.c3d" 
    
        # btk ---
        acqBtk = btkTools.smartReader(str(MAIN_PATH +  filename))                   
        valSACR=(acqBtk.GetPoint("LPSI").GetValues() + acqBtk.GetPoint("RPSI").GetValues()) / 2.0        
        btkTools.smartAppendPoint(acqBtk,"SACR",valSACR,desc="")  
        btkTools.smartWriter(acqBtk, str(MAIN_PATH + filename[:-4]+"_btk.c3d"))

        # openma ---
        trial = trialTools.readC3d(str(MAIN_PATH +  filename))
        valSACR_2=(trial.findChild(ma.T_TimeSequence, "LPSI").data()+ trial.findChild(ma.T_TimeSequence, "RPSI").data()) / 2.0
        trialTools.smartAppendTimeSequence(trial,"SACR",valSACR_2,desc="")
        trialTools.writeC3d(trial,str(MAIN_PATH + filename[:-4]+"_openma2.c3d"))

    @classmethod
    def forcePlateExtractor(cls):
        MAIN_PATH = pyCGM2.pyCGM2_CONFIG.TEST_DATA_PATH + "operations\\miscellaneous\\"
        filename = "gait.c3d" 
        
        acqBtk = btkTools.smartReader(str(MAIN_PATH +  filename))                   
        # --- ground reaction force wrench ---
        pfe = btk.btkForcePlatformsExtractor()
        grwf = btk.btkGroundReactionWrenchFilter()
        pfe.SetInput(acqBtk)
        pfc = pfe.GetOutput()
        grwf.SetInput(pfc)
        grwc = grwf.GetOutput()
        grwc.Update()

        grwc.GetItemNumber()
        pos= grwc.GetItem(0).GetPosition().GetValues()
        force= grwc.GetItem(0).GetForce().GetValues()
        moment= grwc.GetItem(0).GetMoment().GetValues()

        #openma
        trial = trialTools.readC3d(str(MAIN_PATH +  filename))        
        
        wrenches = []
        fps = trial.findChildren(ma.instrument.T_ForcePlate)
        for fp in fps:
            print fp.name()
            print fp.surfaceCorners()
            wrenches.append(fp.wrench(ma.instrument.Location_PointOfApplication))# Location_CentreOfPressure ))#Location_PointOfApplication))
       
#        
        plt.figure()
        plt.plot(pos[:,0],'-r')
        plt.plot(wrenches[0].data()[:,6],'+')
        
        plt.figure()
        plt.plot(force[:,0:3],'-r')
        plt.plot(wrenches[0].data()[:,0:3],'+')
###        
        plt.figure()
        plt.plot(moment[:,0],'-r')
        plt.plot(wrenches[0].data()[:,3],'+')


if __name__ == "__main__":
    plt.close("all")
    #openmaVsBtk_test.smartAppendMarker()
    openmaVsBtk_test.forcePlateExtractor()
     
    
    