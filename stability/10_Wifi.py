#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath) 
from common.settings import Wifi

class TestWifi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        #serino = "adede7a6"
        if len(sys.argv)>1:         
            serino = sys.argv[1] 
        cls.mod = Wifi(serino, "Wifi")

    @classmethod
    def tearDownClass(cls):
        cls.mod.enter()
        cls.mod.close()
        cls.mod.back_to_home()
        cls.mod.logger.debug('Wifi Mission Complete')  
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        Rate = cls.mod.suc_times/cls.mod.test_times*100
        if Rate < 95 :
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(Rate) + '%')

    def setUp(self):
        pass

    def tearDown(self):
        self.mod.back_to_home()
 
    def testSwitchWifi(self):
        times = int(self.mod.dicttesttimes.get("SwitchTimes".lower(),0))
        self.mod.switch(times)
 
    def testConnectWifi(self):
        ssid = self.mod.config.getstr("wifi_name","Wifi","common")
        pwd = self.mod.config.getstr("wifi_password","Wifi","common")
        security = self.mod.config.getstr("wifi_security","Wifi","common")
        self.mod.logger.debug("connect wifi %s/%s." %(ssid,pwd))
        times = int(self.mod.dicttesttimes.get("ConnectTimes".lower(),0))
        self.mod.connect(ssid,pwd,security,times)

if __name__ == '__main__':
    suiteCase = unittest.TestLoader().loadTestsFromTestCase(TestWifi)  
    suite = unittest.TestSuite([suiteCase]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    

