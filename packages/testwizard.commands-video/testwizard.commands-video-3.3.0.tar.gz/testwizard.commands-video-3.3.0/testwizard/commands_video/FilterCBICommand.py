import sys
import json

from testwizard.commands_core import CommandBase
from .FilterResult import FilterResult


class FilterCBICommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FilterCBI")

    def execute(self, contrast, brightness, intensity):
        if contrast is None:
            raise Exception("contrast is required")
        if brightness is None:
            raise Exception("brightness is required")
        if intensity is None:
            raise Exception("intensity is required")

        requestObj = [contrast, brightness, intensity]

        result = self.executeCommand(requestObj, "Could not execute command")

        return FilterResult(result, "FilterCBI was successful", "FilterCBI failed")
