
import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class HideKeyboardCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.HideKeyboard")

    def execute(self, iOS_Key):
        if iOS_Key is None:
            requestObj = []
        else:
            requestObj = [iOS_Key]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "HideKeyboard was successful", "HideKeyboard failed")
