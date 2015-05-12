#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath)

from common.common import Common,connect_device,createlogger,create_folder
from common.browser import Browser
from common.camera import Camera
from common.telephony import Telephony
from common.message import Message
from common.configs import GetConfigs,Configs
from common.settings import Settings

class MultiTask(Common):
    def __init__(self,device,mod):
        self.device = connect_device(device)
        self.logger = createlogger(mod)
        self.log_path = create_folder()
        self.camera = Camera(self.device,"task_camera")
        self.product = Configs("common").get("product","Info") 
        if self.product == "Sprints":
            from common.chrome import Chrome
            self.browser = Chrome(self.device,"task_browser")
        else:
            self.browser = Browser(self.device,"Browser")
        self.tel = Telephony(self.device,"task_tel")
        self.message = Message(self.device,"task_message")
        self.settings = Settings(self.device,"switch_nw")
        self.suc_times = 0
        self.mod_cfg = GetConfigs(mod)
        self.test_times = 0
        self.dicttesttimes = self.mod_cfg.get_test_times()
        for test_time in self.dicttesttimes: self.test_times += int(self.dicttesttimes[test_time]) 
        self.test_times =  self.test_times*2 + 4
        self.logger.info("Trace Total Times " + str(self.test_times))  
                  
    def remove(self):
        self.logger.debug("remove all opened activities")
        self.device.press.menu()
        if self.device(description= "Clear all").wait.exists(timeout = 2000):
            self.device(description= "Clear all").click()
            self.device.delay(5)
            return True
        return False
        
    def start(self):
        self.logger.debug("Start Some activities")
        self.logger.debug("Launch Contacts")
        #self.tel.start_app("Contacts")
        self.tel.enter_contacts()
        self.device.delay(3)
        self.logger.debug("Launch Message")
        self.message.start_app("Messaging")
        self.device.delay(3)
        self.logger.debug("Launch Dialer")         
        #self.tel.start_app("Call")
        self.tel.enter_dialer()
        self.device.delay(3)
        self.logger.debug("Launch Camera")           
        self.camera.start_app("Camera")
        self.device.delay(3)
        self.logger.debug("Launch Browser")        
        #self.browser.start_app("Browser")
        self.browser.enter()
    def make_call(self,number):
        if self.tel.enter_dialer():
            try:
                if self.tel.call_from_dialer(number):
                    self.suc_times += 1
                    self.logger.info("Trace Success Make Call")
                    return True
                else:
                    self.save_fail_img()
                    return False
            except Exception,e:
                self.save_fail_img()
#                 common.common.log_traceback(traceback.format_exc())
                return False
    
    def end_call(self):
        self.logger.debug("end the call")
        if self.tel.end():
            self.suc_times += 1
            self.logger.info("Trace Success, call ended before return to call")
            return True
        elif self.return_to_call() and self.tel.end():
            self.logger.info("Trace Success, call ended before return to call")
            self.suc_times += 1
            return True
        return False
   
    def return_to_call(self):
        self.logger.debug("return to call activity")
        self.device.press("home")
        self.device.delay(1)
        self.device.open.notification()
        self.device.delay(2)
        if self.device(text = "Ongoing call").exists:
            self.device(text = "Ongoing call").click()
#             if self.tel.end():
            return True
        self.device.press.back()         
        self.logger.debug("return to call fail")
        return False
               
    def interaction(self,times):
        self.logger.debug("Switch applications "+ str(times)+" Times")
        for loop in range(times):
            try:
                self.device.press.recent()
                if self.device(resourceId='com.android.systemui:id/recents_view').wait.exists(timeout = 2000):                 
                    if self.product=="Sprints":
                        for i in range(3):
                            self.device.server.adb.shell("input swipe 350 400 350 1000")
                    else:
#                         self.device().fling.toBeginning(max_swipes=100)
                        for i in range(3):
                            self.device.server.adb.shell("input swipe 230 250 230 650")
                    self.device.delay(2)
                    if self.device(resourceId='com.android.systemui:id/recents_view').child(index=0).child(index=3).exists:
                        if self.product=="Sprints":
                            self.device.click(540,450)
                        else:
                            self.device.click(230,280)
                        self.device.delay(2)
                    if not self.device(resourceId='com.android.systemui:id/recents_view').exists:
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                    else:
                        self.logger.warning('Cannot switch to one activity')
                        self.save_fail_img()
                else:
                    self.logger.warning('Cannot switch to recent app activity')
                    self.save_fail_img()
            except Exception,e:
                self.save_fail_img()
#                 common.common.log_traceback(traceback.format_exc())
                self.back_to_home()

class TestMultiTask(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
#         serino = "adede7a6"
        if len(sys.argv)>1:         
            serino = sys.argv[1] 
        cls.mod = MultiTask(serino, "Tasking")
        #cls.mod.remove()
        #cls.mod.settings.switch_network("ALL")
        cls.mod.start()
        
    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Tasking Mission Complete')  
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
        
    def testInteractionWithCall(self):  
        if(self.mod.make_call(Configs("common").get("sdevice_num","Telephony"))):
            self.mod.interaction(int(self.mod.dicttesttimes.get('ITERATIONS'.lower())))
            self.mod.end_call()
            
    def testInteractionWithBrowser(self):
        if self.mod.browser.enter():
            self.mod.suc_times+=1
            self.mod.logger.info("Trace Success Loading web page")
        self.mod.interaction(int(self.mod.dicttesttimes.get('ITERATIONS'.lower())))
        if self.mod.browser.exit():
            self.mod.suc_times+=1
            self.mod.logger.info("Trace Success exit Browser")

if __name__ == '__main__':
 
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestMultiTask)  
#     suite2 = unittest.TestLoader().loadTestsFromTestCase(TestDictValueFormatFunctions)  
#     suite = unittest.TestSuite([suite1, suite2])  
    suite = unittest.TestSuite([suite1]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 

    