#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath)

from common.browser import Browser
from common.chrome import Chrome
from common.camera import Camera
from common.telephony import Telephony
from common.message import Message
from common.configs import GetConfigs,Configs

def setup():
    chrome = Chrome(serino,"Chrome")
    chrome.setup()


if __name__ == '__main__':
     #serino = "MDEVICE"
    serino = "a7c0c6cf"
    if len(sys.argv)>1:
        serino = sys.argv[1]
    a = Chrome("a7c0c64c","Chrome")
    a.setup()
