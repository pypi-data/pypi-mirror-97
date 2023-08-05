import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class TouchAction_PressCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.TouchAction_Press")

    def execute(self, x, y):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")

        requestObj = [x, y]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "TouchAction_Press was successful", "TouchAction_Press failed")
