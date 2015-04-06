
# -*- coding: UTF-8 -*-

from adb import Adb
from getconfigs import GetConfigs

class Lang:
    
    def __init__(self,device):
             
        self._lang = Adb(device).shell("getprop persist.sys.country").strip()
             
    def translate(self, lang_id):
        """get string from language.initActions
        
        argv: (str)lang_id -- option name in file
        author: Zhihao.Gu 
        """
        return unicode(GetConfigs.getstr(self._lang, lang_id, "language"),"utf8")