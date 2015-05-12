# -*- coding: UTF-8 -*-
"""Settings library for scripts.
"""
import re
import sys
from common import Common

class Settings(Common):
    """Provide common functions involved wifi,display,sound etc."""     
    def enter_settings(self,option):
        '''enter the option of settings screen
         argv: the text of the settings option
        '''
        self.logger.debug(option)  
        self.start_app("Settings")
        if self.device(text=self.appconfig("settings","Settings")).wait.exists(timeout = 2000):
            self.logger.debug("enter Settings") 
            if self.device(textStartsWith=option).exists:
                self.device(textStartsWith=option).click()
            else:
                self.device(scrollable=True).scroll.vert.forward(steps=100)
                if self.device(text=option).wait.exists(timeout = 10000):
                    self.device(text=option).click()
                else:
                    return False
            if self.device(text=self.appconfig("settings","Settings")).wait.gone(timeout = 2000):
                self.logger.debug("enter "+option+" setting")
                return True
        return False

    def switch_network(self,type = None):
        """switch network to specified type.    
        argv: (str)type -- the type of network.    
        """
        network_type = self.appconfig(type,"Settings")
        self.logger.debug("Switch network to %s:%s." % (type,network_type))
        if self.enter_settings(u"More…"):
            if self.device(text="Mobile networks").exists:
                self.device(text="Mobile networks").click()
            if self.device(text="Preferred network mode").wait.exists(timeout=self.timeout):
                self.device(text="Preferred network mode").click()
            if self.device(resourceId="android:id/buttonPanel").wait.exists(timeout=self.timeout):
                self.device(text=network_type).click()
        print self._is_connected(type)
        self.back_to_home()

class Wifi(Settings): 
    
    def enter(self):
        return self.enter_settings(self.appconfig("wifi","Settings"))
    
    def back_to_wifi(self):
        self.logger.debug('Back to Wi-Fi list')
        for loop in range(5):
            if self.device(resourceId = "com.android.settings:id/switch_bar").exists:
                return True
            self.device.press.back() 
            self.device.delay(1)
        return False
    
    def open(self):
        self.logger.debug('Open wifi')
        if self.device(checked="false",className='android.widget.Switch').exists:
            self.device(className='android.widget.Switch').click()
        if self.device(textContains='To see available networks').wait.gone(timeout = 10000):
            self.device.delay(10)
            return True
        self.logger.debug('wifi open fail!!!')
        return False

    def close(self):
        self.logger.debug('Close wifi')
        if self.device(checked='true',className='android.widget.Switch'):
            self.device(className='android.widget.Switch').click()
        if self.device(textContains='To see available networks').wait.exists(timeout = 10000):
            return True
        self.logger.debug('wifi close fail!')
        return False
       
    def _connect(self,hotspot,password,security):
        '''device connect wifi hotspot
         argv: (str)hotspotName -- the wifi hotspot's name 
               (str)password -- the wifi hotspot's password
               (str)security -- the password type
        '''       
        self.logger.debug('Add hotspot --> '+hotspot)
        if self.device(description="More options").exists:
            self.device(description="More options").click()
        if self.device(text="Add network").wait.exists(timeout=self.timeout):
            self.device(text="Add network").click()
        self.logger.debug("Input SSID/PWD/Security")
        if self.device(resourceId="com.android.settings:id/ssid").wait.exists(timeout=self.timeout):
            self.device(resourceId="com.android.settings:id/ssid").set_text(hotspot)
            if password != "":
                self.logger.debug("Select security")
                self.device(resourceId="com.android.settings:id/security").click()
                self.device.delay(1)
                self.device(text=security).click()
                self.device.delay(1)
                self.device(resourceId="com.android.settings:id/password").set_text(password)
                self.device.delay(2)
        print self.appconfig("wifi_connect","Settings")
        self.device(text=self.appconfig("wifi_connect","Settings")).click()
        self.device.delay(2)
        self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
        if self.device(text="Connected").wait.exists(timeout=10000):
            self.logger.debug('wifi connect success!!!')
            self.device.delay(10)
            return True  
        else:
            self.logger.debug('can not find hotspot: %s',hotspot)
            return False
        self.logger.debug('wifi connect fail!!!')        
        return False

    def forget(self,hotspot):
        self.logger.debug('forget hospot')
        self.logger.debug('Search hotspot-------> '+hotspot)      
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(text=hotspot)
        if self.device(text=hotspot).wait.exists(timeout = 30000):
            self.device(text=hotspot).long_click()
            if self.device(textContains='Forget').wait.exists(timeout = 2000):
                self.device(textContains='Forget').click()
                if self.device(text="Connected").wait.gone(timeout = 3000):
                    self.device.delay(10)
                    return True
            else:
                self.device.press.back()
                self.logger.debug(hotspot+' is not connected!!!')
                return True
        return False
    
    def _switch(self,times = 1):
        self.logger.debug('Switch wifi')
        if self.device(checked='false',className='android.widget.Switch'):
            self.device(className='android.widget.Switch').click()
            if self.device(textContains='To see available networks').wait.gone(timeout = 10000):
                self.logger.debug('wifi is opened!')
                return True
            else:
                self.logger.debug('wifi open fail!!!') 
                return False
        else:
            self.device(className='android.widget.Switch').click()
            if self.device(textContains='To see available networks').wait.exists(timeout=10000):
                self.logger.debug('wifi is closed!')
                return True
            else:
                self.logger.debug('wifi close fail!!!')
                return False
        return False
 
    def switch(self,times):
        if self.enter():
            for loop in range(times):
                try:
                    self.logger.debug("Wifi switch "+str(loop+1)+" Times")
                    if self._switch():
                        self.suc_times+=1
                        self.logger.info("Trace Success Loop "+ str(loop + 1))
                    else:
                        self.save_fail_img()
                except Exception,e:
                    self.logger.warning("wifi switch fail!")
                    self.save_fail_img()
            #               common.common.log_traceback(traceback.format_exc())
                    self.enter()
        self.logger.debug("Wifi Switch Test Mission Complete")

    def connect(self,ssid,pwd,security,times = 1):
        self.logger.debug("Dis/Connect Wifi %s Times." % times)
        if self.enter() and self.open():
            for loop in range(times):
                try:
                    if self.device(text="Connected").wait.exists(timeout=3000):
                        self.logger.debug("Disconnect wifi first!")
                        self.device(text="Connected").long_click()
                        if self.device(textContains='Forget').wait.exists(timeout = 2000):
                            self.device(textContains='Forget').click()
                    if self._connect(ssid,pwd,security) and self.forget(ssid):
                        self.suc_times+=1
                        self.logger.info("Trace Success Loop "+ str(loop + 1))
                    else:
                        self.save_fail_img()
                        self.back_to_wifi()
                except Exception,e:
                    self.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
                    self.back_to_wifi()
        self.logger.debug("Wifi Connect And Disconnect Test Mission Complete")  


