# -*- coding: UTF-8 -*-
"""Email library for scripts.

"""
import re
import sys
from common import Common


class Email(Common):

    """Provide common functions involved email."""  

#     def setup(self,accountName,password):
#         """login email account
#         TOD OD!!!!!
#         """ 
#         self.logger.debug('set email account')
#         self.device.delay(2)
#         if not self.device(text='Account setup').exists:
#             self.logger.debug('Launch Message fail')
#         else:
#             if self.device(text='Email address').exists:
#                 self.logger.debug('input account name: %s',accountName)
#                 self.device(text='Email address').set_text(accountName)
#                 self.device.delay(3)
#                 if self.device(className='android.widget.EditText',index=4).exists:
#                     self.logger.debug('input pass word: %s',password)
#                     self.device(className='android.widget.EditText',index=4).set_text(password)
#                     self.device.delay(3)
#                     self.device(text='Next').click()
#                     if self.device(text='Next').wait.exists(timeout=60000):
#                         self.device(text='Next').click()
#                     if self.device(description='Your name (displayed on outgoing messages)').wait.exists(timeout=60000):
#                         self.logger.debug('input name: Tester')
#                         self.device(description='Your name (displayed on outgoing messages)').set_text('Tester')
#                         self.device.delay(5)
#                     if self.device(text='Next').wait.exists(timeout=60000):
#                         self.device(text='Next').click()
#                         self.device.delay(2)
#                     if self.device(text=accountName).exists:
#                         self.logger.debug('email login success!!!')
#                         return True
#                     else:
#                         self.device.press.home()
#                         self.device.delay(2)
#                         self.enter()
#                         self.device.delay(2)
#                         if self.device(text=accountName).wait.exists(timeout=60000):
#                             self.logger.debug('email login success!!!')
#                             return True
#         self.logger.debug('email login fail')           
#         return False
    
    def enter(self):
        """Launch email by StartActivity.
        """
        self.logger.debug("Launch email.")
        if self.device(description=self.appconfig("Email","navigation")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Email")
        if self.device(description=self.appconfig("Email","navigation")).wait.exists(timeout=self.timeout):
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
            if self.device(resourceId="com.tct.email:id/account_display_name").wait.exists(timeout = self.timeout):
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
    
    def back_to_mainapp(self):
        self.logger.debug("Back to main activity")
        for i in range(5):
            if self.device(resourceId = "com.tct.email:id/search").exists:
                return True
            self.device.press.back()
            self.device.delay(1)
        else:
            self.logger.warning("Cannot back to main activity")
            return False

    def loading(self):
        self.device.swipe(250,300,250,1200)
        ui_loading = self.device(resourceId = self.appconfig.id("Email","id_loading"))
        if ui_loading.exists:
            self.logger.debug('loading mail')
            if not ui_loading.wait.gone(timeout = 30000):
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
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).click()
        else:
            self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=1).click()
        if self.device(resourceId=self.appconfig.id("Email","id_overflow")).wait.exists(timeout = 5000):
            self.device(resourceId=self.appconfig.id("Email","id_overflow")).click()
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
        if self.device(resourceId = self.appconfig.id("Email","id_empty")).wait.exists(timeout=300000):                        
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
            if self.device(text='No connection.').exists:
                return False  
        else:          
            maxtime=0
#             while not self.device(textContains = self.appconfig("Email","empty_text")).exists:
            while not self.device(resourceId = self.appconfig.id("Email","id_empty")).exists:
                if self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).exists:
                    self.device(className='android.widget.ListView').child(className='android.widget.FrameLayout',index=0).long_click()
                if self.device(description='Delete').wait.exists(timeout = self.timeout):
                    self.device(description='Delete').click()
                    self.device.delay(2)
                if self.device(text= self.appconfig.id("Email","no_connection")).exists:
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
    a = Email("add6e685","Email")
    a.open_email(2)

    
    
    
    