import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class WaitForSampleResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(
            self, result["time"] >= 0 and result["errorCode"] == 0, successMessage, failMessage)

        self.time = result["time"]
        self.similarity = result["similarity"]
        self.distance = result["distance"]

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
