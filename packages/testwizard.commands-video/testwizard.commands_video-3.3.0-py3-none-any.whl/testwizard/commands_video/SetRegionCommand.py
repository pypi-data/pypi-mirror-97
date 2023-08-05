import sys
import json

from testwizard.commands_core import CommandBase
from .FilterResult import FilterResult


class SetRegionCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "SetRegion")

    def execute(self, x, y, width, height):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")

        requestObj = [x, y, width, height]

        result = self.executeCommand(requestObj, "Could not execute command")

        return FilterResult(result, "SetRegion was successful", "SetRegion failed")
