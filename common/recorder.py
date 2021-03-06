"""Recorder library for scripts.
"""

import re
import sys
from common import Common


class Recorder(Common):
    
    """Provide common functions involved Sound Recorder."""
    
    def enter(self):
        """Launch Recorder by StartActivity.
        """       
        self.logger.debug('enter Soundrecorder')
        if self.device(resourceId = self.appconfig.id("id_record","Recorder")).wait.exists(timeout = self.timeout):
            return True
        self.start_app(self.appconfig("name","Recorder"))
        if self.device(resourceId = self.appconfig.id("id_record","Recorder")).wait.exists(timeout = self.timeout):
            return True
        else:
            self.logger.warning('enter Soundrecorder fail!')
            return False
    
    def back_main_app(self):
        self.logger.debug("Back to main app")
        for i in range(5):
            if self.device(resourceId = self.appconfig.id("id_record","Recorder")).exists:
                return True
            self.device.press.back()
            self.device.delay(1)
        else:
            self.logger.warning("Cannot back to main app")
            
    def get_storage_num(self):
        return self.get_file_num(self.appconfig("storage","Recorder"),".amr")+self.get_file_num(self.appconfig("storage","Recorder"),".m4a")+self.get_file_num(self.appconfig("storage","Recorder"),".3gpp")

    def record(self, duration=5): 
        """record audio several seconds.  
        argv: (int)duration -- recording time
        """
        self.logger.debug("Record audio %s seconds." % duration)
        file_num = self.get_storage_num()
        
        if self.device(resourceId=self.appconfig.id("id_start","Recorder")).wait.exists(timeout = self.timeout):
            self.device(resourceId=self.appconfig.id("id_start","Recorder")).click()
        if not self.device(resourceId = self.appconfig.id("id_timerView","Recorder")).wait.exists(timeout = self.timeout):
            self.logger.warning("Fail to start recording!")
            return False
        self.device.delay(duration)
        self.logger.debug("Stop recording audio")
        self.device(resourceId = self.appconfig.id("id_stop","Recorder")).click()
        self.device.delay(2)
        if self.device(text="Save").wait.exists(timeout = self.timeout):
            self.device(text="Save").click()
        if file_num >= self.get_storage_num():
            self.logger.warning("Save audio failed.")
            return False
        else:
            self.back_main_app()
            return True
            
    def enter_audio_list(self):
        """Enter audio file list.
        """
        self.logger.debug("Enter Audio List")
        if self.device(resourceId=self.appconfig.id("id_filelist","Recorder")).wait.exists(timeout = self.timeout):
            self.device(resourceId=self.appconfig.id("id_filelist","Recorder")).click()
        if not self.device(text=self.appconfig("filelist_title","Recorder")).wait.exists(timeout = self.timeout):
            self.logger.warning("Cannot Enter file list")
            return False
        return True

        
    def play(self,Index,duration=5):
        """touch audio according to index.  
        argv: (int)index -- file order in list
        """
        if self.device(resourceId = self.appconfig.id("id_item","Recorder"),index=Index).wait.exists(timeout = self.timeout):
            self.device(resourceId = self.appconfig.id("id_item","Recorder"),index=Index).child(resourceId="com.tct.soundrecorder:id/record_file_icon").click()
            if self.device(resourceId=self.appconfig.id("id_statebar","Recorder")).wait.exists(timeout = self.timeout):
                self.logger.debug("Start Playing...")
                self.device.delay(duration)
                self.back_main_app()
                return True   
        self.logger.warning("Cannot play audio.")
        return False
            
    def delete(self, Index=0):
        """delete audio
        
        argv: (int)index -- file order in list. Default is 0.
        """
        self.logger.debug("Delete Audio.")
        audio_num = self.get_storage_num()
        if self.device(resourceId = self.appconfig.id("id_item","Recorder"),index=Index):
            if self.product == "Alto5GL":
                self.device(resourceId = self.appconfig.id("id_item","Recorder"),index=Index).child(resourceId="com.tct.soundrecorder:id/record_file_duration").long_click()
            else:
                self.device(resourceId = self.appconfig.id("id_item","Recorder"),index=Index).child(resourceId="com.tct.soundrecorder:id/record_file_more").click()
        if self.device(text=self.appconfig("delete","Recorder")).wait.exists(timeout= 2000):
            self.device(text=self.appconfig("delete","Recorder")).click()
        if self.device(text=self.appconfig("delete_confirm","Recorder")).wait.exists(timeout= 2000):
            self.device(text=self.appconfig("delete_confirm","Recorder")).click()
        self.device.delay(2)
        if audio_num <= self.get_storage_num():
            self.logger.warning("Delete audio failed.")
            return False
        else:
            self.back_main_app()
            return True



if __name__ == '__main__':
    a = Recorder("adede7a6","Recorder")
    a.delete(0)
    