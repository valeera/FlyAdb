# -*- coding: UTF-8 -*-
"""Telephony library for scripts.
"""
import os
import sys
import time
# from common import Common
from common import *

class Telephony(Common):
    """Provide common functions for scripts, such as launching activity."""  
        
    def enter_dialer(self):
        '''Launch calender by start activity.
        '''
        self.logger.debug("Enter Dialer")
        if self.device(resourceId= self.appconfig.id("id_enter","Dialer")).exists:
            return True
        self.start_app(self.appconfig("name","Dialer"))
        self.device.delay(2)
        if self.device(resourceId= self.appconfig.id("id_enter","Dialer")).exists:
            return True
        else:
            return False
 
    def enter_contacts(self):
        self.logger.debug("Launch Contacts")
        if self.device(text = "All contacts").exists:
            self.device(text = "All contacts").click()
            self.device.delay(1)
            return True
        self.start_app(self.appconfig("name","Contacts"))
        self.device.delay(2)
        if self.device(text = "All contacts").exists:
            self.device(text = "All contacts").click()
            self.device.delay(1)
            return True
        self.logger.debug("Launch Contacts Fail")
        return False

    def back_to_contact(self):
        self.logger.debug('back to all contact')
        for loop in range(5):
            if self.device(text = "All contacts").exists:
                return True
            self.device.press.back() 
            self.device.delay(1)
        return False

    def setup_contacts(self):
        self.logger.debug("setup Contacts")
#         self.adb.cmd("push",os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"File"), '/sdcard/Music')
        self.enter_contacts()
        contacts = [
                {"id":{"description":"More options"}},
                {"id":"text","content":["Import/export","Import from storage","PHONE"]}
                ]

        store = [
                {"id":"description","content":"add new contact"},
                {"id":{"text":"PHONE"},"assert":False},
                {"id":{"text":"OK"},"assert":False},    
                ]
        UIParser.run(self, [contacts,store],self.back_to_contact)
        self.back_to_contact()
        return False

    def get_contacts_num(self):
        self.device(description = "More options").click()
        self.device.delay(1)
        self.device(resourceId = "android:id/title", text = "Delete").click()
        self.device.delay(1)
        if self.device(resourceId = "com.android.contacts:id/pick_contact_select_all").wait.exists(timeout = self.timeout):
            self.device(resourceId = "com.android.contacts:id/pick_contact_select_all").click()
            self.device.delay(1)
            num = self.device(resourceId = "com.android.contacts:id/selected_num").get_text()
        self.device.press.back()
        self.device.delay(2)
        return num
                
    def delete_all_contacts(self):
        self.logger.debug("delete all contacts")
        if self.device(className = "android.widget.ListView").getChildCount() == 2:
            return True
        while self.device(className = "android.widget.ListView").getChildCount() > 2:
            try:
                if self.device(text = "All contacts", selected = "false").exists:
                    self.device(text = "All contacts", selected = "false").click()
                    self.device.dealy(2)
                self.device(description = "More options").click()
                self.device.delay(1)
                self.device(resourceId = "android:id/title", text = "Delete").click()
                self.device.delay(1)
                if self.device(resourceId = "com.android.contacts:id/select_all_check").exists:                
                    self.device(resourceId = "com.android.contacts:id/select_all_check").click()
                    self.device.delay(1)
                    self.device(resourceId = "com.android.contacts:id/btn_ok").click()
                    self.device.delay(1)
                    self.device(resourceId = "android:id/button1", text = "OK").click()                
                    self.device.delay(2)
                    while self.device(text = "Delete all").exists:
                        self.device.delay(1)
                    if self.device(className = "android.widget.ListView").getChildCount() == 2:
                        return True
                self.logger.debug("delete all contacts fail")
                return False
            except Exception, e:
                self.save_fail_img()
                self.device.press.home()
                self.enter_contacts()
        self.logger.debug('Delete All contact complete')
        return True

    def end(self):
        if self.device(description='End').wait.exists(timeout=self.timeout):
            self.device(description='End').click()
            self.logger.debug('Outgoing call success from dialer')
            return True
        else:
            self.logger.debug('Outgoing call fail from dialer')
            return False

    def call_from_dialer(self,number):
        '''make a call from dialer
         argv:(str)number -- the number you want to call
        '''
        self.logger.debug("Dial Number %s." % number)
        
        step = [
                {"id":{"text":self.appconfig("speed_dial","Dialer")}},
                {"id":{"description":self.appconfig("dial_pad","Dialer")}},             
                {"id":{"resourceId":"com.android.dialer:id/digits"},"action":{"type":"set_text","param":[number]}},                
                {"id":{"description":self.appconfig("dialpad_name","Dialer")}}, 
                ]
        UIParser.run(self, step, self.back_to_contact)
        if self.device(description='End').wait.exists(timeout=self.timeout):
            self.logger.debug('Outgoing call success from dialer')