class Airplane(Settings): 
    def enter(self):
        print self.appconfig("More","Settings")
        if self.enter_settings(self.appconfig("More","Settings")):
            if self.device(text='Airplane mode').wait.exists(timeout=2000):
                return True
    def switch(self):
        self.logger.debug('Switch Airplane')
        if self.device(resourceId="android:id/list").child(index=0).child(checked='false',className='android.widget.Switch'):
            self.device(resourceId="android:id/list").child(index=0).child(className='android.widget.Switch').click()
            if self.device(resourceId="android:id/list").child(index=0).child(checked='true',className='android.widget.Switch').wait.exists(timeout=10000):
                self.logger.debug('Airplane is opened!')
                return True
            else:
                self.logger.debug('Airplane open fail!!!')
        else:
            self.device(resourceId="android:id/list").child(index=0).child(className='android.widget.Switch').click()
            self.device.delay(2)
            if self.device(resourceId="android:id/list").child(index=0).child(checked='false',className='android.widget.Switch').wait.exists(timeout=10000):
                self.logger.debug('Airplane is exit!')
                return True
            else:
                self.logger.debug('Airplane exit fail!!!')
        return False
 
class Bt(Settings):
    def enter(self):
        return self.enter_settings(self.appconfig("bt","Settings"))
       
    def switch(self):
        self.logger.debug('Switch bt')
        if self.device(checked='false',className='android.widget.Switch'):
            self.device(className='android.widget.Switch').click()
            if self.device(text='Available devices').wait.exists(timeout=10000):
                self.logger.debug('bt is opened!')
                return True
            else:
                self.logger.debug('bt open fail!!!')
        else:
            self.device(className='android.widget.Switch').click()
            self.device.delay(2)
            if self.device(textStartsWith='When Bluetooth is turned on').wait.exists(timeout=10000):
                self.logger.debug('bt is closed!')
                return True
            else:
                self.logger.debug('bt close fail!!!')
        return False

if __name__ == '__main__':
    a = Airplane("e8d3e0c2","Settings")
    a.enter()
