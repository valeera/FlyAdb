# -*- coding: UTF-8 -*-
"""Settings library for scripts.
"""
import re
import sys
from common import Common,connect_device,createlogger
#from browser import Browser
from chrome import Chrome
from music import Music
from configs import GetConfigs,AppConfig
from recorder import Recorder
from camera import Camera

class Media():

    def __init__(self, device, mod):
        self.device = connect_device(device)
        self.appconfig = AppConfig("appinfo")
        self.logger = createlogger(mod)
        self.camera = Camera(self.device,"media_camera")
        self.record = Recorder(self.device,"media_recorder")
        #self.browser = Browser(self.device,"media_browser")
        self.chrome = Chrome(self.device,"media_chrome")
        self.music = Music(self.device,"media_music")
        self.suc_times = 0
        self.mod_cfg = GetConfigs(mod)
        self.test_times = 0
        self.dicttesttimes = self.mod_cfg.get_test_times()
        
        for i in self.dicttesttimes:
            self.test_times += int(self.dicttesttimes[i]) 
            if i.upper() in ('VIDEOTIMES','RECORDER','PHOTOTIMES'):
                self.test_times +=int(self.dicttesttimes[i]) * 2
        self.logger.info('Trace Total Times ' + str(self.test_times))


  
    def record_video(self,times = 1):
        number = 0
        self.logger.debug("Record video 30s "+str(times)+' Times')
        if self.camera.enter():
            try:
                #self.camera.switch('video')
                for loop in range(times):
                    self.logger.debug("Taking video")
                    if not self.camera.record_video(30):
                        self.camera.save_fail_img()
                    else:
                        self.suc_times += 1
                        number +=1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                    self.camera.back_to_camera()
            except Exception,e:
                self.camera.save_fail_img()
#                 common.common.log_traceback(traceback.format_exc())
                self.camera.back_to_camera()
                #self.camera.mode('video')
        self.logger.debug('Record video Test complete')
        return number
     
    def play_video(self,times):
        self.logger.debug("Play Back video "+str(times)+' Times')
        if self.camera.enter():
            try:
                for loop in range(times):
                    if self.camera.play_video():
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                    self.camera.back_to_camera()
            except Exception,e:
                self.camera.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
                self.camera.back_to_camera()
        self.logger.debug('Play Back video Test complete')
     
    def del_video(self,times):
        self.logger.debug("Delete video "+str(times)+' Times')
        if self.camera.enter():
            for loop in range(times):
                try:
                    if self.camera.del_video():
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                    else:
                        self.camera.save_fail_img()
                    self.camera.back_to_camera()
                except Exception,e:
                    self.camera.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
                    self.camera.back_to_camera()
        self.logger.debug('Delete video Test complete')
     
    def take_photo(self,times):
        number = 0
        self.logger.debug("Take photo "+str(times)+' Times')
        if self.camera.enter():
            try:
                #self.camera.switch('photo')
                for loop in range(times):
                    self.logger.debug("Taking photo")
                    if not self.camera.take_photo():
                        self.camera.save_fail_img()
                    else:
                        self.suc_times += 1
                        number +=1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                    self.camera.back_to_camera()
            except Exception,e:
                self.camera.save_fail_img()