#             self.device(description='End').click()
            return True
        else:
            self.logger.debug('Outgoing call fail from dialer')
            return False        
        
        '''legency
        self.device(text='Speed dial').click()    
        self.device.delay(2)
        self.device(description ='Dial pad').click()
        self.device.delay(2)
        self.device(resourceId='com.android.dialer:id/digits').set_text(number)
        self.device.delay(2)
        self.device(description='Dial').click()
        self.device.delay(2)
        if self.device(description='End').wait.exists(timeout=self.timeout):
            self.logger.debug('Outgoing call success from dialer')
            return True
        else:
            self.logger.debug('Outgoing call fail from dialer')
            return False
        '''
       
    def _call_history(self):
        self.logger.debug('call from calllog')
        self.device(text=self.appconfig("recent","Dialer")).click()
        self.device.delay(2)
        if self.device(className = "android.widget.LinearLayout", index = 1).exists:
            self.device(className = "android.widget.LinearLayout", index = 1).click()
            self.device(text = "00:05").wait.exists(timeout = 10000)
#         if self.device(descriptionContains='Call').wait.exists(timeout=5000):
#             self.device(descriptionContains='Call').click()
#             self.device.delay(2)
        if self.device(description='End').wait.exists(timeout=self.timeout):
            self.logger.debug('Outgoing call success from dialer')
            self.device(description='End').click()
            self.device.delay(2)
            return True
        self.logger.debug('Outgoing call fail from dialer')
        return False
    
    def _call_contact(self,Index):
        '''select a contact for call
        '''
        contact_name = "Autotest%02d" % (Index+1)
        self.logger.debug('make call from contact %s' %contact_name)
        if self.device(text = "All contacts", selected = "false").exists:
            self.device(text = "All contacts").click()
            self.device.delay(2)
        self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
        self.device(scrollable=True).scroll.vert.to(textStartsWith=contact_name)
        if self.device(textStartsWith=contact_name).exists:
            self.device(textStartsWith=contact_name).click()
        else:
            self.logger.warning("Cannot find the contact %s" %contact_name)
            return False
        self.device.delay(2)
        self.device(resourceId='com.android.contacts:id/communication_card').click()
        self.device(text = "00:05").wait.exists(timeout = 10000)
        if self.device(description='End').wait.exists(timeout=self.timeout):
            self.device(description='End').click()
            self.device.press.back()
            return True
        self.logger.debug('make call from contact fail!!!')
        return False
       
    def call_answer(self):
        '''Pick up the incoming call
        '''
        if (self.device(text='Incoming call').wait.exists(timeout=45000)):
            self.logger.debug("Pick up the incoming call.")
            self.device.press_call()
            self.device.delay(2)
            if self.device(resourceId='com.android.dialer:id/elapsedTime').exists:
                self._logger.debug('Call success!!!' )
                return True
        self._logger.debug("incoming call fail!!!")
        return False
            
    def is_lte(self):
        '''check if it stays at lte network or not.
        '''
        observed_mode = self.adb.get_data_service_state()
        j = 0
        # Try to wait for 20 sec at most if state is unknown
        while observed_mode != 'LTE' and j < 10:
            self.device.sleep(2)
            j += 1
            observed_mode = self.adb.get_data_service_state()
        if observed_mode == 'LTE':
            self.logger.debug("Change to LTE.")
            return True
        else:
            self.logger.warning("Cannot change to LTE")
            return False
 
    def add_contact(self,times = 1):
        if times == 0:
            return 
        self.logger.debug("Add "+str(times)+" New Contact")
        self.enter_contacts()
        for loop in range(times):
            try:
                if not self.device(description = "add new contact").exists:
                    self.enter_contacts()      
                name = random_name(loop)       
                step = [
                        {"id":{"resourceId":"com.android.contacts:id/floating_action_button"}},
                        {"id":{"text":"Name","className":"android.widget.EditText"},"action":{"type":"set_text","param":[name]}},
                        {"id":{"text":"Phone","className":"android.widget.EditText"},"action":{"type":"set_text","param":[Configs("common").get("sdevice_num","Telephony")]}},               
                        {"id":{"description":"Done"}}           
                        ]
                if UIParser.run(self,step, self.back_to_contact)==True and self.device(text = name).wait.exists(timeout=self.timeout):
                    self.logger.info("Trace Success Loop "+str(loop+1))
                    self.suc_times += 1
                    self.back_to_contact()
                    self.device.delay(1)
                else:
                    self.save_fail_img()
                    self.back_to_contact()
            except Exception, e:
