import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class AddCapabilityCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.AddCapability")

    def execute(self, name, value):
        if name is None:
            raise Exception("name is required")
        if value is None:
            raise Exception("value is required")

        requestObj = [name, value]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "AddCapability was successful", "AddCapability failed")
