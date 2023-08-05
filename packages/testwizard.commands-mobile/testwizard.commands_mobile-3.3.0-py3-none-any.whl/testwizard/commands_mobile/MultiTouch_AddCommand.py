import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class MultiTouch_AddCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(
            self, testObject, "Mobile.MultiTouch_AddToMultiTouch")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "MultiTouch_Add was successful", "MultiTouch_Add failed")
