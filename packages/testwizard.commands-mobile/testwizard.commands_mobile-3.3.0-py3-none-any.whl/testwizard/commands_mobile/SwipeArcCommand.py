import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class SwipeArcCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.SwipeArc")

    def execute(self, centerX, centerY, radius, startDegree, degrees, steps):
        if centerX is None:
            raise Exception("centerX is required")
        if centerY is None:
            raise Exception("centerY is required")
        if radius is None:
            raise Exception("radius is required")
        if startDegree is None:
            raise Exception("startDegree is required")
        if degrees is None:
            raise Exception("degrees is required")
        if steps is None:
            raise Exception("steps is required")

        requestObj = [centerX, centerY, radius, startDegree, degrees, steps]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "SwipeArc was successful", "SwipeArc failed")
