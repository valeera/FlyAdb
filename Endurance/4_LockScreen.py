#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath)
from common.common import Common, GetConfigs
      
class LockScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        #serino = "56c05003"
        if len(sys.argv)>1:       
            serino = sys.argv[1] 
        cls.mod = Common(serino, "LockScreen")
        cls.mod_cfg = GetConfigs("LockScreen")
        cls.mod.test_times = 0
        cls.mod.dicttesttimes = cls.mod_cfg.get_test_times()
        for test_time in cls.mod.dicttesttimes: cls.mod.test_times += int(cls.mod.dicttesttimes[test_time])

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('LockScreen Mission Complete')  
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        Rate = cls.mod.suc_times/cls.mod.test_times*100
        if Rate < 95 :
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(Rate) + '%')

    def setUp(self):
        self.mod.back_to_home()

    def tearDown(self):
        self.mod.back_to_home()

    def testUnLockScreen(self):
        test_times = int(self.mod.dicttesttimes.get("Locktimes".lower()))
        for i in range(test_times):
            self.mod.device.press.power()
            self.mod.device.delay(3)
            self.mod.logger.debug("the %s time open the screen~" %(i+1))
            for j in range(3):
                if "mWakefulness=Awake" in self.mod.adb.shell("dumpsys power"):
                    self.mod.logger.debug("Device awake")
                    break
                self.mod.device.press.power()
                self.mod.device.delay(2)
            else:
                self.mod.logger.warning("Cannot wake device")
                self.mod.save_fail_img()
                continue
            self.mod.device.swipe(540,1845,540,45,steps=20)
            if self.mod.device(resourceId='com.tct.launcher:id/page_indicator').wait.exists(timeout=3000):
                self.mod.suc_times = self.mod.suc_times + 1
                self.mod.logger.info("Trace Success Loop %s." % (i+1))
                self.mod.device.delay(2)
            else:
                self.mod.logger.warning("The %s time Unlock failed."  %(i+1))
                self.mod.save_fail_img()
                              
if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(LockScreen)  
    suite = unittest.TestSuite([suiteCase]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    