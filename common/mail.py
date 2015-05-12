# -*- coding: utf-8 -*-
"""Email library """
import re
import sys
from common import Common,UIParser


class Email(Common):

    """Provide common functions involved email."""  

    def setup(self,accountName,password,type = "pop3"):      
        self.enter()
        if type == "pop3":
            step1 = [
                    {"id":{"text":self.appconfig("mail_type","Email")}},
                    {"id":{"resourceId":self.appconfig.id("id_next","Email")}},
                    {"id":{"resourceId":"com.android.email:id/account_email"},"action":{"type":"set_text","param":[accountName]}},
                    {"id":{"resourceId":"com.android.email:id/next"}},
                    {"id":{"text":"POP3"}},
                    {"id":{"resourceId":"com.android.email:id/regular_password"},"action":{"type":"set_text","param":[password]}},
                    {"id":{"resourceId":"com.android.email:id/next"},"delay":5000}, 
                    {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"clear_text"},"delay":5000},  
                    {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"set_text","param":[self.appconfig("mail_server")]}},                     
                    ]

            if UIParser.run(self,step1, self.back_to_mainapp)==False:
                return False
            self.device(scrollable=True).scroll.vert.to(description="Next")
            step2 = [
                    {"id":{"description":"Next"},"delay":10000},     
                    {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"clear_text"},"delay":5000},             
                    {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"set_text","param":[self.appconfig("mail_server")]}},                          
                    ]
            if UIParser.run(self,step2, self.back_to_mainapp)==False:
                return False
            self.device(scrollable=True).scroll.vert.to(description="Next")
            step3 = [
                    {"id":"description","resourceId":["Next","Next"],"delay":10000},
                    {"id":{"resourceId":"com.android.email:id/account_name"},"action":{"type":"set_text","param":"CreatedByUIA"}},
                    {"id":"description","resourceId":["Next","Next"]}               
                    ]
            if UIParser.run(self,step3, self.back_to_mainapp)==False:
                return False
        elif type == "exchange":
            step1 = [
                    {"id":{"resourceId":"com.android.email:id/account_email"},"action":{"type":"set_text","param":[accountName]}},             
                    {"id":"text","content":["Manual setup","Exchange"]},
                    {"id":{"resourceId":"com.android.email:id/regular_password"},"action":{"type":"set_text","param":[password]}},
                    {"id":{"resourceId":"com.android.email:id/next"},"delay":5000},              
                    {"id":{"resourceId":"com.android.email:id/account_username"},"action":{"type":"clear_text"},"delay":5000},  
                    {"id":{"resourceId":"com.android.email:id/account_username"},"action":{"type":"set_text","param":[accountName]}}, 
                    {"id":"meta","content":"back"},
                    {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"clear_text"},"delay":5000},  
                    {"id":{"resourceId":"com.android.email:id/account_server"},"action":{"type":"set_text","param":["mail.tcl.com"]}},                    
                    {"id":"meta","content":"back"},
                    {"id":{"description":"Security type"}},   
                    {"id":{"text":"SSL/TLS (Accept all certificates)"}}, 
                    ]
            if UIParser.run(self,step1, self.back_to_mainapp)==False:
                return False
            self.device(scrollable=True).scroll.vert.to(description="Next")
            step3 = [
                    {"id":{"description":"Next"}},     
                    {"id":{"text":"OK"},"wait":60000},
                    {"id":{"resourceId":"com.android.email:id/account_check_frequency"}},   
                    {"id":{"text":"Manual"}},
                    {"id":{"resourceId":"com.android.email:id/account_sync_window"}},   
                    {"id":{"text":"All"}},                    
                                                      
                    ]
            if UIParser.run(self,step3, self.back_to_mainapp)==False:
                return False            
            self.device(scrollable=True).scroll.vert.to(description="Next")
            step4 = [
                    {"id":{"description":"Next"}},   
                    {"id":{"text":"Activate"},"wait":10000},                   
                    {"id":{"description":"Next"},"wait":30000},                                         
                                                       
                    ]
            if UIParser.run(self,step4, self.back_to_mainapp)==False:
                return False           
            self.device.delay(60)
            self.select_mail(0)
            self.device.delay(5)
            self.select_mail(1)           
            step5 = [
                    {"id":{"resourceId":"com.android.email:id/attachment_icon"},"wait":30000},                                       
                                                       
                    ]
            if UIParser.run(self,step5, self.back_to_mainapp)==False:
                return False               
            self.back_to_mainapp()
        return True
    
    def enter(self):
        """Launch email by StartActivity.
        """
        self.logger.debug("Launch email.")
        if self.device(description=self.appconfig("navigation")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Email")
        if self.device(description=self.appconfig("navigation")).wait.exists(timeout=self.timeout):
            return True
        else:
            self.logger.debug('Launch eamil fail')
            return False

    def enter_box(self,box):
        """enter the box you want  
        argv: (str)box --text of the box
        """
        self.logger.debug('enter the box: %s',box)
        if not self.device(text=box, index=2).exists:
            if self.device(description='Open navigation drawer').wait.exists(timeout=5000):
                self.device(description='Open navigation drawer').click()
            if self.device(resourceId="com.android.email:id/account_display_name").wait.exists(timeout = self.timeout):
                self.device(text=box).click()
            else:
                self.logger.warning("==========================")
                self.save_fail_img()
                self.logger.warning("==========================")
                self.logger.warning("Cannot select box: %s" %box)
                return False
        if not self.device(text=box, index=2).wait.exists(timeout=5000):
            self.logger.warning("Cannot change to box: %s" %box)
            return False
        return True

    def back(self):
        self.device.press.back()
        return True
    
    def back_to_mainapp(self):
        self.logger.debug("Back to main activity")
        for i in range(5):
            if self.device(resourceId = self.appconfig.id("id_search")).wait.exists(timeout = 2000):
                return True
            self.device.press.back()
        else:
            self.logger.warning("Cannot back to main activity")
            return False

    def loading(self):
        self.device.swipe(250,300,250,1200)
        ui_loading = self.device(resourceId = self.appconfig.id("id_loading","Email"))
        if ui_loading.exists:
            self.logger.debug('loading mail')
            if not self.device(resourceId = self.appconfig.id("id_loading","Email")).wait.gone(timeout = 60000):
                self.logger.debug('loading mail Failed')
                return False 
        return True
        
    def forward_email(self,address,att_flag):
        """send a email
        argv: (str)address --email address you want to send
              (str)content --email content
        """
        if self.loading() == False:
            self.logger.debug('loading mail Failed')
            return False 
        if self.device(description='Dismiss tip').exists:
            self.device(description='Dismiss tip').click()
            self.device.delay(1)
        self.logger.debug('create an email')
        if att_flag:
            self.logger.debug('111111')
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).click()
        else:
            self.logger.debug('000000')
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=1).click()
        if self.device(resourceId=self.appconfig.id("id_overflow")).wait.exists(timeout = 5000):
            self.device(resourceId=self.appconfig.id("id_overflow")).click()
        else:
            self.logger.warning('Cannot open an email')
            return False
        if self.device(text='Forward').wait.exists(timeout = 2000):
            self.device(text='Forward').click()
        self.device.delay(2)
        self.device(description='To').set_text(address)
        self.device.delay(2)
        self.device(description='Send').click()
        self.device.delay(2)
        self.logger.debug('email sending...')
        self.device.press.back()
        self.device.delay(2)    
        self.enter_box("Outbox")   
        if self.loading() == False:
            self.logger.debug('loading mail Failed')
            return False 
        if self.device(resourceId = self.appconfig.id("id_empty")).wait.exists(timeout=300000):                        
            return True
        else:
            self.logger.debug('email send fail in 5 min!!!')
            return False
        self.logger.debug('email send fail!!!')
        return False
    
    def del_mail(self,box):
        """delete all email of the box  
        argv: (str)box --text bof the box
        """
        self.logger.debug('delete the mail of %s',box)
        if not self.device(text=box).exists:
            self.device(description='Open navigation drawer').click()
            if not self.device(text=box).wait.exists(timeout = self.timeout):
                self.device.swipe(250,300,250,1200)
                self.device.delay(2)
            self.device(text=box).click()
            self.device.delay(1)
        if self.loading() == False:
            self.logger.debug('loading mail Failed')
            return False
        if self.device(text = "Empty Trash").exists:
            self.device(text = "Empty Trash").click()
            if self.device(text = "Delete").wait.exists(timeout = self.timeout):
                self.device(text = "Delete").click()
                self.device.delay(2)
            if self.device(text='No connection.').exists:
                return False  
            if self.device(text='No connection.').wait.exists(timeout = 30000):
                return False
        else:          
            maxtime=0
