import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class GetOrientationResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["ok"] is True, successMessage, failMessage + ": " + result["errorMessage"])

        self.orientation = result["orientation"]