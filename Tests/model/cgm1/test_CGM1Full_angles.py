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
import pyCGM2.enums as pyCGM2Enums



class CGM1_calibrationTest():


    @classmethod
    def basicCGM1(cls):

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
        csp = modelFilters.ModelCoordinateSystemProcedure(model)


        # --- motion ----
        gaitFilename="PN01NORMSS01.c3d"
        acqGait = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))


        modMotion=modelFilters.ModelMotionFilter(scp,acqGait,model,pyCGM2Enums.motionMethod.Determinist)
        modMotion.compute()

        csdf = modelFilters.CoordinateSystemDisplayFilter(csp,model,acqGait)
        csdf.setStatic(False)
        csdf.display()

        modelFilters.ModelJCSFilter(model,acqGait).compute(description="vectoriel", pointLabelSuffix="cgm1_6dof")

        btkTools.smartWriter(acqGait,"testUpperLimbMotionAngle1.c3d")

        angleLabel = "LNeckAngles"
        import matplotlib.pyplot as plt
        f, (ax1, ax2,ax3) = plt.subplots(1, 3)
        ax1.plot(acqGait.GetPoint(angleLabel).GetValues()[:,0],"-b")
        ax1.plot(acqGait.GetPoint(angleLabel+"_cgm1_6dof").GetValues()[:,0],"-r")

        ax2.plot(acqGait.GetPoint(angleLabel).GetValues()[:,1],"-b")
        ax2.plot(acqGait.GetPoint(angleLabel+"_cgm1_6dof").GetValues()[:,1],"-r")

        ax3.plot(acqGait.GetPoint(angleLabel).GetValues()[:,2],"-b")
        ax3.plot(acqGait.GetPoint(angleLabel+"_cgm1_6dof").GetValues()[:,2],"-r")

        plt.show()



        # # --- motion ----
        # gaitFilename="PN01NORMSS02.c3d"
        # acqGait = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))
        #
        #
        # modMotion=modelFilters.ModelMotionFilter(scp,acqGait,model,pyCGM2Enums.motionMethod.Determinist)
        # modMotion.compute()
        #
        # csdf = modelFilters.CoordinateSystemDisplayFilter(csp,model,acqGait)
        # csdf.setStatic(False)
        # csdf.display()
        #
        #
        # btkTools.smartWriter(acqGait,"testUpperLimbMotion2.c3d")

        # R_leftShankVicon = getViconRmatrix(10, acqGait, "LTIO", "LTIP", "LTIL", "ZXiY")
        # R_rightShankVicon = getViconRmatrix(10, acqGait, "RTIO", "RTIP", "RTIL", "ZXiY")
        #
        # np.testing.assert_almost_equal( R_leftShankProx,
        #                                 R_leftShankVicon, decimal =3)








if __name__ == "__main__":



    CGM1_calibrationTest.basicCGM1()



    logging.info("######## PROCESS CGM1 --> Done ######")
