import sys
import json

from testwizard.commands_core import CommandBase
from .ScreenshotResult import ScreenshotResult


class ScreenshotBMPCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.ScreenshotBMP")

    def execute(self, filename):
        if filename is None:
            raise Exception("filename is required")

        requestObj = [filename]

        result = self.executeCommand(requestObj, "Could not execute command")

        return ScreenshotResult(result, "ScreenshotBMP was successful", "ScreenshotBMP failed")
