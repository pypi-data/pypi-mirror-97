import sys
import json

from testwizard.commands_core import CommandBase
from .ScreenshotResult import ScreenshotResult


class ScreenShotJPGCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.ScreenshotJPG")

    def execute(self, filename, quality):
        if filename is None:
            raise Exception("filename is required")
        if quality is None:
            raise Exception("quality is required")

        requestObj = [filename, quality]

        result = self.executeCommand(requestObj, "Could not execute command")

        return ScreenshotResult(result, "ScreenshotJPG was successful", "ScreenshotJPG failed")
