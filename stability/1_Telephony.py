#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath) 
from common.telephony import Telephony
from common.settings import Settings

class TestTelephony(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
#         serino = "adede7a6"
        if len(sys.argv)>1:       
            serino = sys.argv[1] 
        cls.mod = Telephony(serino, "Telephony")
        cls.set = Settings(cls.mod.device, "Settings")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Telephony Mission Complete')  
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

    def testCall2G(self):
        if int(self.mod.dicttesttimes.get("Contact2G".lower())) != 0:
            self.set.switch_network("2G")
        self.mod.call_contact(int(self.mod.dicttesttimes.get("Contact2G".lower())))
        self.mod.call_callLog(int(self.mod.dicttesttimes.get("CallLog2G".lower())))
            
    def testCall3G(self):
        if int(self.mod.dicttesttimes.get("Contact3G".lower())) != 0:
            self.set.switch_network("3G")
        self.mod.call_contact(int(self.mod.dicttesttimes.get("Contact3G".lower())))
        self.mod.call_callLog(int(self.mod.dicttesttimes.get("CallLog3G".lower()))) 
           
    def testCallLTE(self):
        if int(self.mod.dicttesttimes.get("ContactLTE".lower())) != 0:
            self.set.switch_network("ALL")
        self.mod.call_contact(int(self.mod.dicttesttimes.get("ContactLTE".lower())))
        self.mod.call_callLog(int(self.mod.dicttesttimes.get("CallLogLTE".lower())))
 
    def testContacts(self):
        self.mod.delete_contact(int(self.mod.dicttesttimes.get("DelTimes".lower())))                                
        self.mod.add_contact(int(self.mod.dicttesttimes.get("AddTimes".lower()))) 
                              
if __name__ == '__main__':

    suiteCase = unittest.TestLoader().loadTestsFromTestCase(TestTelephony)  
    suite = unittest.TestSuite([suiteCase]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    

