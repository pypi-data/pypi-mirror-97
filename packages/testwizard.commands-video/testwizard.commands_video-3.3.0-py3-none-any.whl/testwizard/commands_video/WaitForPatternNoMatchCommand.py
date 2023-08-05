import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForPatternResult import WaitForPatternResult


class WaitForPatternNoMatchCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "WaitForPatternNoMatch")

    def execute(self, filename, minSimilarity, timeout, mode, x, y, width, height):
        if filename is None:
            raise Exception("filename is required")
        if minSimilarity is None:
            raise Exception("minSimilarity is required")
        if timeout is None:
            raise Exception("timeout is required")
        if mode is None:
            raise Exception("mode is required")
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")

        requestObj = [filename, minSimilarity,
                      timeout, mode, x, y, width, height]

        result = self.executeCommand(requestObj, "Could not execute command")

        return WaitForPatternResult(result, "WaitForPatternNoMatch was successful", "WaitForPatternNoMatch failed")
