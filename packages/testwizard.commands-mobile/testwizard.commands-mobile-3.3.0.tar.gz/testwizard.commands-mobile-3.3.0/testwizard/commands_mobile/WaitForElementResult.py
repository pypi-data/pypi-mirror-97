import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class WaitForElementResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(
            self, result["elementFound"], successMessage, failMessage + ": " + result["errorMessage"])

        self.time = result["time"]
