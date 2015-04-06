# -*- coding: UTF-8 -*-
"""Message library for scripts.
"""

import re
import sys
import os
from common import Common

class Message(Common):

    """Provide common functions for scripts, such as launching activity."""
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self.msgs = {'Audio':"4",'Video':"3",'Photo':"2",'Text':"1"}
                   
    def enter_message(self):
        """Launch browser.
        """
        self.logger.debug('enter Message')
        if self.device(resourceId= self.appconfig.id("Message","id_enter")).wait.exists(timeout=2000):
            return True
        self.start_app("Messaging")
        if self.device(resourceId= self.appconfig.id("Message","id_enter")).wait.exists(timeout=2000):
            return True
        else:
            self.logger.warning('Launch Message fail')
            return False
        return True
         
    def back_to_message(self):
        """back to message list .
        """  
        self.logger.debug('Back to message list')
        for i in range(5):
            if self.device(resourceId=self.appconfig.id("Message","id_enter")).exists:
                break
            self.device.press.back()
            self.device.delay(1)
            if self.device(text="OK").exists:
                self.device(text="OK").click()
        else:
            self.logger.warning('Back to message list fail')
            
    def sms_Send(self,number,content = ""):
        """send a message(SMS)
        argv: (str)number -- the telephone number you want to send
              (str)content -- SMS content
        """
        if self.enter_message():
            self.device(resourceId=self.appconfig.id("Message","id_new")).click()
            input_text = self.device(className='android.widget.MultiAutoCompleteTextView')
            if input_text.wait.exists(timeout = 2000):
                self.logger.debug('input phone number:'+str(number))
                input_text.set_text(str(number))
#             'Type Name or Number'
                self.device.delay(2)
                if content != "":
                    self.logger.debug('input sms content:'+content)
                    self.device(className='android.widget.EditText').click()
                    self.device.delay(2)
                #self._device.click(className='android.widget.EditText')
    #                 self._device.shell_dos("adb -s "+self._device.get_device_serial()+" shell input text "+content)
                    self.device(className='android.widget.EditText').set_text(content)
                    self.device.delay(2)
                self.logger.debug('send')
                self.device(resourceId=self.appconfig.id("Message","id_send")).click()
                self.device.delay(1)
            if not self.device(text='SENDING…').wait.exists(timeout == 10000):
