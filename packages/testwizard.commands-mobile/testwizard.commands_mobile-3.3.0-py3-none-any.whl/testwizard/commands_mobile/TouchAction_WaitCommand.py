import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class TouchAction_WaitCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.TouchAction_Wait")

    def execute(self, duration):
        if duration is None:
            raise Exception("duration is required")

        requestObj = [duration]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "TouchAction_Wait was successful", "TouchAction_Wait failed")
