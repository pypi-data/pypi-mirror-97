import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class CountLastPatternMatchesResult(ResultBase):
    def __init__(self, result, successMessage, errorMessage):
        ResultBase.__init__(
            self, result["matches"] != -1 and result["errorCode"] == 0, successMessage, errorMessage)

        self.matches = result["matches"]

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
