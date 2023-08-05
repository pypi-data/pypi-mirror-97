import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult

class FindElementCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.FindElement")

    def execute(self, selector):
        if selector is None:
            raise Exception("selector is required")

        requestObj = [selector]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "FindElement was successful", "FindElement failed")