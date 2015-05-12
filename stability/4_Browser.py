#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath) 
from common.browser import Browser
from common.settings import Settings
from common.configs import Configs
from common.chrome import Chrome
class TestBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        #serino = "adede7a6"
        cls.url = "http://122.225.253.188/"
        if len(sys.argv)>1:       
            serino = sys.argv[1] 
        if Configs("common").get("product","Info") == "Sprints":
            cls.mod = Chrome(serino, "Browser")
        else:
            cls.mod = Browser(serino, "Browser")
        cls.set = Settings(cls.mod.device, "Settings")
    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Browser Mission Complete')  
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
    
    def testStability2G(self):
        if int(self.mod.dicttesttimes.get("ATTPage2G".lower(),0)) != 0:
            #self.set.switch_network("2G")
            self.mod.enter()
        self.mod.visit_att(int(self.mod.dicttesttimes.get("ATTPage2G".lower(),0)))
        self.mod.navigate(self.url,int(self.mod.dicttesttimes.get("ATTPage2G".lower(),0)))
        self.mod.visit_topsite(int(self.mod.dicttesttimes.get("TopSites2G".lower(),0)))  

    def testStability3G(self):
        if int(self.mod.dicttesttimes.get("ATTPage3G".lower(),0)) != 0:
            #self.set.switch_network("3G")
            self.mod.enter()
        self.mod.visit_att(int(self.mod.dicttesttimes.get("ATTPage3G".lower(),0)))
        self.mod.navigate(self.url,int(self.mod.dicttesttimes.get("Navigate3G".lower(),0)))
        self.mod.visit_topsite(int(self.mod.dicttesttimes.get("TopSites3G".lower(),0)))
 
    def testStabilityLTE(self):
        if int(self.mod.dicttesttimes.get("ATTPageLTE".lower(),0)) != 0:
            #self.set.switch_network("ALL")
            self.mod.enter()
        self.mod.visit_att(int(self.mod.dicttesttimes.get("ATTPageLTE".lower(),0)))
        self.mod.navigate(self.url,int(self.mod.dicttesttimes.get("NavigateLTE".lower(),0)))
        self.mod.visit_topsite(int(self.mod.dicttesttimes.get("TopSitesLTE".lower(),0)))
                           
if __name__ == '__main__':

    suiteCase = unittest.TestLoader().loadTestsFromTestCase(TestBrowser)  
    suite = unittest.TestSuite([suiteCase]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    

