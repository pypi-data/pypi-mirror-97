import sys
import json

from testwizard.commands_core import CommandBase
from .FilterResult import FilterResult


class FilterGrayscaleCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FilterGrayscale")

    def execute(self, levels):
        if levels is None:
            raise Exception("levels is required")

        requestObj = [levels]

        result = self.executeCommand(requestObj, "Could not execute command")

        return FilterResult(result, "FilterGrayscale was successful", "FilterGrayscale failed")
