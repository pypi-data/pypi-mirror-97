import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForElementResult import WaitForElementResult

class WaitForElementCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.WaitForElement")

    def execute(self, selector, maxSeconds):
        if selector is None:
            raise Exception("selector is required")
        if maxSeconds is None:
            raise Exception("maxSeconds is required")

        requestObj = [selector, maxSeconds]

        result = self.executeCommand(requestObj, "Could not execute command")

        return WaitForElementResult(result, "WaitForElement was successful", "WaitForElement failed")