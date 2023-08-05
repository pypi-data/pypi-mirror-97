import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class TouchAction_NewCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(
            self, testObject, "Mobile.TouchAction_NewTouchAction")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "TouchAction_New was successful", "TouchAction_New failed")
