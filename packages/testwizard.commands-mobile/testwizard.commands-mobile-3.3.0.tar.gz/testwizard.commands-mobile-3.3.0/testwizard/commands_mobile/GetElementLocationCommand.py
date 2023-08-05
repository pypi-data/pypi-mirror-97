import sys
import json

from testwizard.commands_core import CommandBase
from .GetElementLocationResult import GetElementLocationResult


class GetElementLocationCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject,
                             "Mobile.GetElementLocation")

    def execute(self, selector):
        if selector is None:
            raise Exception("selector is required")

        requestObj = [selector]

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetElementLocationResult(result, "GetElementLocation was successful", "GetElementLocation failed")