#                 common.common.log_traceback(traceback.format_exc())
                self.camera.back_to_camera()
        self.logger.debug('Take photo Test complete')
        return number
     
    def open_photo(self,times):
        self.logger.debug("Open photo "+str(times)+' Times')
        if self.camera.enter():
            try:
                for loop in range(times):
                    if self.camera.preview():
                        if self.device(resourceId = self.appconfig.id("Camera","id_view")).child(className = "android.widget.ImageView",index=1).wait.exists(timeout = 2000):
                            self.device.click(600,600)
                        if self.device(resourceId = "com.tct.camera:id/filmstrip_bottom_control_share").wait.exists(timeout = 2000):  
                            self.logger.info("Trace Success Loop "+ str(loop+1))
                            self.suc_times += 1
                        else:
                            self.logger.warning("Cannot not preview picture")
                            self.camera.save_fail_img()
                    self.camera.back_to_camera()
            except Exception,e:
                self.camera.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
                self.camera.back_to_camera()
        self.logger.debug('Open Photo Test complete')
     
    def del_photo(self,times):
        self.logger.debug("Delete Photo " + str(times) +" Times")
        if self.camera.enter():
            for loop in range(times):
                try:
                    if self.camera.del_picture():
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                    else:
                        self.camera.save_fail_img()
                    self.camera.back_to_camera()
                except Exception,e:
                    self.camera.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
                    self.camera.back_to_camera()
        self.logger.debug('Delete Photo Test complete')

    def record_audio(self,times):
        self.logger.debug("Record Audio 5s "+str(times)+' Times')
        number = 0    
        try:
            for loop in range(times):
                if self.record.enter() and self.record.record():   
                    self.suc_times += 1
                    number += 1
                    self.logger.info("Trace Success Loop "+ str(loop+1))
                else:
                    self.record.save_fail_img()
        except Exception,e:
            self.record.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
            self.record.enter()
        self.logger.debug('record audio Test complete')
        return number
     
    def play_audio(self,times):
        self.logger.debug("Play Back Audio "+str(times)+' Times')
        if self.record.enter():
            try:
                for loop in range(times):
                    self.record.enter_audio_list()
                    if self.record.play(0):   
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                    else:
                        self.record.save_fail_img()
            except Exception,e:
                self.record.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
                self.record.enter()
                self.record.enter_audio_list()
        self.logger.debug('play audio Test complete')

     
    def del_audio(self,times):
        self.logger.debug("Delete Audio "+str(times)+' Times')
        if self.record.enter():
            try:
                for loop in range(times):
                    self.record.enter_audio_list()
                    if self.record.delete():   
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                    else:
                        self.record.save_fail_img()
            except Exception,e:
                self.record.save_fail_img()
#                     common.common.log_traceback(traceback.format_exc())
                self.record.enter()
                self.record.enter_audio_list()
        self.logger.debug('Delete Audio Test complete')
             
    def streaming(self,times):
        self.logger.debug("Play Streaming " + str(times) +" Times")
        for loop in range(times):
            if self.chrome.enter():
                try:
                    self.chrome.chrome_webpage(self.appconfig("Media","steamaddress"))
                    self.device.delay(5)
                    self.device.click(540,890)
                    self.device.delay(5)
                    if self.chrome.is_playing_video():
                        self.logger.debug("Streaming playing...")
                        self.device.delay(25)
                        self.chrome.logger.info("Trace Success Loop "+ str(loop+1))
                        self.suc_times += 1
                    else:
                        self.logger.debug("Streaming playing failed.")
                        self.chrome.save_fail_img()
                except Exception,e:
                    self.chrome.save_fail_img()
                    print e
                finally:
                    self.chrome.back_to_home()
                    self.device.delay(3)
        self.logger.debug('Streamings Test complete')
             
    def oc_player(self,times):
        self.logger.debug("Open Close Player "+str(times)+" Times")
        for loop in range(times):
            try:
                if self.music.enter():
                    self.suc_times += 1
                    self.logger.info("Trace Success Loop "+ str(loop+1))
            except Exception,e:
                self.music.save_fail_img()
#                 common.common.log_traceback(traceback.format_exc())
            finally:
                self.music.back_to_home()
                self.device.delay(3)
                     
    def play_music(self,times):
        self.logger.debug("Play music "+str(times)+" Times")
        if self.music.enter() and self.music.enter_library():
            for loop in range(times):
                try:     
                    if self.music.play(loop):
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                except Exception,e:
                    self.music.save_fail_img()
                    self.music.enter()
    #                 common.common.log_traceback(traceback.format_exc())

    def close_music(self):
        self.logger.debug('Close music app.')
        try:
            if self.music.enter():
                if self.music.close():
                    self.suc_times += 1
                    self.logger.info("Trace Success Close Music App")
        except Exception,e:
            self.music.save_fail_img()
#             common.common.log_traceback(traceback.format_exc())
  
if __name__ == '__main__':
    a = Media("56cf51f0","Media")      
    a.record_audio(1)
    a.play_audio(1)
    a.del_audio(1)