#                 and (not self.device(resourceId ='com.android.mms:id/delivered_indicator').wait.exists(timeout=10000)) 
                self.logger.debug('SMS send success!!!')
                self.device.press.back()
                self.device.delay(1)
                self.back_to_message()
                return True
        self.logger.debug('SMS send fail!!!')
        self.back_to_message()
        self.device.delay(1)
        return False
    
    def mms_Send(self,number,content,subject,pic=None,video=None,audio=None):
        """send a message(MMS)
        argv: (str)number -- the telephone number you want to send
              (str)content -- MMS content
              (str)subject -- MMS subject
              pic\video\audio -- attachment of the message
        """
        if self.enter_message():
            self._device(resourceId='com.android.mms:id/action_compose_new').click()
            self._device.delay(2)
            self._logger.debug('input phone number:'+number)
            self._device(text='To').set_text(number)
            self._device.delay(3)
            self._logger.debug('input sms content:'+content)
            self._device(className='android.widget.EditText').click()
            self._device.delay(2)
            self._device.shell_dos("adb -s "+self._device.get_device_serial()+" shell input text "+content)
            self._device.delay(2)
            self._device.press.menu()
            self._device.delay(2)
            if self._device(text='Add subject').exists:
                self._device(text='Add subject').click()
                self._device.delay(3)
                self._device.press(41)
                self._device.press(41)
                self._device.press(47)
                self._device.delay(2)
            if self._device(resourceId='com.android.mms:id/attach_button_sms').exists:
                self._device(resourceId='com.android.mms:id/attach_button_sms').click()
                self._device.delay(1)
            if self._device(description ='Attach').exists:
                self._device(description ='Attach').click()
                self._device.delay(1)
                
            if pic!=None: 
                self._logger.debug('add a picture')
                self._device(text='Pictures').click()
                self._device.delay(2)
                if not self._device(text='File Manager').exists:
                    self._device(text='Recent').click()
                    self._device.delay(1)
                self._device(text='File Manager').click()
                self._device.delay(2)
                self._device(text='Phone storage').click()
                self._device.delay(2)
                self._logger.debug('drag 200,600,200,300')
                #self._device.shell_adb('shell input swipe 200 600 200 300')
                self._device(scrollable=True).scroll.vert.forward(steps=10)
                self._device.delay(2)
                maxloop=0
                while not self._device(textContains='Attachment').exists:
                    if maxloop>5:
                        self._logger.debug('Can not find Attachment folder')
                        return False
                    #self._device.shell_adb('shell input swipe 200 600 200 300')
                    self._device(scrollable=True).scroll.vert.forward(steps=10)
                    self._device.delay(2)
                    maxloop+=1
                self._device(textContains='Attachment').click()
                self._device.delay(1)
                self._device(textContains='jpg').click()
                self._device.delay(2)                 
            if video!=None:
                self._logger.debug('add a video')
                self._device(text='Videos').click()
                self._device.delay(2)
                if not self._device(text='File Manager').exists:
                    self._device(text='Recent').click()
                    self._device.delay(1)
                self._device(text='File Manager').click()
                self._device.delay(2)
                self._device(text='Phone storage').click()
                self._device.delay(2)
                maxloop=0
                while not self._device(textContains='Attachment').exists:
                    if maxloop>5:
                        self._logger.debug('Can not find Attachment folder')
                        return False
                    #self._device.shell_adb('shell input swipe 100 600 200 300')
                    self._device(scrollable=True).scroll.vert.forward(steps=10)
                    maxloop+=1
                self._device(textContains='Attachment').click()                
                self._device.delay(1)
                self._device(textContains='3gp').click()
                self._device.delay(2)                
            if audio!=None:
                self._logger.debug('add an audio')
                self._device(text='Audio').click()
                self._device.delay(1)
                self._device(text='External audio').click()
                self._device.delay(1)
                self._device(text='File Manager').click()
                self._device.delay(1)
                self._device(text='Just once').click()
                self._device.delay(1)
                self._device(text='Phone storage').click()
                maxloop=0
                while not self._device(textContains='Attachment').exists:
                    if maxloop>5:
                        self._logger.debug('Can not find Attachment folder')
                        return False
                    #self._device.shell_adb('shell input swipe 100 600 200 300')
                    self._device(scrollable=True).scroll.vert.forward(steps=10)
                    maxloop+=1
                self._device(textContains='Attachment').click()
                self._device.delay(2)
                self._device(textContains='3gpp').click()
                self._device.delay(2)                  
            self._logger.debug('send')    
            if self._device(text='Send').exists:            
                self._device(text='Send').click()
            if self._device(text='MMS').exists:            
                self._device(text='MMS').click()                
            self._device.delay(1)
            if (self._device(text='SENDING…').exists) and (not self._device(resourceId ='com.android.mms:id/delivered_indicator').wait.exists(timeout=10000)) and (self._device(textContains =':').wait.exists(timeout=300000)):
                self._logger.debug('MMS send success!!!')
                self._device.press.back()
                self._device.delay(1)
                self.back_to_message()
                return True
        self._logger.debug('MMS send fail!!!')
        self.back_to_message()
        self._device.delay(1)
        return False        
        
    def del_all_message(self):
        """delete all message in current list
        """
        self.logger.debug('delete all message')
        self.device(description=self.appconfig("Message","options")).click()
        if self.device(text=self.appconfig("Message","delete_all_action")).wait.exists(timeout = 2000):
            self.device(text=self.appconfig("Message","delete_all_action")).click()
            if self.device(resourceId=self.appconfig.id("Message","id_select_all")).wait.exists(timeout = 2000):          
                self.device(resourceId=self.appconfig.id("Message","id_select_all")).click()
                self.device.delay(2)            
                self.device(description=self.appconfig("Message","delete_action")).click()
                if self.device(text=self.appconfig("Message","delete_confirm")).wait.exists(timeout = 2000):
                    self.device(text=self.appconfig("Message","delete_confirm")).click()
                    self.logger.debug('message delete success!')
                    return True
        self.logger.debug('message delete fail!')
        return False
   
    def _verify_msg_sending(self):
        """verify whether the message has received
        argv: (str)mdevice_NO -- the telephone number of the sender
              (str)content -- MMS content
        """
        if self.device(text='SENDING…').exists:
            if self.device(text='SENDING…').wait.gone(timeout = 10000):
                if self.device(resourceId='com.android.mms:id/date_view').exists:
                    self.logger.debug('message send success!')
                    return True
            self.logger.debug('message send fail!!!')
            return False 
        elif self.device(resourceId='com.android.mms:id/date_view').exists:
            self.logger.debug('message send success!')
            return True
        else:
            self.logger.debug('message send fail!!!')
            return False
    
    def select_msg(self,strtype):
        """select message by specified index.
        
        argv: (int)index -- message order in the list_node
              (str)strtype -- for stability test. 
                              msgs = {'Audio':0,'Video':1,'Photo':2,'Text':3}
        """
        if self.device(resourceId='com.android.mms:id/from',text = self.msgs[strtype]).exists:
            if self.device(resourceId='com.android.mms:id/from',text = self.msgs[strtype]).click():
                if self.device(resourceId='com.android.mms:id/history').wait.exists(timeout = 2000):
                    return True
                else:
                    self.logger.debug('select message fail!!!')
                return False
        return True

    def fwd_msg(self,type,number):
        """Long touch a msg in tread screen and select the option.
        
        argv: (str)str_option -- option dispaly in the popup menu.
        """
        self.logger.debug("Select message option %s." %(type))
        
        self.select_msg(type)
        self.device(resourceId="com.android.mms:id/msg_list_item").long_click()
        if self.device(resourceId="com.android.mms:id/forward").wait.exists(timeout = 2000):
            self.device(resourceId="com.android.mms:id/forward").click()
            input_text = self.device(className='android.widget.MultiAutoCompleteTextView')
            if input_text.wait.exists(timeout = 2000):
                self.logger.debug('input phone number:'+str(number))
                input_text.set_text(str(number))
                self.device.delay(1)
                self.logger.debug('send')
                if type == "Text":
                    if self.device(resourceId=self.appconfig.id("Message","id_sms_send")).wait.exists(timeout = 3000):
                        self.device(resourceId=self.appconfig.id("Message","id_sms_send")).click()
                else:
                    if self.device(resourceId=self.appconfig.id("Message","id_mms_send")).wait.exists(timeout = 3000):
                        self.device(resourceId=self.appconfig.id("Message","id_mms_send")).click()
                self.device.delay(1)
                self.back_to_message()
                self.device.delay(2)
                self.device(className='android.widget.ListView').child(index=0).click()
                self.device.delay(2)
                return self._verify_msg_sending()

    def get_sms_num(self):
        return self.device(resourceId=self.appconfig.id("Message","id_listitem")).count
            
    def lp_delete_msg(self,index = 0):
        ''' Long press to delete message in the message list
        
        argv: (int)index -- message order in the list
        '''
        self.logger.debug("Delete the first message.")
        childNodeNum=self.get_sms_num()
        
        if childNodeNum > 4:
            print self.device(resourceId=self.appconfig.id("Message","id_listitem"),index = index).long_click()
