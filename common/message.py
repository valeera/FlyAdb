# -*- coding: utf-8 -*-
"""Message library for scripts.
"""

import re
import sys
import os
from common import Common,UIParser
from automator.uiautomator import Device
    
class Message(Common):

    """Provide common functions for scripts, such as launching activity."""
    def __init__(self, device, log_name):
        Common.__init__(self, device,log_name)
        self.appconfig.set_section("Message")
        self.msgs = {'Audio':"4",'Video':"3",'Photo':"2",'Text':"1"} 
           
    def enter(self):
        """Launch browser.
        """
        self.logger.debug('enter Message')
        if self.device(resourceId= self.appconfig.id("id_enter")).wait.exists(timeout=2000):
            return True
        self.start_app("Messaging")
        if self.device(resourceId = self.appconfig.id("id_enter")).wait.exists(timeout=2000):
            return True
        else:
            self.logger.warning('Launch Message fail')
            return False
        return True
    
    def setup(self,data = None):
        if not self.enter():
            return False
        text = [
                {"id":{"resourceId":self.appconfig.id("id_new")}},
                {"id":{"className":"android.widget.MultiAutoCompleteTextView"},"action":{"type":"set_text","param":[self.msgs["Text"]]}}, 
                #{"id":{"text":"Type text message"},"action":{"type":"set_text","param":["10010"]}}, #sprints
                {"id":{"resourceId":"com.android.mms:id/embedded_text_editor"},"action":{"type":"set_text","param":["10010"]}}, #alto5gl                          
                {"id":{"resourceId":self.appconfig.id("id_sms_send")}},
                {"id":{"meta":"back_to_message"}},
                ]
        picture = [
                {"id":"resourceId","content":self.appconfig.id("id_new")},
                {"id":"className","content":"android.widget.MultiAutoCompleteTextView","action":{"type":"set_text","param":[self.msgs["Photo"]]}}, 
                {"id":"resourceId","content":self.appconfig.id("id_share")},
                {"id":"text","content":[self.appconfig("picture"),self.appconfig("capture_picture")]},
                {"id":"text","content":"No thanks","assert":False},                 
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/shutter_button","action":{"type":"click"}},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/btn_done"},
                {"id":{"resourceId":self.appconfig.id("id_mms_send")}},
                {"id":"meta","content":"back_to_message"},
                ]   
    
        video = [
                {"id":"resourceId","content":self.appconfig.id("id_new")},
                {"id":"className","content":"android.widget.MultiAutoCompleteTextView","action":{"type":"set_text","param":[self.msgs["Video"]]}}, 
                {"id":"resourceId","content":"com.android.mms:id/share_button"},
                {"id":"text","content":["Videos","Capture video"]},                     
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/shutter_button","action":{"type":"click","delay":1000}},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/shutter_button"},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/btn_done"},
                {"id":"resourceId","content":"com.android.mms:id/send_button_mms"},
                {"id":"meta","content":"back_to_message"},
                ]
     
        audio = [
                {"id":"resourceId","content":self.appconfig.id("id_new")},
                {"id":"className","content":"android.widget.MultiAutoCompleteTextView","action":{"type":"set_text","param":self.msgs["Audio"]}}, 
                {"id":"resourceId","content":"com.android.mms:id/share_button"},
                {"id":"text","content":["Audio","Record audio"]},                     
                {"id":"resourceId","content":"com.tct.soundrecorder:id/recordButton","action":{"type":"click","delay":1000}},
                {"id":"text","content":"Save","wait":20000},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/btn_done"},
                {"id":"resourceId","content":"com.android.mms:id/send_button_mms"},
                {"id":"meta","content":"back_to_message"},
                ]
            
        #return UIParser.run(self,[text,picture,video,audio],self.back_to_message)
        return UIParser.run(self,[text,picture,video,audio],self.back_to_message)
    
    def back_to_message(self):
        """back to message list .
        """  
        self.logger.debug('Back to message list')
        for i in range(5):
            if self.device(resourceId=self.appconfig.id("id_enter")).exists:
                break
            self.device.press.back()
            self.device.delay(1)
            if self.device(text="OK").exists:
                self.device(text="OK").click()
        else:
            self.logger.warning('Back to message list fail')

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
        select = [
                  {"id":{"resourceId":'com.android.mms:id/from',"text":self.msgs[strtype]}}
                  ]
        return UIParser.run(self,select,self.back_to_message) 
        #------------------legency---------------------------  
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
        send = "Send" if type=="Text" else "Send MMS"
        fwd = [
               {"id":{"resourceId":'com.android.mms:id/text_view'},"action":{"type":"long_click"}},         
               {"id":{"text":'Forward'}},
               {"id":{"className":"android.widget.MultiAutoCompleteTextView"},"action":{"type":"set_text","param":[number]}}, 
               {"id":{"description":send}}, 
               {"id":"meta","content":"_verify_msg_sending","assert":False},
               {"id":"meta","content":"back_to_message"}  
               ]      
        return UIParser.run(self,fwd,self.back_to_message)
     
        #------------------legency---------------------------  
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
                    if self.device(resourceId=self.appconfig.id("id_sms_send")).wait.exists(timeout = 3000):
                        self.device(resourceId=self.appconfig.id("id_sms_send")).click()
                else:
                    if self.device(resourceId=self.appconfig.id("id_mms_send")).wait.exists(timeout = 3000):
                        self.device(resourceId=self.appconfig.id("id_mms_send")).click()
                self.device.delay(1)
                self.back_to_message()
                self.device.delay(2)
                self.device(className='android.widget.ListView').child(index=0).click()
                self.device.delay(2)
                return self._verify_msg_sending()

    def get_sms_num(self):
        return self.device(resourceId=self.appconfig.id("id_listitem")).count
            
    def delete_extra_msg(self):
        ''' Long press to delete message in the message list
        
        argv: (int)index -- message order in the list
        '''
        self.logger.debug("Delete the extra message.")
        childNodeNum=self.get_sms_num()
        if childNodeNum == 4:
            return True
        elif childNodeNum>4:
            for i in range(childNodeNum):
                from_num = self.device(resourceId="android:id/list").child(index = i).child(resourceId="com.android.mms:id/from").get_text()
                if from_num not in self.msgs.values():
                    self.device(resourceId="android:id/list").child(index = i).child(resourceId="com.android.mms:id/from").click()
                    self.logger.debug("Delete the message from: %s" %from_num)              
                    if self.device(description = "More options").wait.exists(timeout = self.timeout):# and self.device(text=from_num).exists:
                        self.device(description = "More options").click()
                    elif (self.device(resourceId="com.android.mms:id/embedded_text_editor").wait.exists(timeout = 5000) and
                        (self.device(text=from_num).exists)): 
                        self.device(description="accessibility overflow label").click()
                    else:
                        self.logger.warning("Enter the wrong msg!")
                        break
                    if self.device(text="Delete thread").wait.exists(timeout = self.timeout):
                        self.device(text="Delete thread").click()
                        if self.device(text=self.appconfig('delete_confirm')).wait.exists(timeout = self.timeout):
                            self.device(text=self.appconfig('delete_confirm')).click()
                            return self.delete_extra_msg()
                    elif self.device(text="Discard").wait.exists():
                        self.device(text="Discard").click()
                        return self.delete_extra_msg()
                    self.back_to_message()
        else:
            self.logger.warning("Too many extra messages")
            return False
                    
    def case_forward_msg(self,msg_type, times):
        if times == 0:
            return 
        self.logger.debug("Send %s %s times." % (msg_type, times))
        for loop in range(times):
            try:
                self.logger.debug("Select the message with %s." % (msg_type))
                if self.fwd_msg(msg_type,"10000"):
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
        if self.enter():
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
        
