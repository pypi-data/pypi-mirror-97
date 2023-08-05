import sys
import json

from testwizard.commands_core import CommandBase
from .GetOrientationResult import GetOrientationResult


class GetOrientationCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.GetOrientation")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetOrientationResult(result, "GetOrientation was successful", "GetOrientation failed")
