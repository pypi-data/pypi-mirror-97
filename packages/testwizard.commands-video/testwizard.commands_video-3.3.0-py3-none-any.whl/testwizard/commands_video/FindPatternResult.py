import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class FindPatternResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        self.similarity = result["similarity"]
        self.position = result["position"]

        ResultBase.__init__(self, self.similarity != -1 and result["errorCode"] == 0, successMessage, failMessage)

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
