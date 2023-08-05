import json
import sys

from testwizard.commands_core.ResultBase import ResultBase

class GetSizeResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["ok"] is True, successMessage, failMessage + ": " + result["errorMessage"])

        self.width = result["width"]
        self.height = result["height"]