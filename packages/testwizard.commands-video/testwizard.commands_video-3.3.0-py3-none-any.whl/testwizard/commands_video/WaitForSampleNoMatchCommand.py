import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForSampleResult import WaitForSampleResult


class WaitForSampleNoMatchCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "WaitForSampleNoMatch")

    def execute(self, x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod, maxDistance):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")
        if minSimilarity is None:
            raise Exception("minSimilarity is required")
        if timeout is None:
            raise Exception("timeout is required")
        if tolerance is None:
            raise Exception("tolerance is required")

        requestObj = [x, y, width, height, minSimilarity, timeout, tolerance]
        if distanceMethod is not None:
            requestObj = [x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod]
            if maxDistance is not None:
                requestObj = [x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod, maxDistance]

        result = self.executeCommand(requestObj, "Could not execute command")

        return WaitForSampleResult(result, "WaitForSampleNoMatch was successful", "WaitForSampleNoMatch failed")
