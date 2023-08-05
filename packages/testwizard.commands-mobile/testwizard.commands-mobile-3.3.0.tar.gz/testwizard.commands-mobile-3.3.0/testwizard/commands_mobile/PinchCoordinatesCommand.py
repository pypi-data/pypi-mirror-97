import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class PinchCoordinatesCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.PinchCoordinates")

    def execute(self, x, y, length):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if length is None:
            raise Exception("length is required")

        requestObj = [x, y, length]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "PinchCoordinates was successful", "PinchCoordinates failed")
