"""Camera library for scripts.
"""

import re
import sys
from common import Common,UIParser

class Music(Common):
        
    def enter(self):
        """Launch music by StartActivity.
        """          
        self.logger.debug('enter music')
        if self.device(resourceId="com.tct.music:id/scan_icon").wait.exists(timeout = 5000):
            return True
        self.start_app("Music",b_desk=False)
        if self.device(resourceId="com.tct.music:id/scan_icon").wait.exists(timeout = 5000):
            return True
        else:
            navigate_home = self.device(description = self.appconfig("navigate_home","Music"))
            if navigate_home.exists:
                navigate_home.click()
                return True
            self.logger.warning('enter music fail!')
            return False
    
    def enter_library(self):
        self.logger.debug("Enter the music library")
        if self.device(description="Open navigation drawer").exists:
            self.device(description="Open navigation drawer").click()
        if self.device(text=self.appconfig("library","Music")).exists:
            self.device(text=self.appconfig("library","Music")).click()
            if self.device(resourceId="android:id/action_bar").wait.exists(timeout = self.timeout):
                return True
        self.logger.warning("Cannot enter the library")
        return False

    def play(self,Index=0):
        """paly music 
        """
        self.logger.debug('play music')
        
        music_num = self.device(resourceId="com.tct.music:id/music_setting_image").count
        Index = Index % music_num
        if self.device(className=self.appconfig('class_library_view',"Music")).wait.exists(timeout = self.timeout):  
            music_name = self.device(resourceId="android:id/list").child(index=Index).child(index=1).child(resourceId="com.tct.music:id/line1").get_text()         
            self.device(resourceId="android:id/list").child(index=Index).child(index=1).child(resourceId="com.tct.music:id/line1").click() 
        self.device.delay(5)
        playing_name = self.device(resourceId="com.tct.music:id/title").get_text()
        if music_name == playing_name:
            self.logger.debug("Playing: %s" %music_name)
            if self.device(resourceId=self.appconfig.id("id_play","Music")).wait.exists(timeout = self.timeout):
                self.logger.debug("Play music success")
                self.device(resourceId=self.appconfig.id("id_play","Music")).click()
                return True
            return True
        else:
            self.logger.debug("play music fail: %s" %music_name)
            return False

    def _exit(self):
        """exit music 
        """
        options = self.device(resourceId = self.appconfig.id("id_options","Music"))
        exit_action = self.device(text=self.appconfig("exit_action","Music"))
        if options.exists:
            options.click()
            if exit_action.wait.exists(timeout = self.timeout):
                exit_action.click()
            if self.device(packageName = self.appconfig("package","Music")).wait.gone(timeout = self.timeout):
                return True
        return False

    def close(self):
        """close music 
        """
        self.logger.debug('close music')
        navigate_home = self.device(description = self.appconfig("navigate_home","Music"))
        if navigate_home.exists:
            navigate_home.click()
        return self._exit()

    
    def is_playing_music(self):
        """check if music is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media_session")
        if not data:
            return None
        if "state=PlaybackState {state=3" in data:
            self.logger.debug("The music is playing now")
            return True
        else:
            self.logger.debug("The music is not playing.")
            return False


class PlayMusic(Common):
        
    def enter(self):
        """Launch music by StartActivity.
        """          
        self.logger.debug('enter music')
        if self.device(resourceId="com.google.android.music:id/search").wait.exists(timeout = self.timeout):
            return True
        self.start_app("Play Music",b_desk=False)
        if self.device(resourceId="com.google.android.music:id/search").wait.exists(timeout = self.timeout):
            return True
        else:
            self.logger.warning('enter play music fail!')
            return False

    def setup(self):
        """Launch music by StartActivity.
        """          
        self.enter()
        step = [
               {"id":{"text":'Skip'},"assert":False},
               ]      
        return UIParser.run(self,step,self.close)        
 
    def enter_title(self,title):
        self.logger.debug("Enter the music %s"%title)
        if self.device(text=title).exists:
            return True
        if self.device(description="Show navigation drawer").exists:
            self.device(description="Show navigation drawer").click()       
        if self.device(text=title).wait.exists(timeout = self.timeout):
            self.device(text=title).click()
            if self.device(text=title).wait.exists(timeout = self.timeout):
                self.logger.warning("Cannot enter the %s"%title)
                return True          
        return False  
     
    def enter_library(self):
        return self.enter_title("My Library")

    def play(self,Index=0):
        """paly music 
        """
        self.logger.debug('play music')
        self.enter_library()  
        if self.device(text="SONGS").exists:
            self.device(text="SONGS").click()
        music_num = self.device(resourceId="com.google.android.music:id/icon").count
        music_index = Index % music_num + 1
        music_name = self.device(resourceId="android:id/list").child(index=music_index).child(resourceId="com.google.android.music:id/line1").get_text()
        self.device(resourceId="android:id/list").child(index=music_index).child(resourceId="com.google.android.music:id/line1").click()
        self.device.delay(5)
        playing_name = self.device(resourceId="com.google.android.music:id/trackname").get_text()
        if music_name == playing_name:
            self.logger.debug("Playing: %s" %music_name)
            self.device.delay(10)
            return True
        else:
            self.logger.debug("play music fail: %s" %music_name)
            return False

    def _exit(self):
        """exit music 
        """
        self.back_to_home()
        if self.device(packageName = self.appconfig("package","PlayMusic")).wait.gone(timeout = self.timeout):
            return True
        return False
    
    def is_playing_music(self):
        """check if music is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media_session")
        if not data:
            return None
        if "state=PlaybackState {state=3" in data:
            self.logger.debug("The music is playing now")
            return True
        else:
            self.logger.debug("The music is not playing.")
            return False

    def close(self):
        """close music 
        """
        self.logger.debug('close music')
        if self.is_playing_music():
            self.logger.debug('Stop music play')
            if self.device(description="Pause").exists:
                self.device(description="Pause").click()
            self.device.delay(2)
        return self._exit()

if __name__ == '__main__':
#     a = Music("adede7a6","Music")
#     a.enter()
#     a.enter_library()
#     a.play(2)
#     a.close()
#         
    s = "message23"
    
    a = re.findall(r"(.*)_.*", s,re.I);
    if a:
        print a[0]
    
    
    