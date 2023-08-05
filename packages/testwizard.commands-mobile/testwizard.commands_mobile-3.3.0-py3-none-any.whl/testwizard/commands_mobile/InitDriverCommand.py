import sys

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult

import json
class InitDriverCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.InitDriver")
    
    def execute(self, appPath):
        if appPath is None:
            requestObj = []
        else:
            requestObj = [appPath]

        result = self.executeCommand(requestObj, "Could not execute command")
        
        return SimpleResult(result, "InitDriver was successful", "InitDriver failed")   