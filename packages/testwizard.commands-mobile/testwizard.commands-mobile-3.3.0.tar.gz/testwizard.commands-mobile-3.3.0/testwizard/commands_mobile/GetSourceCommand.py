import sys
import json

from testwizard.commands_core import CommandBase
from .GetSourceResult import GetSourceResult

class GetSourceCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.GetSource")
    
    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetSourceResult(result, "GetSource was successful", "GetSource failed")   