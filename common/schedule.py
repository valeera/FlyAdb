import os
import sys
from common import *

class Schedule(Common):
    """Provide common functions involved Calendar."""
    
    def enter_calendar(self):
        '''Launch calender by start activity.
        '''
        if self.device(resourceId= self.appconfig.id("Calendar","id_enter")).wait.exists(timeout = self.timeout):
            return True
        self.start_app("Calendar")
        if self.device(resourceId= self.appconfig.id("Calendar","id_enter")).wait.exists(timeout = self.timeout):
            return True
        else:
            return False  
        
    def back_to_calendar(self):
        self.logger.debug('Back to Calendar')
        for i in range(5):
            if self.device(resourceId=self.appconfig.id("Calendar","id_enter")).exists:
                break
            self.device.press.back()
            self.device.delay(1)
        else:
            self.logger.warning('Back to message list fail')
            
    def switch_view(self, strsort):
        """Switch to specified view.
        """
        def _check_view_type(strsort):
            if (strsort == "Agenda" and self.device(resourceId= self.appconfig.id("Calendar","id_switch_agenda")).exists):
                return True
            elif (strsort == "Week" and
                self.device(resourceId= self.appconfig.id("Calendar","id_switch_week")).exists):
                return True
            elif (strsort == "Month" and self.device(resourceId= self.appconfig.id("Calendar","id_switch_month")).exists):
                return True
            elif (strsort == "Day" and self.device(textContains=self.appconfig("Calendar","switch_today"))):
                return True
            else:
                self.logger.warning("Not In %s." % strsort)
                return False
        self.logger.debug("Switch to %s view." % strsort)
        if not _check_view_type(strsort):
            self.device(resourceId= self.appconfig.id("Calendar","id_action_bar")).click()
            if self.device(text=strsort).wait.exists(timeout = self.timeout):
                self.device(text=strsort).click()
                self.device(text=strsort).wait.gone(timeout = self.timeout)
        if _check_view_type(strsort):
            return True
        else:
            self.logger.debug('can not enter the view of '+strsort)
            return False
            
    def create_schedule(self, event_name, Index=1):
        self.logger.debug('create a new event')
        if self.device(resourceId=self.appconfig.id("Calendar","id_floating_action_button")).exists:
            self.device(resourceId=self.appconfig.id("Calendar","id_floating_action_button")).click()
        self.logger.debug('input event name')
        self.device.delay(2)
        self.device(text= self.appconfig("Calendar","create_event_name_text")).set_text(event_name)
        self.device.delay(2)
        self.logger.debug('select calendar date')
        if not self.device(resourceId= "com.tct.calendar:id/start_date").exists:
            self.device.press.back()
        if self.device(resourceId="com.tct.calendar:id/start_date").wait.exists(timeout=self.timeout):
            self.device(resourceId="com.tct.calendar:id/start_date").click()
        if self.device(resourceId="com.tct.calendar:id/animator").wait.exists(timeout=5000):
            self.device(resourceId="com.tct.calendar:id/animator").child(index=0).child(index=0).child(index=Index).click()
        self.device(resourceId= self.appconfig.id("Calendar","id_done")).click()
        self.device.delay(2)
        self.logger.debug('Save calendar')
        self.device(resourceId= self.appconfig.id("Calendar","id_action_done")).click()
        self.device.delay(2)    
        self.device(text="Agenda").click()
        self.device.delay(2)
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.to(text=event_name)
        if self.device(text=event_name).exists:
            return True
        else:
            self.logger.warning("Cannot find the calendar added.")
            return False

    def delete_calendar(self,name=None):
        self.logger.debug('delete calendar:%s' %name)
        if self.device(scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(textStartsWith=name)
        if self.device(textStartsWith=name).exists:
            self.device(textStartsWith=name).click()
        else:
            self.logger.warning("Cannot find the calendar %s" %name)
            return False
        if self.device(description= self.appconfig("Calendar","delete_action")).wait.exists(timeout=5000):
            self.device(description= self.appconfig("Calendar","delete_action")).click()
            delete_confirm = self.appconfig("Calendar", "delete_confirm")
            if self.device(text=delete_confirm).wait.exists(timeout = self.timeout):
                self.device(text=delete_confirm).click()
                self.device.delay(2)
                return True
        self.logger.debug('delete calendar fail!')
        return True
    
    def enter_alarm(self):
        '''Launch alarm by start activity.
        '''
        alarm = self.appconfig("Alarm","switch_alarm")
        if self.device(description=alarm).exists:
            self.device(description=alarm).click()
            self.device.delay(2)
            return True
        self.start_app("Time")
        self.device.delay(2)
        if self.device(description=alarm).exists:
            self.device(description=alarm).click()
            self.device.delay(2)
            return True
        else:
            return False

    def add_alarm(self):
        """add an alarm without change.
        """
        id_add = self.appconfig.id("Alarm","id_add")
        self.logger.debug("Add an alarm without change.")
        if self.device(resourceId= id_add).exists:
            self.device(resourceId= id_add).click()
            self.device.delay(2)
            self.device(text= self.appconfig("Alarm","add_comfirm")).click()
            self.device.delay(2)
            for i in range(3):
                if not self.device(resourceId="com.tct.timetool:id/onoff",checked=True).exists:
                    break
                self.device(resourceId="com.tct.timetool:id/onoff",checked=True).click()
                self.device.delay(1)
            return True
        self.logger.debug('alarm add fail!')
        return False
 
    def delete_alarm(self):
        '''Delete alarm.        
        '''
        self.logger.debug('delete a alarm')
        delete_action = self.appconfig("Alarm", "delete_action")
        if not self.device(description = delete_action).exists:
            self.device(resourceId= self.appconfig.id("Alarm","delete_option")).click()
            self.device.delay(2)
            if not self.device(description = delete_action).exists:
                self.logger.debug('delete alarm fail!')
                return False
        self.device(description = delete_action).click()
        self.device.delay(2)
        delete_confirm = self.appconfig("Alarm","delete_confirm")
        if self.device(text= delete_confirm).exists:
            self.device(text= delete_confirm).click()
        return True

    def add_calendars(self,times):
        self.logger.debug('Add an Calendar ' + str(times) + ' Times')
        if self.enter_calendar():
            for loop in range (times):
                try:
                    if self.create_schedule(random_name(loop),loop):
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))                        
                    else:
                        self.save_fail_img()
                except Exception,e:
                    self.save_fail_img()
