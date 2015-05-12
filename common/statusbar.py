from common import Common

class StatusBar(Common):
    '''
    classdocs
    '''
    def drag_down(self):
        self.logger.debug("Drag status bar down")
        self.device.open.notification()
        for i in range(5):
            if self.device(resourceId="com.android.systemui:id/quick_settings_panel").exists:
                return True
            if self.product == "Sprints":
                self.adb.shell("input swipe 540 50 540 1700")
            else:
                self.adb.shell("input swipe 250 80 250 800")
            self.device.delay(1)
        else:
            self.logger.warning("Cannot drag status bar down")
            return False
        
    def switch_wifi(self):
        self.logger.debug('Switch wifi')
        wifi_switcher = self.device(resourceId="com.android.systemui:id/quick_settings_panel").child(index=2).child(index=0)
        if self.device(description='Wi-Fi is off.'):
            wifi_switcher.click()
            if self.device(description='Wi-Fi is off.').wait.gone(timeout = 10000):
                self.logger.debug('wifi is opened!')
                return True
            else:
                self.logger.debug('wifi open fail!!!') 
                return False
        else:
            wifi_switcher.click()
            if self.device(description='Wi-Fi is off.').wait.exists(timeout=10000):
                self.logger.debug('wifi is closed!')
                return True
            else:
                self.logger.debug('wifi close fail!!!')
                return False
            
    def switch_Bt(self):
        self.logger.debug('Switch BT')
        bt_switcher = self.device(resourceId="com.android.systemui:id/quick_settings_panel").child(index=4).child(index=0)
        if not self.device(description='Bluetooth on.').exists:
            bt_switcher.click()
            if self.device(description='Bluetooth on.').wait.exists(timeout = 10000):
                self.logger.debug('Bluetooth is opened!')
                return True
            else:
                self.logger.debug('Bluetooth open fail!!!') 
                return False
        else:
            bt_switcher.click()
            if self.device(description='Bluetooth on.').wait.gone(timeout=10000):
                self.logger.debug('Bluetooth is closed!')
                return True
            else:
                self.logger.debug('Bluetooth close fail!!!')
                return False
            
    def switch_airplane(self):
        self.logger.debug('Switch airplane')
        bt_switcher = self.device(resourceId="com.android.systemui:id/quick_settings_panel").child(index=3).child(index=0)
        if self.device(description='Airplane mode off.').exists:
            bt_switcher.click()
            if self.device(description='Airplane mode on.').wait.exists(timeout = 10000):
                self.logger.debug('Airplane mode open!')
                return True
            else:
                self.logger.debug('Airplane mode open fail!!!') 
                return False
        else:
            bt_switcher.click()
            if self.device(description='Airplane mode off.').wait.exists(timeout=10000):
                self.logger.debug('Airplane mode exit.')
                return True
            else:
                self.logger.debug('Airplane mode exit fail.')
                return False
        