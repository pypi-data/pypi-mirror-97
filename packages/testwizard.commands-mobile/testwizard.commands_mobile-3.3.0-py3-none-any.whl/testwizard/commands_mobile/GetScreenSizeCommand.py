import sys
import json

from testwizard.commands_core import CommandBase
from .GetSizeResult import GetSizeResult


class GetScreenSizeCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.GetScreenSize")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetSizeResult(result, "GetScreenSize was successful", "GetScreenSize failed")
