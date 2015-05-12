#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
import random
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath) 
from common.mail import Email
from common.settings import Settings

class TestEmail(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
#         serino = "adede7a6"
        if len(sys.argv)>1:       
            serino = sys.argv[1] 
        cls.mod = Email(serino, "Email")
        cls.set = Settings(cls.mod.device, "Settings")
    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Email Mission Complete')  
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        Rate = cls.mod.suc_times/cls.mod.test_times*100
        if Rate < 95 :
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(Rate) + '%')

    def setUp(self):
        self.receiver = random.choice(self.mod.config.getstr("Email_receiver","Email","common").split(","))

    def tearDown(self):
        self.mod.back_to_home()
 
    def testFWDMsg2G(self):
        if int(self.mod.dicttesttimes.get("SendBy2G".lower(),0)) != 0:
            #self.set.switch_network("2G")
            self.mod.enter()
        self.mod.send_email(self.receiver,False,int(self.mod.dicttesttimes.get("SendBy2G".lower(),0))) 
        self.mod.send_email(self.receiver,True,int(self.mod.dicttesttimes.get("SendBy2G".lower(),0)))    
  
    def testFWDMsg3G(self): 
        if int(self.mod.dicttesttimes.get("SendBy3G".lower(),0)) != 0:
            #self.set.switch_network("3G")
            self.mod.enter()
        self.mod.send_email(self.receiver,False,int(self.mod.dicttesttimes.get("SendBy3G".lower(),0))) 
        self.mod.send_email(self.receiver,True,int(self.mod.dicttesttimes.get("SendBy3G".lower(),0)))  
 
    def testFwdMsgLTE(self):
        if int(self.mod.dicttesttimes.get("SendByLTE".lower(),0)) != 0:
            #self.set.switch_network("ALL")
            self.mod.enter()
        self.mod.send_email(self.receiver,False,int(self.mod.dicttesttimes.get("SendByLTE".lower(),0))) 
        self.mod.send_email(self.receiver,True,int(self.mod.dicttesttimes.get("SendByLTE".lower(),0))) 
 
    def testOpenMails(self):
        self.mod.enter()
        self.mod.open_email(int(self.mod.dicttesttimes.get("opentimes".lower(),0)))
         
                              
if __name__ == '__main__':

    suiteCase = unittest.TestLoader().loadTestsFromTestCase(TestEmail)  
    suite = unittest.TestSuite([suiteCase]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    

