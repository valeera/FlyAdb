#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath) 
from common.schedule import Schedule
from common.configs import GetConfigs     

class TestPim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
        #serino = "adede7a6"
        if len(sys.argv)>1:
            serino = sys.argv[1] 
        cls.mod = Schedule(serino, "Pim")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('PIM Mission Complete')  
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
     
    def testAddCalendar(self):
        times = int(self.mod.dicttesttimes.get("add_calendar",0))
#         self.assertTrue(times>0)
        self.mod.add_calendars(times)
       
    def testDelCalendar(self):
        times = int(self.mod.dicttesttimes.get("add_calendar",0))
#         self.assertTrue(times>0)
        self.mod.delete_calendars(times)
     
    def testAddAlarm(self):
        times = int(self.mod.dicttesttimes.get("add_alarm",0))
#         self.assertTrue(times>0)
        self.mod.add_alarms(times)
      
    def testDelAlarm(self):
        times = int(self.mod.dicttesttimes.get("del_alarm",0))
#         self.assertTrue(times>0)
        self.mod.delete_alarms(times)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suiteCase = loader.loadTestsFromTestCase(TestPim)
    loader.sortTestMethodsUsing = None
    suite = unittest.TestSuite([suiteCase]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    

