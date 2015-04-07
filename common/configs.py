# -*- coding: utf-8 -*-

import sys
import os
from ConfigParser import ConfigParser

class Configs(object):
    def __init__(self, module,subconfig = None):
        self.config = ConfigParser()
        m =  os.path.join(os.path.join(subconfig), "%s.ini"%module) if subconfig else "%s.ini"%module
        self.config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure",m))
    def get(self,section,option):
        """return an string value for the named option."""
        try:
            try:
                return self.config.getint(section, option)
            except:
                return self.config.get(section,option).strip('\'').strip('\"')
        except:
            return None

class AppConfig(Configs):
    def __call__(self, *args, **kwargs):
        return self.get(*args)
    def id(self,section,option):
        try:
            return "%s:%s"%(self.get(section,"package").strip('\'').strip('\"'),self.get(section,option).strip('\'').strip('\"'))
        except:
            return None

class GetConfigs(object):
    """Get a option value from a given section."""
    def __init__(self, module):
        self.commonconfig = ConfigParser()
#         self.commonconfig.read(sys.path[-1] + "\\common.ini")
        self.commonconfig.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","common.ini"))
        self.testtype = self.commonconfig.get("Default","TEST_TYPE").upper()
        self.networktype = self.commonconfig.get("Default","NETWORK_TYPE")
        self.module = module.capitalize()
    @staticmethod
    def getstr(section, option, filename, exc=None):
        """return an string value for the named option."""
        config = ConfigParser()
        try:
#             config.read(sys.path[-1] + "\\"+filename + ".ini")
            config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","%s.ini"%filename))
            return config.get(section,option)
        except Exception,e:
            print e
            return exc
    @staticmethod
    def getint(section, option, filename, exc=0):
        """return an integer value for the named option.
        return exc if no the option. 
        """
        config = ConfigParser()
        try:
#             config.read(sys.path[-1] + "\\"+filename + ".ini")
            config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","%s.ini"%filename))
            return config.getint(section, option)
        except:
            return exc

    def get_test_times(self):
        """return a dict with name:value for each option
        in the section.
        """
        config = ConfigParser()
        if self.testtype == "STABILITY" or self.testtype == "MINI":
#             config.read(sys.path[-1] + "\\"+self.testtype+"_"+self.networktype+".ini")
            config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","%s_%s.ini"%(self.testtype,self.networktype)))
        else:
#             config.read(sys.path[-1] + "\\"+self.testtype+".ini")
            config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","%s.ini"%self.testtype))
        item = config.items(self.module)
        return dict(item)


if __name__ == '__main__':
    config = Configs("configure","appinfo")
    print config