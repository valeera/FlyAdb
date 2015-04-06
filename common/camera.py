"""Camera library for scripts.
"""

import re
import sys
from common import Common

class Camera(Common):
   
    def enter(self):
        """Launch camera by StartActivity.
        """    
        if self.device(description=self.appconfig("Camera","shutter_action")).exists:
            return True
        else:      
            self.logger.debug('enter camera')
            self.start_app("Camera")
            self.device.delay(2)
            if self.device(text='Yes').exists:
                self.device(text='Yes').click()
                if self.device(text='Cancel').wait.exists(timeout = 2000):
                    self.device(text='Cancel').click()
            if self.device(description=self.appconfig("Camera","shutter_action")).exists:
                return True
            else:
                self.logger.debug('enter camera fail!')
                return False
            
    def back_to_camera(self):
        self.logger.debug("Back to camera")
        for i in range(5):
            if not self.device(description = "Navigate up").wait.exists(timeout=1000):
                self.adb.shell("input tap 540 450")
                if not self.device(description = "Navigate up").wait.exists(timeout=1000):
                    return True
            self.device.press.back()
            self.device.delay(1)
        else:
            self.logger.warning("Cannot back to camera")
            return False

    def get_photo_number(self):
        return self.get_file_num(self.appconfig("Camera","storage_path"),".jpg")

    def get_video_number(self):
        return self.get_file_num(self.appconfig("Camera","storage_path"),".mp4")   

    def mode(self):
        if self.device(text=self.appconfig("Camera","photo_settings")).exists:
            self.device.press.back()
            return "photo"
        elif self.device(text=self.appconfig("Camera","video_settings")).exists:
            self.device.press.back()
            return "video"
        else:
            self.device(resourceId= self.appconfig.id("Camera","id_setting_mode")).click()
            self.device.delay(2)
            if self.device(text=self.appconfig("Camera","photo_settings")).exists:
                self.device.press.back()
                return "photo"
            elif self.device(text=self.appconfig("Camera","video_settings")).exists:
                self.device.press.back()
                return "video"
        return None
    
    def switch_mode(self,mode):
        """switch camera mode(Camera, video, or panorama selector) 
        """         
        self.logger.debug('switch to %s mode',mode)
        self.device.delay(1)
        if self.mode()!=mode:
            self.device(resourceId=self.appconfig.id("Camera","id_camera_switch")).click()
            self.device.delay(2)
            if self.mode() != mode:
                self.logger.debug("Can not switch to %s"%mode)
                return True
        return True 
    
    def switch_picker(self,picker):
        """switch camera picker
        """         
        self.logger.debug('switch to %s picker' %picker)
        self.device.delay(1)
        if picker.lower() == "back":
            for i in range(3):
                if self.device(resourceId=self.appconfig.id("Camera","id_flash_picker")).wait.exists(timeout=3000):
                    return True
                self.device(resourceId=self.appconfig.id("Camera","id_camera_picker")).click()
        elif picker == "front":
            for i in range(3):
                if not self.device(resourceId=self.appconfig.id("Camera","id_flash_picker")).wait.exists(timeout=3000):
                    return True
                self.device(resourceId=self.appconfig.id("Camera","id_camera_picker")).click()
        else:
            self.logger.debug("Unknown argv: %s, back or front" %picker)
            return False
        self.logger.warning("Cannot switch to %s picker" %picker)
        return False
        
    def take_photo(self):
        """take photo 
        """         
        self.logger.debug('take photo')
        filenumber = self.get_photo_number()
        self.device(description=self.appconfig("Camera","shutter_action")).click()
        self.device.delay(5)
        if self.get_photo_number() > filenumber:
            return True
        else:
            self.logger.warning("Take picture failed!")
            return False

    def preview(self):
        """enter preview mode
        """   
        self.logger.debug('enter preview mode')
        self.adb.shell('input swipe 1050 700 50 700')
        maxtimes=0
        while not self.device(resourceId=self.appconfig.id("Camera","id_action_delete")).wait.exists(timeout = 2000):
            self.adb.shell('input swipe 1050 700 50 700')
            maxtimes+=1
            if maxtimes>5:
                self.logger.debug('enter preview mode failed!')
                return False
        self.logger.debug('enter preview mode success!')
        return True    
        
    def del_picture(self):
        """delete photo in preview mode
        """          
        if self.preview():
            filenumber = self.get_photo_number()
            self.adb.shell('input swipe 540 800 540 1700')
            self.device.delay(1)
            self.device.click(540,200)
            self.device.delay(4)
        if self.get_photo_number() < filenumber:
            return True
        else:
            self.logger.warning("Delete picture failed!")
            return False
     
    def record_video(self,duration = 5):
        """record video
        argv: (int)recordTime --time of the video
        """ 
        self.logger.debug('record video')
        filenumber = self.get_video_number()
        self.device(resourceId=self.appconfig.id("Camera","id_camera_video_switch_icon")).click()
        if not self.device(resourceId = self.appconfig.id("Camera","id_recording_time")).wait.exists(timeout = 2000):
            self.logger.warning("Fail to start recording!")
            return False
        self.device.delay(duration)
        self.device(resourceId=self.appconfig.id("Camera","id_camera_video_switch_icon")).click()
        self.device.delay(5)    
        if self.get_video_number() > filenumber:
            return True
        else:
            self.logger.warning("Record video failed!")
            return False
        
    def play_video(self,duration = 30):
        """play video
        """
        self.logger.debug('play video')
        self.preview()
        video = self.device(resourceId = self.appconfig.id("Camera","id_view")).child(className = "android.widget.FrameLayout",index=1).child(className = "android.widget.ImageView",index=1)
        if video.wait.exists(timeout = 2000):
            video.click()
            self.device.delay(1)
            video.click()
            self.device.delay(1)    
            if  self.device(text='Video player').exists:
                self.device(text='Video player').click()
                self.device.delay(1)
            if self.device(text='Just once').exists:
                self.device(text='Just once').click()
                self.device.delay(2)
            if self.is_playing_video():
                self.logger.debug('Video Playing...')
                self.device.delay(duration)
                self.device.press.back()
                self.device.delay(2)
                return True
        self.logger.warning("Play video failed!")
        return False

    def del_video(self):
        """delete video in preview mode
        """         
        if self.preview():
            filenumber = self.get_video_number()
            self.adb.shell('input swipe 540 800 540 1700')
            self.device.delay(1)
            self.device.click(540,200)
            self.device.delay(4)
            if self.get_video_number() < filenumber:
                return True
            else:
                self.logger.warning("Delete video failed!")
                return False

if __name__ == '__main__':
    a = Camera("56c051e1","Media")
    a.enter()
#     a.switch("video")
#     a.switch("video")
#     a.switch("photo")
#     a.take_photo()
#     a.del_picture()
    a.play_video(10)
    a.del_video()