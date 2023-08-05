import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class FilterResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["ok"] is True, successMessage, failMessage)

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
