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
        if self.device(resourceId=self.appconfig.id("Chrome","id_location_bar")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Chrome")
        if self.device(resourceId="com.android.chrome:id/terms_accept").wait.exists(timeout=5000):
            self.device(resourceId="com.android.chrome:id/terms_accept").click()
            if self.device(resourceId="com.android.chrome:id/positive_button").wait.exists(timeout=5000):
                self.device(resourceId="com.android.chrome:id/positive_button").click()
            if self.device(text="No, thanks").wait.exists(timeout=5000):
                self.device(text="No, thanks").click()
        if self.device(resourceId=self.appconfig.id("Chrome","id_location_bar")).wait.exists(timeout=self.timeout):
            return True
        else:
            return False
 
    def setup(self):      
        bookmark = [
                    {"id":"description","content":["More options","Bookmark this page"]},
                    {"id":{"text":"Save"}},
                    {"id":"meta","content":"back_to_chrome"}
                    ]
        self.chrome_webpage("www.baidu.com")
        UIParser.run(self,bookmark,self.back_to_chrome)
        pass
        
    def back_to_chrome(self):
        self.logger.debug('Back Chrome')
        for i in range(3):
            if self.device(resourceId=self.appconfig.id("Chrome","id_location_bar")).wait.exists(timeout=self.timeout):
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
        self.device(description=self.appconfig("Chrome","options")).click()
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(text=self.appconfig("Chrome","history"))
        if self.device(text=self.appconfig("Chrome","history")).wait.exists(timeout = 30000):
            self.device(text=self.appconfig("Chrome","history")).click()
        if self.device(description=self.appconfig("Chrome","cbd")).wait.exists(timeout=self.timeout):
            self.device(description=self.appconfig("Chrome","cbd")).click()
        clear = self.device(text=self.appconfig("Chrome","txt_clear"))
        if clear.wait.exists(timeout=self.timeout):
            clear.click()
        self.back_to_chrome()
        
    def chrome_webpage(self,website):
        """browser webpage
        """ 
        #widget position:the edit area of website 
        url_text = self.device(className='android.widget.EditText',resourceId=self.appconfig.id("Chrome","id_url_bar")) 
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
        progress = self.device(resourceId=self.appconfig.id("Chrome","id_progress"))
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
                if self.chrome_webpage(self.appconfig("Chrome","streamaddress")):
                    if self.device(text=self.appconfig("Chrome","Authentication")).wait.exists(timeout=self.timeout):
                        self.logger.debug('input user name:'+self.appconfig("Chrome","account_pwd"))
                        self.device(description=self.appconfig("Chrome","username"),
                                    className='android.widget.EditText').set_text(self.appconfig("Chrome","account_pwd"))
                        self.device.delay(1)
                        self.logger.debug('input password:'+self.appconfig("Chrome","account_pwd"))
                        self.device(description=self.appconfig("Chrome","password"),
                                    className='android.widget.EditText').set_text(self.appconfig("Chrome","account_pwd"))
                        self.device.delay(1)
                        self.device(text=self.appconfig("Chrome","login")).click()
                        self.device.delay(1)
                    if self.device(description=self.appconfig("Chrome","streamname")).wait.exists(timeout=self.timeout):
                        self.logger.debug('Choese dirty_dance_1_mp4_amr_14m_80kbps.3gp')
                        x,y = self.device(description=self.appconfig("Chrome","streamname")).get_location()
                        self.adb.shell("input tap %s %s" %(x,y))
                        if self.device(text=self.appconfig("Chrome","vp")).wait.exists(timeout=self.timeout):
                            self.device(text=self.appconfig("Chrome","vp")).click()
                        if self.device(text=self.appconfig("Chrome","always")).wait.exists(timeout=self.timeout):
                            self.device(text=self.appconfig("Chrome","always")).click()
                        if self.device(text=self.appconfig("Chrome","startover")).wait.exists(timeout=self.timeout):
                            self.device(text=self.appconfig("Chrome","startover")).click()
                        if self.device(description=self.appconfig("Chrome","vptb")).wait.exists(timeout=self.timeout):
                            self.logger.debug("loading movies... ...")
                        if self.device(resourceId=self.appconfig("Chrome","view_root")).wait.exists(timeout=self.timeout):
                            self.logger.debug('Long movies load success!')
                            maxtimes=1
                            while self.device(resourceId=self.appconfig("Chrome","view_root")).exists:
                                self.device.delay(10)
                                self.logger.debug('Playing %s secs' %(maxtimes*10))
                                if maxtimes > (duration/10):
                                    return True
                                maxtimes+=1
                            if self.device(description=self.appconfig("Chrome","streamname")).exists:
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
                if self.chrome_webpage(self.appconfig("Chrome","downloadaddress")):
                    if self.device(text=self.appconfig("Chrome","Authentication")).wait.exists(timeout=self.timeout):
                        self.logger.debug('input user name:'+self.appconfig("Chrome","account_pwd"))
                        self.device(description=self.appconfig("Chrome","username"),
                                    className='android.widget.EditText').set_text(self.appconfig("Chrome","account_pwd"))
                        self.device.delay(1)
                        self.logger.debug('input password:'+self.appconfig("Chrome","account_pwd"))
                        self.device(description=self.appconfig("Chrome","password"),
                                    className='android.widget.EditText').set_text(self.appconfig("Chrome","account_pwd"))
                        self.device.delay(1)
                        self.device(text=self.appconfig("Chrome","login")).click()
                        self.device.delay(1)
                    if self.device(description=self.appconfig("Chrome","downloadname")).wait.exists(timeout=self.timeout):
                        self.logger.debug('Choese dirty_dance_1_mp4_amr_14m_80kbps.3gp')
                        x,y = self.device(description=self.appconfig("Chrome","downloadname")).get_location()
                        self.adb.shell("input tap %s %s" %(x,y))
                        self.logger.debug("Drag down the status bar")
                        self.device.drag(400, 50, 400, 1000, 10)
                        if self.device(resourceId=self.appconfig("Chrome","android_id_progress")).wait.exists(timeout=20000):
                            self.logger.debug('Downloading......')
                            if self.device(resourceId=self.appconfig("Chrome","android_id_progress")).wait.gone(timeout=2400000):
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
    
if __name__ == '__main__':
    a = Chrome("a7c0c6cf","Chrome")
    a.setup()
    