import sys
import json

from testwizard.commands_core import CommandBase
from .GetElementAttributeResult import GetElementAttributeResult


class GetElementAttributeCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.GetElementAttribute")

    def execute(self, selector, attribute):
        if selector is None:
            raise Exception("selector is required")
        if attribute is None:
            raise Exception("attribute is required")

        requestObj = [selector, attribute]

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetElementAttributeResult(result, "GetElementAttribute was successful", "GetElementAttribute failed")
