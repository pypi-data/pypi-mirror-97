import sys
import json

from testwizard.commands_core import CommandBase
from .FilterResult import FilterResult


class FilterBlackWhiteCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FilterBlackWhite")

    def execute(self, separation):
        if separation is None:
            raise Exception("separation is required")

        requestObj = [separation]

        result = self.executeCommand(requestObj, "Could not execute command")

        return FilterResult(result, "FilterBlackWhite was successful", "FilterBlackWhite failed")
