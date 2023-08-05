import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class DetectMotionResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(
            self, result["time"] >= 0 and result["errorCode"] == 0, successMessage, failMessage)

        self.time = result["time"]
        self.difference = result["difference"]
        self.distance = result["distance"]

        if self.success is True:
            return

        if result["errorCode"] == 14:
            self.message = self.message + ": motionDuration is bigger than Timeout"
        else:
            self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
