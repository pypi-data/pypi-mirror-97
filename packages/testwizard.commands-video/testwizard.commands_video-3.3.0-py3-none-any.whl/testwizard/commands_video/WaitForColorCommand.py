import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForColorResult import WaitForColorResult


class WaitForColorCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "WaitForColor")

    def execute(self, x, y, width, height, refColor, tolerance, minSimilarity, timeout):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")
        if refColor is None:
            raise Exception("refColor is required")
        if tolerance is None:
            raise Exception("tolerance is required")
        if minSimilarity is None:
            raise Exception("minSimilarity is required")
        if timeout is None:
            raise Exception("timeout is required")

        requestObj = [x, y, width, height, refColor,
                      tolerance, minSimilarity, timeout]

        result = self.executeCommand(requestObj, "Could not execute command")

        return WaitForColorResult(result, "WaitForColor was successful", "WaitForColor failed")
