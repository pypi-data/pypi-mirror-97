import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class QuitDriverCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.QuitDriver")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "QuitDriver was successful", "QuitDriver failed")
