# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 12:46:40 2016

@author: Fabien Leboeuf ( Salford Univ, UK)
"""

import numpy as np
import scipy as sp

import pdb
import logging

import pyCGM2
from pyCGM2 import log; log.setLoggingLevel(logging.DEBUG)

# btk
pyCGM2.CONFIG.addBtk()

# pyCGM2
from pyCGM2.Tools import  btkTools
from pyCGM2.Model.CGM2 import cgm
from pyCGM2.Model import  modelFilters,modelDecorator, frame
from pyCGM2 import enums



class CGM1_angleTest():


    @classmethod
    def CGM1_fullUpperLimb(cls):

        MAIN_PATH = pyCGM2.CONFIG.TEST_DATA_PATH + "CGM1\\CGM1-TESTS\\full-PiG\\"
        staticFilename = "PN01NORMSTAT.c3d"

        acqStatic = btkTools.smartReader(str(MAIN_PATH +  staticFilename))

        model=cgm.CGM1UpperLimbs()
        model.configure()


        markerDiameter=14
        mp={
        'LeftShoulderOffset'   : 50,
        'LeftElbowWidth' : 91,
        'LeftWristWidth' : 56 ,
        'LeftHandThickness' : 28 ,
        'RightShoulderOffset'   : 45,
        'RightElbowWidth' : 90,
        'RightWristWidth' : 55 ,
        'RightHandThickness' : 30         }
        model.addAnthropoInputParameters(mp)

         # -----------CGM STATIC CALIBRATION--------------------
        scp=modelFilters.StaticCalibrationProcedure(model)

        modelFilters.ModelCalibrationFilter(scp,acqStatic,model).compute()



        # --- motion ----
        gaitFilename="PN01NORMSS01.c3d"
        acqGait = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))


        modMotion=modelFilters.ModelMotionFilter(scp,acqGait,model,enums.motionMethod.Determinist)
        modMotion.compute()

        csp = modelFilters.ModelCoordinateSystemProcedure(model)
        csdf = modelFilters.CoordinateSystemDisplayFilter(csp,model,acqGait)
        csdf.setStatic(False)
        csdf.display()

        modelFilters.ModelJCSFilter(model,acqGait).compute(description="vectoriel", pointLabelSuffix="cgm1_6dof")

        btkTools.smartWriter(acqGait,"upperLimb_angle.c3d")

        angleLabel = "LShoulderAngles"
        import matplotlib.pyplot as plt
        f, (ax1, ax2,ax3) = plt.subplots(1, 3)
        ax1.plot(acqGait.GetPoint(angleLabel).GetValues()[:,0],"-b")
        ax1.plot(acqGait.GetPoint(angleLabel+"_cgm1_6dof").GetValues()[:,0],"-r")

        ax2.plot(acqGait.GetPoint(angleLabel).GetValues()[:,1],"-b")
        ax2.plot(acqGait.GetPoint(angleLabel+"_cgm1_6dof").GetValues()[:,1],"-r")

        ax3.plot(acqGait.GetPoint(angleLabel).GetValues()[:,2],"-b")
        ax3.plot(acqGait.GetPoint(angleLabel+"_cgm1_6dof").GetValues()[:,2],"-r")

        plt.show()




    @classmethod
    def CGM1_fullbody(cls):

        MAIN_PATH = pyCGM2.CONFIG.TEST_DATA_PATH + "CGM1\\CGM1-TESTS\\full-PiG\\"
        staticFilename = "PN01NORMSTAT.c3d"

        # CALIBRATION ###############################
        acqStatic = btkTools.smartReader(str(MAIN_PATH +  staticFilename))

        markerDiameter=14

        # Lower Limb
        mpLower={
        'Bodymass'   : 83,
        'LeftLegLength' : 874,
        'RightLegLength' : 876.0 ,
        'LeftKneeWidth' : 106.0,
        'RightKneeWidth' : 103.0,
        'LeftAnkleWidth' : 74.0,
        'RightAnkleWidth' : 72.0,
        'LeftSoleDelta' : 0,
        'RightSoleDelta' : 0}

        model=cgm.CGM1LowerLimbs()
        model.configure()
        model.addAnthropoInputParameters(mpLower)

        scp=modelFilters.StaticCalibrationProcedure(model) # load calibration procedure

        modelFilters.ModelCalibrationFilter(scp,acqStatic,model,
                                            leftFlatFoot = True,
                                            rightFlatFoot = True,
                                            markerDiameter = 14,
                                            viconCGM1compatible=True
                                            ).compute()

        # ----- UpperLimb
        mpUpper={
        'LeftShoulderOffset'   : 50,
        'LeftElbowWidth' : 91,
        'LeftWristWidth' : 56 ,
        'LeftHandThickness' : 28 ,
        'RightShoulderOffset'   : 45,
        'RightElbowWidth' : 90,
        'RightWristWidth' : 55 ,
        'RightHandThickness' : 30 }

        modelUL=cgm.CGM1UpperLimbs()
        modelUL.configure()
        modelUL.addAnthropoInputParameters(mpUpper)


        scpul=modelFilters.StaticCalibrationProcedure(modelUL)
        modelFilters.ModelCalibrationFilter(scpul,acqStatic,modelUL).compute()


        # MOTION ###############################
        gaitFilename="PN01NORMSS01.c3d"
        acqGait = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))


        # lowerLimbModel
        modMotion=modelFilters.ModelMotionFilter(scp,acqGait,model,enums.motionMethod.Determinist,
                                      markerDiameter=14,
                                      viconCGM1compatible=False)
        modMotion.compute()


        # upperLimbModel
        modMotionUL=modelFilters.ModelMotionFilter(scpul,acqGait,modelUL,enums.motionMethod.Determinist)
        modMotionUL.compute()


        cgm.computeRelativeThoraxAngle(acqGait,modelUL,model,pointLabelSuffix="cgm1_6dof")


        csp = modelFilters.ModelCoordinateSystemProcedure(model)
        csdf = modelFilters.CoordinateSystemDisplayFilter(csp,model,acqGait).display()

        cspul = modelFilters.ModelCoordinateSystemProcedure(modelUL)
        csdful = modelFilters.CoordinateSystemDisplayFilter(cspul,modelUL,acqGait).display()

        btkTools.smartWriter(acqGait,"fullbody.c3d")

        angleLabel = "SpineAngles"
        import matplotlib.pyplot as plt
        f, (ax1, ax2,ax3) = plt.subplots(1, 3)
        ax1.plot(acqGait.GetPoint("L"+angleLabel).GetValues()[:,0],"-r")
        ax1.plot(acqGait.GetPoint("R"+angleLabel).GetValues()[:,0],"-b")
        ax1.plot(acqGait.GetPoint("L"+angleLabel+"_cgm1_6dof").GetValues()[:,0],"-g")
        ax1.plot(acqGait.GetPoint("R"+angleLabel+"_cgm1_6dof").GetValues()[:,0],"+g")

        ax2.plot(acqGait.GetPoint("L"+angleLabel).GetValues()[:,1],"-r")
        ax2.plot(acqGait.GetPoint("R"+angleLabel).GetValues()[:,1],"-b")
        ax2.plot(acqGait.GetPoint("L"+angleLabel+"_cgm1_6dof").GetValues()[:,1],"-g")
        ax2.plot(acqGait.GetPoint("R"+angleLabel+"_cgm1_6dof").GetValues()[:,1],"+g")

        ax3.plot(acqGait.GetPoint("L"+angleLabel).GetValues()[:,2],"-r")
        ax3.plot(acqGait.GetPoint("R"+angleLabel).GetValues()[:,2],"-b")
        ax3.plot(acqGait.GetPoint("L"+angleLabel+"_cgm1_6dof").GetValues()[:,2],"-g")
        ax3.plot(acqGait.GetPoint("R"+angleLabel+"_cgm1_6dof").GetValues()[:,2],"+g")

        plt.show()



if __name__ == "__main__":



    CGM1_angleTest.CGM1_fullUpperLimb()
    #CGM1_angleTest.CGM1_fullbody()



    logging.info("######## PROCESS CGM1 --> Done ######")
