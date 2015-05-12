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
from common.mail import Email
from common.telephony import Telephony
from common.message import Message
from common.configs import GetConfigs,Configs

def setup(serino):
    chrome = Chrome(serino,"Chrome")
    message = Message(serino,"Message")
    email = Email(serino,"Email")
    call = Telephony(serino,"call")
    
#     chrome.setup()
    message.setup()
    email.setup("atttest06@tcl.com", "Password001", "exchange")
    call.setup_contacts()    

if __name__ == '__main__':
    serino = "MDEVICE"
    serino = "a541c694"
    if len(sys.argv)>1:
        serino = sys.argv[1]
    setup(serino)
