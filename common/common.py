# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import logging 
import time
import re
from datetime import datetime
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if not libpath in sys.path:
    sys.path.append(libpath)
print libpath
from automator.uiautomator import Device 
from configs import GetConfigs,Configs
from automator.adb import Adb
import random
from configs import AppConfig

from functools import wraps
def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

class UIParser():
    @staticmethod
    def nest(self,func):
        def wrapper(*args,**kwargs):
            print args
            func(args)
        return wrapper
    @staticmethod
    def run(obj,params,exceptfunc = None):
        device = obj if isinstance(obj,Device) else obj.device
        def listfoo(param):
            resault = True
            if isinstance(param["content"],list):
                for content in param["content"]:
                    param_tmp = param
                    param_tmp["content"]=content
                    resault = resault and listfoo(param)
            elif param["id"] == "meta":
                getattr(obj,param["content"])(*param["action"]["param"] if param.has_key("action") and param("action").has_key("param") else [])
            else:
                select = device(**{param["id"]:param["content"]})
                action=select.wait.exists(timeout = 5000) if not param.has_key("wait") or (param.has_key("wait") and param["wait"]) else True
                if action and not (param.has_key("action") and param["action"]==None):
                    getattr(select,"click")(None) if not param.has_key("action") else getattr(select,param["action"]["type"])(*param["action"]["param"] if param["action"].has_key("param") else [])
                    time.sleep(param["action"]["delay"] if param.has_key("aciton") and param["action"].has_key("delay") else 0)
                resault = resault and action
            return resault
        
        def dictfoo(param):
            resault = True    
            if not param.has_key("id"):
                return False   
            if isinstance(param["id"],list):
                for content in param["id"]:
                    param_tmp = param
                    param_tmp["id"]=content
                    if param["id"].has_key("action"):
                        param_tmp["action"]=param["action"]
                    resault = resault and listfoo(param)
            elif param["id"].has_key("meta"):
                getattr(obj,param["id"]["meta"])(*param["action"]["param"] if param.has_key("action") and param("action").has_key("param") else [])
            else:
                select = device(**param["id"])
                action=select.wait.exists(timeout = 5000) if not param.has_key("wait") or (param.has_key("wait") and param["wait"]) else True
                if action and not (param.has_key("action") and param["action"]==None):
                    getattr(select,"click")(None) if not param.has_key("action") else getattr(select,param["action"]["type"])(*param["action"]["param"] if param["action"].has_key("param") else [])
                    time.sleep(param["action"]["delay"] if param.has_key("aciton") and param["action"].has_key("delay") else 0)
                resault = resault and action
            return resault
        
        for param in params:
            if isinstance(param,list):
                UIParser.run(obj,param)
            else:
                if param.has_key("id") and isinstance(param["id"],dict):
                    if not dictfoo(param):
                        print "%s error!"%param
                        exceptfunc() if (exceptfunc) else None
                        return False
                elif param.has_key("id") and param.has_key("content") and not isinstance(param["id"],dict):
                    if not listfoo(param):
                        print "%s error!"%param
                        exceptfunc() if (exceptfunc) else None
                        return False  
        return True

def create_folder():
    """Create folder to save pic & log.     
    Return a folder path or None
    Exception: OSError
    """
    log_path = os.environ.get("LOG_PATH")
    if log_path is None:
        log_path =  sys.path[0][sys.path[0].find(':')+1:] + '\\results'
    if not os.path.exists(log_path):
        logger.debug("log_path not exsit")
        os.makedirs(log_path)
    if not os.path.exists(log_path):
        return None
    return log_path

