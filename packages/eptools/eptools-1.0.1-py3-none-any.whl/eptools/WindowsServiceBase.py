'''
SMWinservice
by Davide Mastromatteo
Base class to create winservice in Python
-----------------------------------------
Instructions:
1. Just create a new class that inherits from this base class
2. Define into the new class the variables
   _svc_name_ = "nameOfWinservice"
   _svc_display_name_ = "name of the Winservice that will be displayed in scm"
   _svc_description_ = "description of the Winservice that will be displayed in scm"
3. Override the three main methods:
    def start(self) : if you need to do something at the service initialization.
                      A good idea is to put here the inizialization of the running condition
    def stop(self)  : if you need to do something just before the service is stopped.
                      A good idea is to put here the invalidation of the running condition
    def main(self)  : your actual run loop. Just create a loop based on your running condition
4. Define the entry point of your module calling the method "parse_command_line" of the new class
5. Enjoy
'''

import datetime
import logging
import os
import socket
import sys
import time
import servicemanager
import win32event
import win32service
import win32serviceutil
from .logger import createRotatingLogger, createSlackLogger

class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'pythonService'
    _svc_display_name_ = 'Python Service'
    _svc_description_ = 'Python Service Description'
    _svc_logger_ = 'pythonService_logger'
    _looptime_ = 5
    _daily_ = None
    _svc_logpath_ = 'C:\\logs\\pythonService\\'
    args = []
    logger = None
    slacker = None

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)
    
    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        self.args = [arg for arg in args]
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.isrunning = False
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self._svc_logger_ = self._svc_name_ + '_logger'
        self._svc_logpath_ = 'C:\\logs\\' + self._svc_name_ + '\\'
        if not os.path.exists(self._svc_logpath_):
            os.makedirs(self._svc_logpath_)
        self.logger = createRotatingLogger(self._svc_logger_ , self._svc_logpath_)
        self.slacker = createSlackLogger(self._svc_name_,self.logger)
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.isrunning = True
        self.main()


    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        if self._daily_:
            checker = datetime.datetime.now()
            # checks if next loop should start or not every second
            while self.isrunning:
                if datetime.datetime.now() > checker:
                    checker += datetime.timedelta(seconds=self._looptime_)
                    # wait for 14h
                    if datetime.datetime.now().hour == self._daily_:
                        checker += datetime.timedelta(hours=24,seconds=-self._looptime_)
                        try:
                            self.logger.debug("loop service: " + self._svc_name_)
                            self.loop()
                        except Exception as e:
                            self.logger.error("Exception executing run: " + str(e))
            time.sleep(1)
        else:
            checker = datetime.datetime.now()
            time.sleep(1)
            # checks if next loop should start or not every second
            while self.isrunning:
                if datetime.datetime.now() > checker:
                    try:
                        self.logger.debug("-----------started loop--" + str(checker) + "-----------")
                        self.loop()
                        self.logger.debug("-----------ended loop--" + str(checker) + "-----------")
                    except Exception as e:
                        self.logger.error("Exception executing run: " + str(e))
                    checker += datetime.timedelta(seconds=self._looptime_)
                time.sleep(1)
            
    def loop(self):
        '''
        Loop to be overridden to add loop logic
        '''
        raise NotImplementedError
        
# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    SMWinservice.parse_command_line()