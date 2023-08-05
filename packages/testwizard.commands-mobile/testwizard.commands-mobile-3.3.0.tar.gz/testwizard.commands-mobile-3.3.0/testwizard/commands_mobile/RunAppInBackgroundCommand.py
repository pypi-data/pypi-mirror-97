import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class RunAppInBackgroundCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.RunAppInBackground")

    def execute(self, seconds):
        if seconds is None:
            requestObj = []
        else:
            requestObj = [seconds]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "RunAppInBackground was successful", "RunAppInBackground failed")
