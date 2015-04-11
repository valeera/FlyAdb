"""Browser library for scripts.
"""
import re
import sys
import os
from common import Common

class Browser(Common):
        
    def enter(self):
        """Launch browser.
        """
        self.logger.debug('enter browser')
        if self.device(resourceId= self.appconfig.id("Browser","id_url")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Browser")
        if self.device(resourceId= self.appconfig.id("Browser","id_url")).wait.exists(timeout=self.timeout):
            return True
        else:
            return False 
 
    def exit(self):
        """exit browser.
        """
        self.logger.debug('exit browser')
        if not self.device(packageName = self.appconfig("Browser","package")):
            return True
        self.device(description=self.appconfig("Browser","options")).click()
        self.device.delay(3)
        self.device(scrollable=True).scroll.vert.to(text=self.appconfig("Browser","exit"))
        self.device(text=self.appconfig("Browser","exit")).click()
        if self.device(text = self.appconfig("Browser","exit_confirm")).wait.exists(timeout=self.timeout):
            self.device(text = self.appconfig("Browser","exit_confirm")).click()
        if not self.device(packageName = self.appconfig("Browser","package")):
            return True
        return False

    def home(self):
        for loop in range(3):
            if self.device(resourceId= self.appconfig.id("Browser","id_url")).wait.exists(timeout=2000):
                return
            else:
                self.device.press.back()
                
    def enter_homepage(self):
        """enter home page
        """
        self.logger.debug('enter the home page')
        self.device(description=self.appconfig("Browser","options")).click()
        homepage = self.device(text=self.appconfig("Browser","action_home"))
        if homepage.wait.exists(timeout=self.timeout):  
            homepage.click()
        else:
            self.logger.debug("home page load fail!")
            return False      
        self.logger.debug('loading...')  
        progress = self.device(resourceId=self.appconfig.id("Browser","id_progress"))     
        if progress.wait.exists(timeout=self.timeout):
            if not progress.wait.gone(timeout=30000):
                self.logger.debug("home page load fail!")
                return False
        self.logger.debug("home page load success!")
        return True      
        
    def browser_webpage(self,website):
        """browser webpage
        """ 
        #widget position:the edit area of website 
        url_text = self.device(className='android.widget.EditText',resourceId=self.appconfig.id("Browser","id_url")) 
        if url_text.wait.exists(timeout=self.timeout):    
            url_text.set_text(website)
            self.device.delay(3)
            self.device.press.enter()
            self.device.delay(1)
            self.logger.debug('loading...')
            progress = self.device(resourceId=self.appconfig.id("Browser","id_progress"))     
            if progress.wait.exists(timeout=self.timeout):
                if not progress.wait.gone(timeout=30000):
                    self.logger.debug(website+" open fail!")
                    return False
            self.logger.debug(website+" load success!")
            return True 
        self.logger.debug(website+" open fail!")
        return False
 
    def clear_data(self):
        """clear data of browser
        """         
        self.logger.debug('Clear browser data')
        self.device(description=self.appconfig("Browser","options")).click()
        self.device.delay(2)
        self.device(scrollable=True).scroll.vert.forward(steps=10)
        setting = self.device(text= self.appconfig("Browser","settings"))
        if setting.wait.exists(timeout=self.timeout):
            setting.click()
        ps = self.device(text=self.appconfig("Browser","security"))
        if ps.wait.exists(timeout=self.timeout):
            ps.click()
        clear = self.device(text=self.appconfig("Browser","clear_cache"))
        if clear.wait.exists(timeout=self.timeout):
            clear.click()           
        ok = self.device(text=self.appconfig("Browser","clear_confirm"))
        if ok.wait.exists(timeout=self.timeout):
            ok.click()             
        self.home()
            

    def browser_playvideo(self,website):
        """play video by browser
        """         
        url_text = self.device(className='android.widget.EditText',resourceId=self.appconfig.id("Browser","id_url")) 
        if url_text.wait.exists(timeout=self.timeout):    
            url_text.set_text(website)
            self.device.delay(3)
            self.device.press.enter()
            self.device.delay(1)
            self.logger.debug('loading...')
            if self.device(description='watch?v=MVbeoSPqRs4#').wait.exists(timeout=10000):
                self.logger.debug('play video...')
                self.device(description='watch?v=MVbeoSPqRs4#').click()
                self.device.delay(30)
                self.device.press.back()
                self.device.delay(2)
                return True
        self.logger.debug("browser play video fail!")
        return False
    
    def select_menu(self,menu_text):
        """enter node of menu
        """
        self.logger.debug('enter menu: '+ menu_text)
        if self.device(text = self.appconfig("Browser","bookmarks_title")).exists:
            return True
        self.device(description=self.appconfig("Browser","options")).click()
        if self.device(text=menu_text).wait.exists(timeout = self.timeout):          
            self.device(text=menu_text).click()
        else:
            self.device(scrollable=True).scroll.vert.forward(steps=10)
            self.device(text=menu_text).click()
        self.device.delay(2)
        return True
        
    def select_bookmark(self,number):
        """load webpage from bookmark 
        """
        #each coordinate match up different bookmark 
        self.select_menu('Bookmarks')    
#         self._device(text='Mobile Bookmarks').wait.exists(timeout=10000)
        bookmark = self.device(className="android.widget.LinearLayout",index=number/3+1).child(className="android.widget.RelativeLayout",index=number%3)
        if bookmark.wait.exists(timeout=self.timeout):
            bookmark.click()
            self.logger.debug('loading...')
            progress = self.device(resourceId=self.appconfig.id("Browser","id_progress"))     
            if progress.wait.exists(timeout=self.timeout):
                if not progress.wait.gone(timeout=30000):
                    self.logger.debug("Bookmark %s load failed!"%number)
                    return False
            self.logger.debug("Bookmark %s load success!"%number)
            return True
        self.logger.debug("Bookmark %s load failed!"%number)
        return True 

    def visit_att(self,times=1):
        for index in range(times):
            try:
                if self.select_bookmark(0):
                    self.device.press.back()
                    self.clear_data()
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop "+ str(index+1))                        
                else:
                    self.save_fail_img()
            except Exception,e:
                self.save_fail_img()
    #                     self.log_traceback(traceback.format_exc())
                self.enter()
        return True
    def navigate(self,url,times=1):
        for index in  range(times):
            try:      
                if self.browser_webpage(url):
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop "+ str(index+1))                        
                else:
                    self.save_fail_img()
            except Exception,e:
                self.save_fail_img()
    #                     self.log_traceback(traceback.format_exc())
                self.enter()
        return True
    def visit_topsite(self,times): 
        for index in range(times):  
            try:
                success = 0
                for i in range(5):
                    if self.select_bookmark(i):
                        success+=1                 
                    else:
                        self.save_fail_img()
                        break
                else:
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop %s." % (index+1))          
            except Exception,e:
                self.save_fail_img()
    #                     self.log_traceback(traceback.format_exc())
                self.enter()  
        return True


if __name__ == '__main__':
    a = Browser("a7c0c6cf","Browser")
    a.visit_att(0)
    a.visit_topsite(0)
    print a.exit()    

#     a.enter_contacts()
