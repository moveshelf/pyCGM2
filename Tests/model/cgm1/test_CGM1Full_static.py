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
from pyCGM2 import log; log.setLoggingLevel(logging.INFO)

# btk
pyCGM2.CONFIG.addBtk()

# pyCGM2
from pyCGM2.Tools import  btkTools
from pyCGM2.Model.CGM2 import cgm
from pyCGM2.Model import  modelFilters,modelDecorator, frame
import pyCGM2.enums as pyCGM2Enums




class CGM1_calibrationTest():


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
        csp = modelFilters.ModelCoordinateSystemProcedure(model)

        csdf = modelFilters.CoordinateSystemDisplayFilter(csp,model,acqStatic)
        csdf.setStatic(True)
        csdf.display()

        btkTools.smartWriter(acqStatic,"upperLimb_calib.c3d")


        # joint centres
        #np.testing.assert_almost_equal(acqStatic.GetPoint("LCLO").GetValues().mean(axis=0),acqStatic.GetPoint("LSJC").GetValues().mean(axis=0),decimal = 3)
        #np.testing.assert_almost_equal(acqStatic.GetPoint("LHUO").GetValues().mean(axis=0),acqStatic.GetPoint("LEJC").GetValues().mean(axis=0),decimal = 3)
        #np.testing.assert_almost_equal(acqStatic.GetPoint("LCLO").GetValues().mean(axis=0),acqStatic.GetPoint("LSJC").GetValues().mean(axis=0),decimal = 3)




if __name__ == "__main__":



    CGM1_calibrationTest.CGM1_fullUpperLimb()



    logging.info("######## PROCESS CGM1 --> Done ######")
