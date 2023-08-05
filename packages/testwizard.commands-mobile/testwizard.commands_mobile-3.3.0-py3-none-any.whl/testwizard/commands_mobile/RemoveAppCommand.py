import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class RemoveAppCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.RemoveApp")

    def execute(self, appId):
        if appId is None:
            raise Exception("appId is required")

        requestObj = [appId]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "RemoveApp was successful", "RemoveApp failed")
