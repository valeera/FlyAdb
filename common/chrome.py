"""chrome library for scripts.
"""

import re
import sys
from common import Common,UIParser

class Chrome(Common):
    '''
    classdocs
    '''
    def enter(self):
        """Launch Chrome.
        """
        self.logger.debug('enter Chrome')
        if self.device(resourceId=self.appconfig.id("id_location_bar","Chrome")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Chrome")
        if self.device(resourceId="com.android.chrome:id/terms_accept").wait.exists(timeout=5000):
            self.device(resourceId="com.android.chrome:id/terms_accept").click()
            if self.device(resourceId="com.android.chrome:id/positive_button").wait.exists(timeout=5000):
                self.device(resourceId="com.android.chrome:id/positive_button").click()
            if self.device(text="No, thanks").wait.exists(timeout=5000):
                self.device(text="No, thanks").click()
        if self.device(resourceId=self.appconfig.id("id_location_bar","Chrome")).wait.exists(timeout=self.timeout):
            return True
        else:
            return False
 
    def setup(self):
        self.enter()
        for web in self.config.get("Browser","setup").split(","):      
            bookmark = [
                        {"id":"description","content":["text Accept & continue","Next","No thanks"],"assert":False},
                        {"id":"meta","content":"chrome_webpage","action":{"param":[web]}},               
                        {"id":"description","content":["More options","Bookmark this page"]},
                        {"id":{"text":"Save"}},
                        {"id":"meta","content":"back_to_chrome"}
                        ]
            #self.chrome_webpage("www.baidu.com")
            UIParser.run(self,bookmark,self.back_to_chrome)
        pass
 
    def home(self):
        self.logger.debug('Back Chrome')
        for i in range(3):
            if self.device(resourceId=self.appconfig.id("id_location_bar","Chrome")).wait.exists(timeout=self.timeout):
                return True
            self.device.press.back()
            self.logger.debug('Back Chrome %s times' %i)
            self.device.delay(1)
        else:
            self.logger.warning("Cannot back to Chrome")

    def exit(self):
        self.logger.debug('Exit')
        for i in range(4):
            self.device.press.back()
            self.device.delay(1)
        if self.device(resourceId=self.appconfig.id("id_location_bar","Chrome")).exists:
            return False
        return True

    def back_to_chrome(self):
        self.logger.debug('Back Chrome')
        for i in range(3):
            if self.device(resourceId=self.appconfig.id("id_location_bar","Chrome")).wait.exists(timeout=self.timeout):
                return True
            self.device.press.back()
            self.logger.debug('Back Chrome %s times' %i)
            self.device.delay(1)
        else:
            self.logger.warning("Cannot back to Chrome")
        
    def clear_data(self):
        """clear data of browser

        author:li.huang
        """         
        self.logger.debug('Clear browser data')
        self.device(description=self.appconfig("options","Chrome")).click()
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(text=self.appconfig("history","Chrome"))
        if self.device(text=self.appconfig("history","Chrome")).wait.exists(timeout = 30000):
            self.device(text=self.appconfig("history","Chrome")).click()
        if self.device(description=self.appconfig("cbd","Chrome")).wait.exists(timeout=self.timeout):
            self.device(description=self.appconfig("cbd","Chrome")).click()
        clear = self.device(text=self.appconfig("txt_clear","Chrome"))
        if clear.wait.exists(timeout=self.timeout):
            clear.click()
        self.back_to_chrome()
        
    def chrome_webpage(self,website):
        """browser webpage
        """ 
        #widget position:the edit area of website 
        url_text = self.device(className='android.widget.EditText',resourceId=self.appconfig.id("id_url_bar","Chrome")) 
        if url_text.wait.exists(timeout=self.timeout):    
            url_text.set_text(website)
            self.device.delay(3)
            self.device.press.enter()
            self.device.delay(1)
            self.logger.debug('loading...')
            return self.is_loaded()
        self.logger.debug(website+" open fail!")
        return False
        
    def is_loaded(self):
        progress = self.device(resourceId=self.appconfig.id("id_progress","Chrome"))
        if progress.wait.exists(timeout=self.timeout):
            if not progress.wait.gone(timeout=30000):
                self.logger.debug("website open fail!")
                return False
        self.logger.debug("website load success!")
        return True 
        
    def navigate(self,url,times=1):
        ''' Navigate to URL specific
        
        @param url: Web address
        @type url: string
        @author: Zhihao.Gu
        '''
        for index in range(times):
            try:      
                if self.chrome_webpage(url):
                    self.clear_data()
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop "+ str(index+1))                        
                else:
                    self.save_fail_img()
            except Exception,e:
                self.save_fail_img()
                self.enter()
        return True
    
    def streaming(self,times,duration):
        self.logger.debug("Play Streaming " + str(times) +" Times")
        for loop in range(times):
            try:
                if self.chrome_webpage(self.appconfig("streamaddress","Chrome")):
                    if self.device(text=self.appconfig("Authentication","Chrome")).wait.exists(timeout=self.timeout):
                        self.logger.debug('input user name:'+self.appconfig("account_pwd","Chrome"))
                        self.device(description=self.appconfig("username","Chrome"),
                                    className='android.widget.EditText').set_text(self.appconfig("account_pwd","Chrome"))
                        self.device.delay(1)
                        self.logger.debug('input password:'+self.appconfig("account_pwd","Chrome"))
                        self.device(description=self.appconfig("password","Chrome"),
                                    className='android.widget.EditText').set_text(self.appconfig("account_pwd","Chrome"))
                        self.device.delay(1)
                        self.device(text=self.appconfig("login","Chrome")).click()
                        self.device.delay(1)
                    if self.device(description=self.appconfig("streamname","Chrome")).wait.exists(timeout=self.timeout):
                        self.logger.debug('Choese dirty_dance_1_mp4_amr_14m_80kbps.3gp')
                        x,y = self.device(description=self.appconfig("streamname","Chrome")).get_location()
                        self.adb.shell("input tap %s %s" %(x,y))
                        if self.device(text=self.appconfig("vp","Chrome")).wait.exists(timeout=self.timeout):
                            self.device(text=self.appconfig("vp","Chrome")).click()
                        if self.device(text=self.appconfig("always","Chrome")).wait.exists(timeout=self.timeout):
                            self.device(text=self.appconfig("always","Chrome")).click()
                        if self.device(text=self.appconfig("startover","Chrome")).wait.exists(timeout=self.timeout):
                            self.device(text=self.appconfig("startover","Chrome")).click()
                        if self.device(description=self.appconfig("vptb","Chrome")).wait.exists(timeout=self.timeout):
                            self.logger.debug("loading movies... ...")
                        if self.device(resourceId=self.appconfig("view_root","Chrome")).wait.exists(timeout=self.timeout):
                            self.logger.debug('Long movies load success!')
                            maxtimes=1
                            while self.device(resourceId=self.appconfig("view_root","Chrome")).exists:
                                self.device.delay(10)
                                self.logger.debug('Playing %s secs' %(maxtimes*10))
                                if maxtimes > (duration/10):
                                    return True
                                maxtimes+=1
                            if self.device(description=self.appconfig("streamname","Chrome")).exists:
                                self.save_fail_img()
                                return False
                self.logger.debug('Long movies load fail')
                self.save_fail_img()
                return False
            except Exception,e:
                self.save_fail_img()
            finally:
                self.back_to_chrome()
        self.logger.debug('Streamings Test complete')
    
    def download_file(self, times, URL):
        """Download file
        
        @author: zhihao.gu
        """
        self.logger.debug("Download file " + str(times) +" Times")
        for loop in range(times):
            try:
                if self.chrome_webpage(self.appconfig("downloadaddress","Chrome")):
                    if self.device(text=self.appconfig("Authentication","Chrome")).wait.exists(timeout=self.timeout):
                        self.logger.debug('input user name:'+self.appconfig("account_pwd","Chrome"))
                        self.device(description=self.appconfig("username","Chrome"),
                                    className='android.widget.EditText').set_text(self.appconfig("account_pwd","Chrome"))
                        self.device.delay(1)
                        self.logger.debug('input password:'+self.appconfig("account_pwd","Chrome"))
                        self.device(description=self.appconfig("password","Chrome"),
                                    className='android.widget.EditText').set_text(self.appconfig("account_pwd","Chrome"))
                        self.device.delay(1)
                        self.device(text=self.appconfig("login","Chrome")).click()
                        self.device.delay(1)
                    if self.device(description=self.appconfig("downloadname","Chrome")).wait.exists(timeout=self.timeout):
                        self.logger.debug('Choese dirty_dance_1_mp4_amr_14m_80kbps.3gp')
                        x,y = self.device(description=self.appconfig("downloadname","Chrome")).get_location()
                        self.adb.shell("input tap %s %s" %(x,y))
                        self.logger.debug("Drag down the status bar")
                        self.device.drag(400, 50, 400, 1000, 10)
                        if self.device(resourceId=self.appconfig("android_id_progress","Chrome")).wait.exists(timeout=20000):
                            self.logger.debug('Downloading......')
                            if self.device(resourceId=self.appconfig("android_id_progress","Chrome")).wait.gone(timeout=2400000):
                                if self.device(text='Download complete').exists:
                                    self.logger.debug('File download success!')
                                    return True
                self.logger.debug('File download fail!')
                return False
            except Exception,e:
                self.save_fail_img()
            finally:
                self.back_to_chrome()
        self.logger.debug('Download file Test complete')

    #-------------------------------------to do-------------------------------  
    def select_menu(self,menu_text):
        """enter node of menu
        """
        self.logger.debug('enter menu: '+ menu_text)
        if self.device(text = self.appconfig("bookmarks_title","Chrome")).exists:
            return True
        self.device(description=self.appconfig("options","Chrome")).click()
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
        bookmark = self.device(resourceId="com.android.chrome:id/bookmarks_list_view").child(index=number)
        if bookmark.wait.exists(timeout=self.timeout):
            bookmark.click()
            self.logger.debug('loading...')
            progress = self.device(resourceId=self.appconfig.id("id_progress","Chrome"))     
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
    a = Chrome("a7ffc62c","Chrome")
    a.setup()
    