#             if self.device(resourceId=self.appconfig.id("Message","id_listitem"),index = index).child(resourceId = "com.android.mms:id/from").get_text() not in self.msgs.values():
#                 print 111111111111111111111111111
            if self.device(text=self.appconfig("Message",'delete_action')).wait.exists(timeout = 2000):
                self.device(text=self.appconfig("Message",'delete_action')).click()
            if self.device(text=self.appconfig("Message",'delete_confirm')).wait.exists(timeout = 2000):
                self.device(text=self.appconfig("Message",'delete_confirm')).click()
            if self.get_sms_num()<childNodeNum:    
                return True
            else:
                return False
        return True  

    def delete_extra_msg(self):
        ''' Long press to delete message in the message list
        
        argv: (int)index -- message order in the list
        '''
        self.logger.debug("Delete the extra message.")
        childNodeNum=self.get_sms_num()
        for j in range(5):
            if childNodeNum == 4:
                return True
            for i in range(childNodeNum):
                from_num = self.device(resourceId=self.appconfig.id("Message","id_listitem"),index = i).child(resourceId="com.android.mms:id/from").get_text()
                if from_num not in self.msgs.values():
                    self.device(resourceId=self.appconfig.id("Message","id_listitem"),index = i).click()
                    self.logger.debug("Delete the message from: %s" %from_num)
                    if (self.device(resourceId="com.android.mms:id/embedded_text_editor").wait.exists(timeout = 5000) and
                        (self.device(text=from_num).exists)): 
                        self.device(description="accessibility overflow label").click()
                        if self.device(text="Delete thread").wait.exists(timeout = self.timeout):
                            self.device(text="Delete thread").click()
                        if self.device(text=self.appconfig("Message",'delete_confirm')).wait.exists(timeout = self.timeout):
                            self.device(text=self.appconfig("Message",'delete_confirm')).click()
                            break
                    else:
                        self.logger.warning("Enter the wrong msg!")
                        break
                    self.back_to_message()
            childNodeNum=self.get_sms_num()
        else:
            self.logger.warning("Too many extra messages")
            return False

    def clean_message(self):
        self.logger.debug('clean message')
        sms_bum = self.get_sms_num()
        if sms_bum > 4:
            self.device(description=self.appconfig("Message","options")).click()
            if self.device(text=self.appconfig("Message","delete_all_action")).wait.exists(timeout = 2000):
                self.device(text=self.appconfig("Message","delete_all_action")).click()
                if self.device(resourceId=self.appconfig.id("Message","id_select_all")).wait.exists(timeout = 2000):          
                    self.device(resourceId=self.appconfig.id("Message","id_select_all")).click()
                    self.device.delay(2)   
            for index in range(sms_bum):
                if index!=0:
                    self.device(resourceId=self.appconfig.id("Message","id_listitem"),index = index).click()
            
                       
    def case_forward_msg(self,msg_type, times):
        if times == 0:
            return 
        self.logger.debug("Send %s %s times." % (msg_type, times))
        for loop in range(times):
            try:
                self.logger.debug("Select the message with %s." % (msg_type))
                if self.fwd_msg(msg_type,"10010"):
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop %s." % (loop+1))
                else:
                    self.logger.warning("Less 4 msg in the list")
                    self.save_fail_img()
                self.back_to_message()
                self.delete_extra_msg()
            except Exception,e:
                self.save_fail_img()
                self.enter_message()
                self.back_to_message()
                self.delete_extra_msg()
        self.logger.debug("Send %s Msg Test complete." % msg_type )
    
    def case_open_msg(self,msg_type, times):
        self.logger.debug("Open %s %s Times." %(msg_type, times))
        if self.enter_message():
            for loop in range(times):
                try:
                    if self.select_msg(msg_type):
                        self.suc_times += 1
                        self.back_to_message()
                        self.logger.info("Trace Success Loop %s." % (loop+1))
                    else:
                        self.logger.warning("Cannot open message with %s." % msg_type)
                        self.save_fail_img()
                    self.back_to_message()
                except Exception,e:
                    self.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
                    self.enter_message()
                    self.back_to_message()
        self.logger.debug("Open %s Msg Test complete." % msg_type)
   
if __name__ == '__main__':
    a = Message("56c051e1","Message")
    a.delete_extra_msg()

