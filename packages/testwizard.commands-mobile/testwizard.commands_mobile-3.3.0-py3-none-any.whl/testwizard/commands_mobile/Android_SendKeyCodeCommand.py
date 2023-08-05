import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class Android_SendKeyCodeCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.Android_SendKeyCode")

    def execute(self, keyCode):
        if keyCode is None:
            raise Exception("keyCode is required")

        requestObj = [keyCode]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "Android_SendKeyCode was successful", "Android_SendKeyCode failed")
