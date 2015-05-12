#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath) 
from common.common import GetConfigs
from common.camera import Camera 

class CameraEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        #serino = "56c051e1"
        if len(sys.argv)>1:         
            serino = sys.argv[1] 
        cls.mod = Camera(serino, "Camera")
        cls.mod_cfg = GetConfigs("Camera")
        cls.mod.test_times = 0
        cls.mod.dicttesttimes = cls.mod_cfg.get_test_times()
        for test_time in cls.mod.dicttesttimes: cls.mod.test_times += int(cls.mod.dicttesttimes[test_time])

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('CameraEndurance Mission Complete')  
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        Rate = cls.mod.suc_times/cls.mod.test_times*100
        if Rate < 95 :
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(Rate) + '%')

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testCamera(self):
        test_times = int(self.mod.dicttesttimes.get("take_pic".lower()))
        self.mod.enter()
        for i in range(test_times):
            self.mod.logger.debug("Take pic with back camera.")
            self.mod.logger.debug(self.mod.product)
            if self.mod.product == "Sprints":
                if self.mod.take_photo():
                    self.mod.del_picture()
                    self.mod.back_to_camera()
                else:
                    continue               
            else:
                if self.mod.switch_picker("back") and self.mod.take_photo():
                    self.mod.del_picture()
                    self.mod.back_to_camera()
                else:
                    continue
                if self.mod.switch_picker("front") and self.mod.take_photo():
                    self.mod.del_picture()
                    self.mod.back_to_camera()
                else:
                    continue
            self.mod.logger.info("Trace Success Loop %s." % (i+1))
            self.mod.suc_times = self.mod.suc_times + 1

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(CameraEndurance)  
    suite = unittest.TestSuite([suite1]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
