#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath) 
from common.message import Message
from common.settings import Settings

class TestMessage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        serino = "a541c694"
        if len(sys.argv)>1:         
            serino = sys.argv[1] 
        cls.mod = Message(serino, "Message")
        cls.set = Settings(cls.mod.device, "Settings")
    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Message Mission Complete')  
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
        
    def testFwdMsg2G(self):
        if int(self.mod.dicttesttimes.get("SMS2G".lower(),0)) != 0:
            #self.set.switch_network("2G")
            self.mod.enter()
        self.mod.case_forward_msg('Text',int(self.mod.dicttesttimes.get("SMS2G".lower(),0)))
        self.mod.case_forward_msg('Photo',int(self.mod.dicttesttimes.get("Pic2G".lower(),0)))
        self.mod.case_forward_msg('Video',int(self.mod.dicttesttimes.get("Video2G".lower(),0)))        
        self.mod.case_forward_msg('Audio',int(self.mod.dicttesttimes.get("Auiod2G".lower(),0)))
#   
    def testFwdMsg3G(self):
        if int(self.mod.dicttesttimes.get("SMS3G".lower(),0)) != 0:
            #self.set.switch_network("3G")
            self.mod.enter()
        self.mod.case_forward_msg('Text',int(self.mod.dicttesttimes.get("SMS3G".lower(),0)))
        self.mod.case_forward_msg('Photo',int(self.mod.dicttesttimes.get("Pic3G".lower(),0)))
        self.mod.case_forward_msg('Video',int(self.mod.dicttesttimes.get("Video3G".lower(),0)))        
        self.mod.case_forward_msg('Audio',int(self.mod.dicttesttimes.get("Auiod3G".lower(),0)))
#    
    def testFwdMsgLTE(self):
        if int(self.mod.dicttesttimes.get("SMSlTE".lower(),0)) != 0:
            #self.set.switch_network("ALL")
            self.mod.enter()
        self.mod.case_forward_msg('Text',int(self.mod.dicttesttimes.get("SMSlTE".lower(),0)))
        self.mod.case_forward_msg('Photo',int(self.mod.dicttesttimes.get("PicLTE".lower(),0)))
        self.mod.case_forward_msg('Video',int(self.mod.dicttesttimes.get("VideoLTE".lower(),0)))        
        self.mod.case_forward_msg('Audio',int(self.mod.dicttesttimes.get("AuiodLTE".lower(),0)))
     
    def testOpenMsg(self):
        times = int(self.mod.dicttesttimes.get("OpenTimes".lower(),0))
        self.mod.enter()
        self.mod.case_open_msg('Text',times)
        self.mod.case_open_msg('Photo',times)
        self.mod.case_open_msg('Video',times)
        self.mod.case_open_msg('Audio',times)
        
if __name__ == '__main__':

    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestMessage)  
#     suite2 = unittest.TestLoader().loadTestsFromTestCase(TestDictValueFormatFunctions)  
#     suite = unittest.TestSuite([suite1, suite2])  
    suite = unittest.TestSuite([suite1]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    