#----------------------------------------------- not used-------------------------------------------------------------------
    def send_pic(self,number):
        """send a message(SMS)
        argv: (str)number -- the telephone number you want to send
              (str)content -- SMS content
        """
        picture = [
                {"id":"resourceId","content":"com.android.mms:id/action_compose_new"},
                {"id":"className","content":"android.widget.MultiAutoCompleteTextView","action":{"type":"set_text","param":[number]}}, 
                {"id":"resourceId","content":"com.android.mms:id/share_button"},
                {"id":"text","content":["Pictures","Capture picture"]},                     
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/shutter_button","action":{"type":"click"}},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/btn_done"},
                {"id":"resourceId","content":"com.android.mms:id/send_button_mms"},
                {"id":"meta","content":"back_to_message"},
                ]  
        return UIParser.run(self,picture,self.back_to_message)       

    def sms_Send(self,number,content = ""):
        """send a message(SMS)
        argv: (str)number -- the telephone number you want to send
              (str)content -- SMS content
        """
        if self.enter():
            self.device(resourceId=self.appconfig.id("id_new")).click()
            input_text = self.device(className='android.widget.MultiAutoCompleteTextView')
            if input_text.wait.exists(timeout = self.timeout):
                self.logger.debug('input phone number:'+str(number))
                input_text.set_text(str(number))
                self.device.delay(2)
                if content != "":
                    self.logger.debug('input sms content:'+content)
                    self.device(className='android.widget.EditText').click()
                    self.device.delay(2)
                    self.device(className='android.widget.EditText').set_text(content)
                    self.device.delay(2)
                self.logger.debug('send')
                #self.device(resourceId=self.appconfig.id("Message","id_send_sms")).click()
                self.device(description=self.appconfig("send")).click()
                self.device.delay(1)
            if self.device(text='SENDING?').wait.gone(timeout = 10000):
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
    
    def mms_Send(self,number,type,content = "10010"):
        """send a message(MMS)
        argv: (str)number -- the telephone number you want to send
              (str)content -- MMS content
              (str)subject -- MMS subject
              pic\video\audio -- attachment of the message
        """
        if not self.enter():
            return False
        text = [
                {"id":"resourceId","content":"com.android.mms:id/action_compose_new"},
                {"id":"className","content":"android.widget.MultiAutoCompleteTextView","action":{"type":"set_text","param":[number]}}, 
                {"id":"text","content":"Type text message","action":{"type":"set_text","param":[content]}}, 
                {"id":"resourceId","content":"com.android.mms:id/send_button_sms"},
                {"id":"meta","content":"back_to_message"},
                ]
    
        picture = [
                {"id":"resourceId","content":"com.android.mms:id/action_compose_new"},
                {"id":"className","content":"android.widget.MultiAutoCompleteTextView","action":{"type":"set_text","param":[number]}}, 
                {"id":"resourceId","content":"com.android.mms:id/share_button"},
                {"id":"text","content":["Pictures","Capture picture"]},                     
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/shutter_button","action":{"type":"click"}},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/btn_done"},
                {"id":"resourceId","content":"com.android.mms:id/send_button_mms"},
                {"id":"meta","content":"back_to_message"},
                ]   
    
        video = [
                {"id":"resourceId","content":"com.android.mms:id/action_compose_new"},
                {"id":"className","content":"android.widget.MultiAutoCompleteTextView","action":{"type":"set_text","param":[number]}}, 
                {"id":"resourceId","content":"com.android.mms:id/share_button"},
                {"id":"text","content":["Videos","Capture video"]},                     
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/shutter_button","action":{"type":"click","delay":1000}},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/shutter_button"},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/btn_done"},
                {"id":"resourceId","content":"com.android.mms:id/send_button_mms"},
                {"id":"meta","content":"back_to_message"},
                ]
     
        audio = [
                {"id":"resourceId","content":"com.android.mms:id/action_compose_new"},
                {"id":"className","content":"android.widget.MultiAutoCompleteTextView","action":{"type":"set_text","param":[number]}}, 
                {"id":"resourceId","content":"com.android.mms:id/share_button"},
                {"id":"text","content":["Audio","Record audio"]},                     
                {"id":"resourceId","content":"com.tct.soundrecorder:id/recordButton","action":{"type":"click","delay":1000}},
                {"id":"text","content":"Save"},
                {"id":"resourceId","content":"org.codeaurora.snapcam:id/btn_done"},
                {"id":"resourceId","content":"com.android.mms:id/send_button_mms"},
                {"id":"meta","content":"back_to_message"},
                ]
        return UIParser.run(self,locals()[str(type)],self.back_to_message)
        
    def del_all_message(self):

        """delete all message in current list
        """
        self.logger.debug('delete all message')    
        delete_all = [
                      {"id":"description","content":"More options"},
                      {"id":"text","content":["Delete all threads","Delete"]},                      
                      {"id":"resourceId","content":"com.android.mms:id/empty","action":None},                                          
                      ]
        return UIParser.run(self,delete_all,self.back_to_message)
        '''
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
       '''

    def clean_message(self):
        self.logger.debug('clean message')
        sms_bum = self.get_sms_num()
        if sms_bum > 4:
            self.device(description=self.appconfig("options")).click()
            if self.device(text=self.appconfig("delete_all_action")).wait.exists(timeout = 2000):
                self.device(text=self.appconfig("delete_all_action")).click()
                if self.device(resourceId=self.appconfig.id("id_select_all")).wait.exists(timeout = 2000):          
                    self.device(resourceId=self.appconfig.id("id_select_all")).click()
                    self.device.delay(2)   
            for index in range(sms_bum):
                if index!=0:
                    self.device(resourceId=self.appconfig.id("id_listitem"),index = index).click()

    def lp_delete_msg(self,index = 0):
        ''' Long press to delete message in the message list
        
        argv: (int)index -- message order in the list
        '''
        self.logger.debug("Delete the first message.")
        childNodeNum=self.get_sms_num()
        
        if childNodeNum > 4:
            print self.device(resourceId=self.appconfig.id("id_listitem"),index = index).long_click()
            if self.device(text=self.appconfig('delete_action')).wait.exists(timeout = 2000):
                self.device(text=self.appconfig('delete_action')).click()
            if self.device(text=self.appconfig('delete_confirm')).wait.exists(timeout = 2000):
                self.device(text=self.appconfig('delete_confirm')).click()
            if self.get_sms_num()<childNodeNum:    
                return True
            else:
                return False
        return True  

if __name__ == '__main__':
    
    a = Message("a7ffc62c","Message")
    print a.setup()

    #a.device.watcher("messaging").when(text = "This can cause charges to your mobile account.").click(text = "Send")
    #a.device.watcher("messaging").triggered
