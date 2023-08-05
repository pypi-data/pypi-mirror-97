import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class SetOrientationCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.SetOrientation")

    def execute(self, orientation):
        if orientation is None:
            raise Exception("orientation is required")

        requestObj = [orientation]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "SetOrientation was successful", "SetOrientation failed")
