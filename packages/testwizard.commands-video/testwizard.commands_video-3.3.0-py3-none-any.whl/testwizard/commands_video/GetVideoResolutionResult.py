import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class GetVideoResolutionResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        self.width = result["width"]
        self.height = result["height"]

        ResultBase.__init__(self, self.width != -1 and self.height != -1, successMessage, failMessage)
