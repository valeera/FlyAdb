#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath) 
from common.media import Media 
from common.settings import Settings

class TestMedia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        serino = "MDEVICE"
#         serino = "adede7a6"
        if len(sys.argv)>1:         
            serino = sys.argv[1] 
        cls.mod = Media(serino, "Media")
        cls.set = Settings(cls.mod.device, "Settings")
#         cls.set.switch_network("ALL")

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.debug('Muitl-Media Mission Complete')  
        cls.mod.logger.info("Success Times: %s." % cls.mod.suc_times)
        Rate = cls.mod.suc_times/cls.mod.test_times*100
        if Rate < 95 :
            cls.mod.logger.warning("Result Fail Success Rate Is " + str(Rate) + '%')
        else:
            cls.mod.logger.info("Result Pass Success Rate Is " + str(Rate) + '%')

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testStability(self):
        video_num  = self.mod.record_video(int(self.mod.dicttesttimes.get("VIDEOTIMES".lower())))
        if video_num:
            self.mod.play_video(video_num)
            self.mod.del_video(video_num)
        pic_num  = self.mod.take_photo(int(self.mod.dicttesttimes.get("PHOTOTIMES".lower())))
        if pic_num:
            self.mod.open_photo(pic_num)
            self.mod.del_photo(pic_num)
        aud_num  = self.mod.record_audio(int(self.mod.dicttesttimes.get("RECORDER".lower())))
        if aud_num:
            self.mod.play_audio(aud_num)
            self.mod.del_audio(aud_num)
  
        self.mod.streaming(int(self.mod.dicttesttimes.get('STREAMTIMES'.lower())))
        self.mod.oc_player(int(self.mod.dicttesttimes.get('OPENCLOSETIMES'.lower())))        
        self.mod.play_music(int(self.mod.dicttesttimes.get('MUSICPLAYTIMES'.lower())))
        self.mod.close_music()

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestMedia)  
    suite = unittest.TestSuite([suite1]) 
    unittest.TextTestRunner(verbosity=2).run(suite) 
    