#                 self.device.log_traceback(traceback.format_exc())
                self.save_fail_img()
                self.back_to_contact()
        self.logger.debug('Add contact complete')
        
                       
    def delete_contact(self,times = 1):
        if times == 0:
            return 
        self.logger.debug("Delete Contact "+str(times)+" times")
        self.enter_contacts()
        self.device(scrollable=True).scroll.vert.toBeginning(steps=100, max_swipes=100)
        self.device.delay(1)
        for loop in range(times):
            try:
                if self.device(text = "All contacts").exists:     
                    self.device(resourceId="android:id/list").child(index=3).click()
                    contact_name = self.device(resourceId="com.android.contacts:id/large_title").get_text()
                    self.logger.debug("Get contact name is %s" %(contact_name))      
                    step = [
                            {"id":{"resourceId":'com.android.contacts:id/menu_edit'}},
                            {"id":{"description":'More options'}}, 
                            {"id":"text","content":['Delete','OK']},     
                            ]
                    UIParser.run(self, step, self.back_to_contact)
                    if not self.device(text = contact_name).exists:
                        self.logger.info("Trace Success Loop "+str(loop+1))
                        self.suc_times += 1
                        self.device.delay(1)
                    else:
                        self.logger.warning("Contact still existing")
                        self.save_fail_img()
                        self.back_to_contact()
                else:
                    self.logger.warning("Cannot find All contacts")
                    self.save_fail_img()
                    self.back_to_contact()
            except Exception, e:
                self.logger.warning(e)
                self.save_fail_img()
                self.back_to_contact()
        self.logger.debug('Delete contact complete')

    def call_contact(self,times=1):
        if times == 0:
            return 
        self.logger.debug("call_contact "+str(times)+" times")
        self.enter_contacts()
        self.temp_index = 0
        for loop in range(times):        
            try: 
                contact_index = loop%50               
                if self._call_contact(contact_index):
                    self.back_to_contact()
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop %s." % (loop+1))
                else:
                    self.back_to_contact()
                    self.logger.debug('calling has broken off')
                    self.save_fail_img()                    
            except Exception,e:
                self.save_fail_img()
    #                     common.log_traceback(traceback.format_exc())
                self.back_to_contact()

                    
    def call_callLog(self,times=1):
        if times == 0:
            return 
        self.logger.debug("call_callLog "+str(times)+" times")
        self.enter_dialer()
        for loop in range(times):        
            try:                
                if self._call_history():
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop %s." % (loop+1))
                else:
                    self.logger.debug('calling has broken off')
                    self.save_fail_img()                    
            except Exception,e:
                self.save_fail_img()
#                     common.log_traceback(traceback.format_exc())
                self.enter_dialer()
                      
         
if __name__ == '__main__':
    a = Telephony("e7cdca9a","Telephony")
    
    a.call_from_dialer(10010)
#     a.setup_contacts()                       
    