#                     self.log_traceback(traceback.format_exc())
                    self.back_to_calendar()
            self.logger.debug('Add Calendar Test complete')
        return True
    
    def delete_calendars(self,times):
        self.logger.debug('Del an Calendar ' + str(times) + ' Times')
        if self.enter_calendar():
            self.device(text="Agenda").click()
            for loop in range (times):
                try:
                    cal_name = "Autotest%02d" %(loop+1)
                    if not self.delete_calendar(cal_name):
                        self.save_fail_img()
                    else:
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                except Exception,e:
                    self.save_fail_img()
                    self.logger.warning(e)
                    self.back_to_calendar()
        self.logger.debug('Del Calendar Test complete')
        return True    

    def add_alarms(self,times):
        self.logger.debug('Add an Alarm ' + str(times) + ' Times')
        if self.enter_alarm():
            for loop in range (times):
                try:
                    if not self.add_alarm():
                        self.save_fail_img()
                    else:
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                except Exception,e:
                    self.save_fail_img()
                    self.logger.warning(e)
                    self.enter_alarm()
        self.logger.debug('Add Alarm Test complete')
        return True   
    
    def delete_alarms(self,times):
        self.logger.debug('Del an Alarm ' + str(times) + ' Times')
        if self.enter_alarm():
            for loop in range (times):
                try:
                    if not self.delete_alarm():
                        self.save_fail_img()          
                    else:
                        self.suc_times += 1
                        self.logger.info("Trace Success Loop "+ str(loop+1))
                except Exception,e:
                    self.save_fail_img()
                    self.logger.warning(e)
                    self.enter_alarm()
        self.logger.debug('Delete Alarm Test complete')
        return True    
       
if __name__ == '__main__':
    a = Schedule("56c05072","Schedule")
    for k in range(20):
        a.add_calendars(5)
        a.delete_calendars(5)
    