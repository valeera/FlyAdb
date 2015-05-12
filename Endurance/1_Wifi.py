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
from common.settings import Wifi
from common.statusbar import StatusBar
      
class WifiEndurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        #serino = "a7c0c6cf"
        if len(sys.argv)>1:       
            serino = sys.argv[1] 
        cls.mod = Wifi(serino, "Set_WifiConnect")
        cls.sb = StatusBar(cls.mod.device, "sb_WifiConnect")
        cls.mod_cfg = GetConfigs("WifiConnect")
        cls.mod.test_times = 0
        cls.mod.dicttesttimes = cls.mod_cfg.get_test_times()
        for test_time in cls.mod.dicttesttimes: cls.mod.test_times += int(cls.mod.dicttesttimes[test_time])

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('WIFI Mission Complete')  
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

    def testWifiINSetting(self):
        test_times = int(self.mod.dicttesttimes.get("Wifi_in_set".lower()))
        self.mod.enter()
        for i in range(test_times):
            if self.mod._switch():
                if self.mod.device(scrollable=True).exists:
                    self.mod.device(scrollable=True).scroll.vert.toBeginning(steps=10)
                if self.mod.device(text="Connected").wait.exists(timeout=10000):
                    self.mod.logger.debug('wifi connect success!!!')
                    self.mod.device.delay(10)
            else:
                self.mod.logger.warning("Cannot connect wifi")
                self.mod.save_fail_img()
            if self.mod._switch():
                self.mod.suc_times = self.mod.suc_times + 1
                self.mod.logger.info("Trace Success Loop %s." % (i+1))
                self.mod.device.delay(10)
            else:
                self.mod.logger.warning("Close wifi failed.")
                self.mod.save_fail_img()
            
    def testWifiINStatusBar(self):
        test_times = int(self.mod.dicttesttimes.get("wifi_in_status".lower()))
        if self.sb.drag_down():
            for i in range(test_times):
                self.sb.switch_wifi()
                if self.sb.device(text="Wi-Fi").wait.gone(timeout=10000):
                    self.sb.logger.debug('wifi connect success!!!')
                    self.sb.device.delay(10)
                else:
                    self.mod.logger.warning("Cannot connect wifi")
                    self.mod.save_fail_img()    
                if self.sb.switch_wifi():
                    self.mod.suc_times = self.mod.suc_times + 1
                    self.sb.logger.info("Trace Success Loop %s." % (i+1))
                    self.sb.device.delay(10)
                else:
                    self.sb.logger.warning("Close wifi failed.")
                    self.sb.save_fail_img()
        
if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(WifiEndurance)  
    suite = unittest.TestSuite([suiteCase]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    