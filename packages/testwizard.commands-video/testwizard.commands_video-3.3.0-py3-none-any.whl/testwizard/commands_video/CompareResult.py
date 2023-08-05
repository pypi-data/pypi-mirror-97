import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class CompareResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["errorCode"] == 0 and result["similarity"] != -1, successMessage, failMessage)

        self.similarity = result["similarity"]

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
