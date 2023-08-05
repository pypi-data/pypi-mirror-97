import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class SwipeCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.Swipe")

    def execute(self, startX, startY, endX, endY, duration):
        if startX is None:
            raise Exception("startX is required")
        if startY is None:
            raise Exception("startY is required")
        if endX is None:
            raise Exception("endX is required")
        if endY is None:
            raise Exception("endY is required")
        if duration is None:
            raise Exception("duration is required")

        requestObj = [startX, startY, endX, endY, duration]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "Swipe was successful", "Swipe failed")
