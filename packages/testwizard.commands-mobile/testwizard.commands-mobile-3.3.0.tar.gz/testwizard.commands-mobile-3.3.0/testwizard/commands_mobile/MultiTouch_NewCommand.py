import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class MultiTouch_NewCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(
            self, testObject, "Mobile.MultiTouch_NewMultiTouch")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "MultiTouch_New was successful", "MultiTouch_New failed")
