import os
import sys
from common import *

class Schedule(Common):
    """Provide common functions involved Calendar."""
    
    def enter_calendar(self):
        '''Launch calender by start activity.
        '''
        if self.device(resourceId= self.appconfig.id("id_enter","Calendar")).wait.exists(timeout = self.timeout):
            return True
        self.start_app("Calendar")
        if self.device(text= "Just a sec?").wait.exists(timeout = self.timeout):
            self.device.press.back()    
        if self.device(resourceId= self.appconfig.id("id_enter","Calendar")).wait.exists(timeout = self.timeout):
            return True
        else:
            return False  
        
    def back_to_calendar(self):
        self.logger.debug('Back to Calendar')
        for i in range(5):
            if self.device(resourceId=self.appconfig.id("id_enter","Calendar")).exists:
                break
            self.device.press.back()
            self.device.delay(1)
        else:
            self.logger.warning('Back to message list fail')
            
    def switch_view(self, strsort):
        """Switch to specified view.
        """
        def _check_view_type(strsort):
            if ((strsort == "Agenda" or strsort == "Schedule") and self.device(resourceId= self.appconfig.id("id_switch_agenda","Calendar")).exists):
                return True
            elif (strsort == "Week" and
                self.device(resourceId= self.appconfig.id("id_switch_week","Calendar")).exists):
                return True
            elif (strsort == "Month" and self.device(resourceId= self.appconfig.id("id_switch_month","Calendar")).exists):
                return True
            elif (strsort == "Day" and self.device(textContains=self.appconfig("switch_today","Calendar"))):
                return True
            else:
                self.logger.warning("Not In %s." % strsort)
                return False
        self.logger.debug("Switch to %s view." % strsort)
        if not _check_view_type(strsort):
            self.device(resourceId= self.appconfig.id("id_action_bar","Calendar")).click()
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
        if self.device(resourceId=self.appconfig.id("id_floating_action_button","Calendar")).exists:
            self.device(resourceId=self.appconfig.id("id_floating_action_button","Calendar")).click()
        elif self.device(description=self.appconfig("create_option","Calendar")).exists:
            self.device(description=self.appconfig("create_option","Calendar")).click()
            if self.device(text = "New event").wait.exists(timeout = self.timeout):
                self.device(text = "New event").click()
                if self.device(text = "No calendars").wait.exists(timeout = 2000):
                    self.device(text = "Cancel").click()  
        self.logger.debug('input event name')
        self.device.delay(2)
        self.device(text= self.appconfig("create_event_name_text","Calendar")).set_text(event_name)
        self.device.delay(2)
        self.logger.debug('select calendar date')
        if not self.device(resourceId= "com.tct.calendar:id/start_date").exists:
            self.device.press.back()
        if self.device(resourceId=self.appconfig.id("start_date","Calendar")).wait.exists(timeout=self.timeout):
            self.device(resourceId=self.appconfig.id("start_date","Calendar")).click()
        if self.device(resourceId=self.appconfig.id("animator","Calendar")).wait.exists(timeout=5000):
            self.device(resourceId=self.appconfig.id("animator","Calendar")).child(index=0).child(index=0).child(index=Index).click()
        self.device(resourceId= self.appconfig.id("id_done","Calendar")).click()
        self.device.delay(2)
        self.logger.debug('Save calendar')
        if self.device(resourceId= self.appconfig.id("id_action_done","Calendar")).exists:
            self.device(resourceId= self.appconfig.id("id_action_done","Calendar")).click()
            self.device.delay(2) 
            if self.device(text="Agenda").exists: 
                self.device(text="Agenda").click()
        self.device.delay(2)
        if self.device(text=event_name).exists:
            return True
        elif self.device(resourceId= self.appconfig.id("id_switch_agenda","Calendar"),scrollable=True).exists:
            self.device(resourceId= self.appconfig.id("id_switch_agenda","Calendar"),scrollable=True).scroll.to(text=event_name)
            if self.device(text=event_name).exists:
                return True
        else:
            self.logger.warning("Cannot find the calendar added.")
            return False

    def delete_calendar(self,name=None):
        self.logger.debug('delete calendar:%s' %name)
        if self.device(textStartsWith=name).exists:
            self.device(textStartsWith=name).click()
        elif self.device(resourceId= self.appconfig.id("id_switch_agenda","Calendar"),scrollable=True).exists:
            self.device(scrollable=True).scroll.vert.toBeginning(steps=10)
            self.device(scrollable=True).scroll.vert.to(textStartsWith=name)
            self.logger.warning("Cannot find the calendar %s" %name)
            return False
        if self.device(description= self.appconfig("delete_action","Calendar")).wait.exists(timeout=5000):
            self.device(description= self.appconfig("delete_action","Calendar")).click()
            delete_confirm = self.appconfig("delete_confirm","Calendar")
            if self.device(text=delete_confirm).wait.exists(timeout = self.timeout):
                self.device(text=delete_confirm).click()
                self.device.delay(2)
                return True
        self.logger.debug('delete calendar fail!')
        return True
    
    def enter_alarm(self):
        '''Launch alarm by start activity.
        '''
        alarm = self.appconfig("switch_alarm","Alarm")
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
        id_add = self.appconfig.id("id_add","Alarm")
        self.logger.debug("Add an alarm without change.")
        if self.device(resourceId= id_add).exists:
            self.device(resourceId= id_add).click()
            self.device.delay(2)
            self.device(text= self.appconfig("add_comfirm","Alarm")).click()
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
        delete_action = self.appconfig("delete_action","Alarm")
        if not self.device(description = delete_action).exists:
            self.device(resourceId= self.appconfig.id("delete_option","Alarm")).click()       
        if not self.device(description = delete_action).wait.exists(timeout = self.timeout):
            self.logger.debug('delete alarm fail!')
            return False
        self.device(description = delete_action).click()
        self.device.delay(2)
        delete_confirm = self.appconfig("delete_confirm","Alarm")
        if delete_confirm!=None and self.device(text= delete_confirm).exists:
            self.device(text= delete_confirm).click()
        return True

    def add_calendars(self,times):
        self.logger.debug('Add an Calendar ' + str(times) + ' Times')
        if self.enter_calendar() and self.switch_view(self.appconfig("name","Calendar")):
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
        if self.enter_calendar() and self.switch_view(self.appconfig("name","Calendar")):
#             self.device(text="Agenda").click()
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
    a = Schedule("f8e3ecd8","Schedule")
#     a.add_calendars(5)
#     a.delete_calendars(5)
    a.delete_alarms(2)

    
