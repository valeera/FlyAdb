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
from common.settings import Airplane
from common.statusbar import StatusBar
      
class AirplaneEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        #serino = "56c05003"
        if len(sys.argv)>1:       
            serino = sys.argv[1] 
        cls.mod = Airplane(serino, "Set_airplane")
        cls.sb = StatusBar(cls.mod.device, "sb_airplane")
        cls.mod_cfg = GetConfigs("Airplane")
        cls.mod.test_times = 0
        cls.mod.dicttesttimes = cls.mod_cfg.get_test_times()
        for test_time in cls.mod.dicttesttimes: cls.mod.test_times += int(cls.mod.dicttesttimes[test_time])

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Airplane Mission Complete')  
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

    def testAPINSetting(self):
        test_times = int(self.mod.dicttesttimes.get("ap_in_set".lower()))
        self.mod.enter()
        for i in range(test_times):
            if not self.mod.switch():
                self.mod.save_fail_img()
            else:
                self.mod.device.delay(10)
            if self.mod.switch():
                self.mod.suc_times = self.mod.suc_times + 1
                self.mod.logger.info("Trace Success Loop %s." % (i+1))
                if self.mod.device(resourceId="com.android.stk:id/button_ok").wait.exists(timeout=20000):
                    self.mod.logger.debug("Confirm the USIM window")
                    self.mod.device(resourceId="com.android.stk:id/button_ok").click()
                    self.mod.device.delay(2)
            else:
                self.mod.save_fail_img()
            
                
    def testAPINStatusBar(self):
        test_times = int(self.mod.dicttesttimes.get("ap_in_status".lower()))
        if self.sb.drag_down():
            for i in range(test_times):
                if self.sb.switch_airplane():
                    self.sb.device.delay(10)
                else:
                    self.mod.save_fail_img()    
                if self.sb.switch_airplane():
                    self.mod.suc_times = self.mod.suc_times + 1
                    self.sb.logger.info("Trace Success Loop %s." % (i+1))
                    if self.mod.device(resourceId="com.android.stk:id/button_ok").wait.exists(timeout=20000):
                        self.mod.logger.debug("Confirm the USIM window")
                        self.mod.device(resourceId="com.android.stk:id/button_ok").click()
                        self.mod.device.delay(2)
                else:
                    self.sb.save_fail_img()
        
if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(AirplaneEndurance)  
    suite = unittest.TestSuite([suiteCase]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    