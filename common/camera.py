"""Camera library for scripts.
"""

import re
import sys
from common import Common

class Camera(Common):
   
    def enter(self):
        """Launch camera by StartActivity.
        """    
        if self.device(description=self.appconfig("shutter_action","Camera")).exists:
            return True
        else:      
            self.logger.debug('enter camera')
            self.start_app("Camera")
            self.device.delay(2)
            if self.device(text='Yes').exists:
                self.device(text='Yes').click()
                if self.device(text='Cancel').wait.exists(timeout = 2000):
                    self.device(text='Cancel').click()
            if self.device(description=self.appconfig("shutter_action","Camera")).exists:
                return True
            else:
                self.logger.debug('enter camera fail!')
                return False
            
    def back_to_camera(self):
        self.logger.debug("Back to camera")
        for i in range(5):
            if self.device(description=self.appconfig("shutter_action","Camera")).exists:
                return True           
#             if not self.device(description = "Navigate up").exists:
#                 self.adb.shell("input tap 540 450")
#                 if not self.device(description = "Navigate up").exists:
#                     return True
            self.device.press.back()
            self.device.delay(1)
        else:
            self.logger.warning("Cannot back to camera")
            return False

    def get_photo_number(self):
        return self.get_file_num(self.appconfig("storage_path","Camera"),".jpg")

    def get_video_number(self):
        return self.get_file_num(self.appconfig("storage_path","Camera"),".mp4")   

    def mode(self):
        if self.device(text=self.appconfig("photo_settings","Camera")).exists:
            self.device.press.back()
            return "photo"
        elif self.device(text=self.appconfig("video_settings","Camera")).exists:
            self.device.press.back()
            return "video"
        else:
            self.device(resourceId= self.appconfig.id("id_setting_mode","Camera")).click()
            self.device.delay(2)
            if self.device(text=self.appconfig("photo_settings","Camera")).exists:
                self.device.press.back()
                return "photo"
            elif self.device(text=self.appconfig("video_settings","Camera")).exists:
                self.device.press.back()
                return "video"
        return None
    
    def switch_mode(self,mode):
        """switch camera mode(Camera, video, or panorama selector) 
        """         
        self.logger.debug('switch to %s mode',mode)
        self.device.delay(1)
        if self.mode()!=mode:
            self.device(resourceId=self.appconfig.id("id_camera_switch","Camera")).click()
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
                if self.device(resourceId=self.appconfig.id("id_flash_picker","Camera")).wait.exists(timeout=3000):
                    return True
                self.device(resourceId=self.appconfig.id("id_camera_picker","Camera")).click()
        elif picker == "front":
            for i in range(3):
                if not self.device(resourceId=self.appconfig.id("id_flash_picker","Camera")).wait.exists(timeout=3000):
                    return True
                self.device(resourceId=self.appconfig.id("id_camera_picker","Camera")).click()
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
        if self.product == "Alto5GL":
            self.switch_mode("photo")
        else:
            if self.device(description= "Camera, video, or panorama selector").wait.exists(timeout = self.timeout):
                self.device(description= "Camera, video, or panorama selector").click()
                if self.device(description= "Switch to photo").wait.exists(timeout = self.timeout):
                    self.device(description= "Switch to photo").click()
        if self.device(resourceId=self.appconfig.id("id_shutter","Camera")).wait.exists(timeout = self.timeout):
            self.device(resourceId=self.appconfig.id("id_shutter","Camera")).click()
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
        if self.product == "Alto5GL":
            
            self.adb.shell('input swipe 400 300 100 300')
        else:
            self.adb.shell('input swipe 650 600 50 600')
        maxtimes=0
        while not self.device(resourceId=self.appconfig.id("id_action_delete","Camera")).wait.exists(timeout = 2000):
            if self.product == "Alto5GL":           
                self.adb.shell('input swipe 400 300 100 300')
            else:
                self.adb.shell('input swipe 650 600 50 600')
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
            if self.device(resourceId=self.appconfig.id("id_action_delete","Camera")).wait.exists(timeout = 2000):
                self.device(resourceId=self.appconfig.id("id_action_delete","Camera")).click()
            else:
                self.adb.shell('input swipe 540 800 540 1700')
                self.device.delay(1)            
                self.device.click(540,200)
        if self.device(text = "Deleted").wait.exists(timeout = 2000):
            self.device(text = "Deleted").click()
        self.device.delay(5)
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
        if self.product == "Alto5GL":
            self.switch_mode("video")
        else:           
            if self.device(description= "Camera, video, or panorama selector").wait.exists(timeout = self.timeout):
                self.device(description= "Camera, video, or panorama selector").click()
                if self.device(description= "Switch to video").wait.exists(timeout = self.timeout):
                    self.device(description= "Switch to video").click()
        if self.device(resourceId=self.appconfig.id("id_shutter","Camera")).wait.exists(timeout = self.timeout):
            self.device(resourceId=self.appconfig.id("id_shutter","Camera")).click()
#             else:      
#                 self.device(resourceId=self.appconfig.id("id_camera_video_switch_icon","Camera")).click()
        if not self.device(resourceId = self.appconfig.id("id_recording_time","Camera")).wait.exists(timeout = 2000):
            self.logger.warning("Fail to start recording!")
            return False
        self.device.delay(duration)
        self.device(resourceId=self.appconfig.id("id_shutter","Camera")).click()
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
        video = self.device(resourceId = self.appconfig.id("id_view","Camera")).child(className = "android.widget.FrameLayout",index=1).child(className = "android.widget.ImageView",index=1)
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
            if self.device(resourceId=self.appconfig.id("id_action_delete","Camera")).wait.exists(timeout = 2000):
                self.device(resourceId=self.appconfig.id("id_action_delete","Camera")).click()
            else:
                self.adb.shell('input swipe 540 800 540 1700')
                self.device.delay(1)
                self.device.click(540,200)
            if self.device(text = "Deleted").wait.exists(timeout = 2000):
                self.device(text = "Deleted").click()
            self.device.delay(5)
            if self.get_video_number() < filenumber:
                return True
            else:
                self.logger.warning("Delete video failed!")
                return False

if __name__ == '__main__':
    a = Camera("adede7a6","Media")
#     a.enter()
#     a.switch("video")
#     a.switch("video")
#     a.switch("photo")
#     a.take_photo()
#     a.del_picture()
#     a.record_video(10)
    a.play_video()
#     a.del_video()