#             while not self.device(textContains = self.appconfig("Email","empty_text")).exists:
            while not self.device(resourceId = self.appconfig.id("id_empty")).exists:
                if self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).exists:
                    self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).long_click()
                if self.device(description='Delete').wait.exists(timeout = self.timeout):
                    self.device(description='Delete').click()
                    self.device.delay(2)
                if self.device(text= self.appconfig.id("no_connection")).exists:
                    return False
                if maxtime>100:
                    return False
                maxtime+=1

        self.logger.debug('mail of the %s has delete complete',box)
        return True

    def select_mail(self,Index):
        self.logger.debug('select the mail of %s',str(Index))
        self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=Index).click()
        self.device.delay(2)
        if self.device(description='Reply').wait.exists(timeout=10000):
            return True
        else:
            self.logger.debug('select mail fail!')
            return False

    def send_email(self,address,att_flag,times = 1):
        self.logger.debug("Send with %d attachemnt %d Times" % (att_flag,times))   
        for loop in range (times):
            self.enter_box("Inbox")
            try:
                if self.forward_email(address,att_flag):
                    self.logger.debug("select mail success")
                    self.suc_times = self.suc_times + 1
                    self.logger.info("Trace Success Loop "+ str(loop + 1))
                    self.device.press.back() 
                    if self.del_mail('Sent') and self.del_mail('Trash'):
                        self.logger.debug('email send success!!!')
                    else:
                        self.logger.warning("Delete Trash Email Failed")
                        self.save_fail_img()
                else:
                    self.save_fail_img()
                    self.del_mail("Outbox")  
            except Exception,e:
                self.save_fail_img()
                #                 common.common.log_traceback(traceback.format_exc())
                self.back_to_mainapp()
                self.enter_box("Inbox")
                
    def open_email(self,times):
        self.logger.info('Open Email '+str(times)+' Times')
        for loop in range (times):
            self.enter_box("Inbox")
            try:
                if self.select_mail(0):
                    self.logger.debug("select mail success")
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop "+ str(loop + 1))
                    self.device.press.back()
                    self.device.delay(2)
                else:
                    self.save_fail_img()
                    self.enter_box("Inbox")
            except Exception,e:
                self.save_fail_img()
#                 common.common.log_traceback(traceback.format_exc())
                self.back_to_mainapp()
                self.enter_box("Inbox")


#test--------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    a = Email("a7c0c6cf","Email")
    a.setup("atttest08@tcl.com", "Password001","exchange")
    #a.open_email(2)