def createlogger(name): 
    """Create a logger named specified name with the level set in config file.  
    return a logger
    """
    config = GetConfigs("common")
    lev_key = config.getstr("Default","LOG_FITER","common").upper()
    lev_dict = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, 
                "WARNING": logging.WARNING, "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL}
    logger = logging.getLogger(name)
    logger.setLevel(lev_dict[lev_key])
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d: [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s',
        '%y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = createlogger("COMMON")

def log_traceback(traceback):
    """print traceback information with the log style.
    """
    str_list = traceback.split("\n")
    for string in str_list:
        logger.warning(string)

def connect_device(device_name):
    """connect_device(device_id) -> Device    
    Connect a device according to device ID.
    """
    environ = os.environ
    device_id = environ.get(device_name)
    if device_id == None:
        device_id = device_name       
    backend = Configs("common").get("Info","backend")
    logger.debug("Device ID is " + device_id + " backend is " + backend) 
    if backend.upper() == "MONKEY":
        from monkeyUser import MonkeyUser
        device = globals()["%sUser"%backend](device_id)
    else:
        device = Device(device_id)
    if device is None:
        logger.critical("Cannot connect device.")
        raise RuntimeError("Cannot connect %s device." % device_id)
    return device

def startactivity(serial,packet,activity): 
    """start activity
    """     
    adb = Adb(serial)
    data = adb.shell("am start -n %s/%s"%(packet,activity))
    if data.find("Error")>-1:
        return False
    return True

def random_name(index_num):
    numseed = "0123456789"
    logger.debug('Create a random name.')
    sa = []
    for i in range(5):
        sa.append(random.choice(numseed))
    stamp = ''.join(sa)
    strname = 'Autotest%02d_' %(index_num+1) +stamp
    return strname

class Common(object):  
    """Provide common functions for all scripts."""  
    def __init__(self, device,mod,timeout = 5000):
        self.timeout = timeout
        if isinstance(device, Device):
            self.device = device
        else:
            self.device = connect_device(device)
        self.logger = createlogger(mod)
        self.log_path = create_folder()
        self.config = GetConfigs("common")
        self.appconfig = AppConfig("appinfo")
        self.adb = self.device.server.adb
        self.suc_times = 0
        try:
            self.mod_cfg = GetConfigs(mod)
            self.test_times = 0
            self.dicttesttimes = self.mod_cfg.get_test_times()
            if mod == "Email":
                for i in self.dicttesttimes:
                    self.test_times += int(self.dicttesttimes[i])
                    if i <> 'opentimes':
                        self.test_times += int(self.dicttesttimes[i])
            elif mod == "Message":
                for i in self.dicttesttimes:
                    self.test_times += int(self.dicttesttimes[i])
                    if i == 'opentimes':
                        self.test_times += int(self.dicttesttimes[i])*3
            else:
                for test_time in self.dicttesttimes: self.test_times += int(self.dicttesttimes[test_time])
            self.logger.info("Trace Total Times " + str(self.test_times))
        except:
            pass

    def device(self):
        return self.device
           
    def save_fail_img(self, newimg = None):
        """save fail image to log path.        
        argv: The picture want to save as failed image.
        """
        path = (self.log_path + "\\" +datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".png")
        if newimg is None:
            self.logger.debug("Take snapshot.")
            newimg = self.device.screenshot(path)
        if newimg is None:
            self.logger.warning("newimg is None.")
            return False
        self.logger.error("Fail: %s" %(path))
        return True
    
    def get_file_num(self, path, format):
        """get number of file with specified format.
        """        
        content = self.adb.shell("ls " + path)
        num = content.count(format)
        self.logger.debug("%s file num is %d." % (format,num))
        return num

    def start_activity(self,packet,activity):      
        data = self.device.server.adb.shell("am start -n %s/%s"%(packet,activity))
        if data.find("Error")>-1:
            self.logger.error("Fail: %s/%s" %(packet,activity))
            return False
        return True

    def start_app(self,name,b_desk=True):
        '''Call/People/ALL APPS/Messaging/Browser'''   
        self.logger.debug("start app:%s" %(name))
        self.device.press.home()
        if b_desk and self.device(text=name).wait.exists(timeout = 2000):
            self.device(text=name).click()
            return True
        elif b_desk and self.device(description=name).wait.exists(timeout = 2000):
            self.device(text=name).click()
            return True
        elif self.device(description="ALL APPS").exists:
            self.device(description="ALL APPS").click()
            self.device().fling.horiz.toBeginning()
            for loop in range(5):  
                if self.device(description=name).exists:
                    self.device(description=name).click()
                    return True
                self.device().fling.horiz.forward()  
        elif self.device(description="Apps").exists:
            self.device(description="Apps").click()
            self.device().fling.horiz.toBeginning()
            for loop in range(5):  
                if self.device(description=name).exists:
                    self.device(description=name).click()
                    return True
                self.device().fling.horiz.forward()     
        return False

    def select_menu_item(self, stritem):
        self.device.press.menu()
        self.device.delay(1)
        self.device(text=stritem).click()        
        self.device.delay(2)
        
    def _is_connected(self,type):
        temp_type = type
        if type == "ALL":
            temp_type = "LTE"
        for i in range(5):
            if self.adb.get_data_service_state() == temp_type:
                break
            self.device.delay(5)
        else:
            self.logger.warning("Cannot get %s service." % (type))
            self.device.press.back()
            return False
        for i in range(5):
            if self.adb.get_data_connected_status():
                return True
            self.device.delay(5)
        else:
            self.logger.warning("Cannot connect %s data." % (type))
            self.device.press.back()
            return False 
        
    def switch_network(self,type = None):
        """switch network to specified type.    
        argv: (str)type -- the type of network.    
        """
        self.logger.debug("Switch network to %s." % (type))
        self.start_activity(self.appconfig("RadioInfo","package"),self.appconfig("RadioInfo","activity"))
        self.device.delay(2)
        network_type = self.appconfig("RadioInfo",type)
        print network_type
        self.device(scrollable=True).scroll.to(text=self.appconfig("RadioInfo","set"))
        if self.device(resourceId=self.appconfig.id("RadioInfo","id_network")).wait.exists(timeout = 2000):
            self.device(resourceId=self.appconfig.id("RadioInfo","id_network")).click()
        self.device(scrollable=True).scroll.to(text=network_type)       
        self.device.delay(1)
        self.device(text=network_type).click()
        self._is_connected(type)
        self.back_to_home()

    def back_to_home(self):
        """back_to_home.
        """
        for loop in range(4):
            self.device.press.back()
            self.device.delay(1)
            if self.device(text = "Quit").exists:
                self.device(text = "Quit").click()
        self.device.press.home()
        
    def is_playing_video(self):
        """check if video is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media.player")
        if not data:
            return None
        if "AudioTrack" in data:
            self.logger.debug("The video is playing now")
            return True
        else:
            self.logger.debug("The video is not playing.")
            return False
             
if __name__ == "__main__":
    a = Common("56c051e1","Media")
    a.start_app("Sound Recorder")
                
                