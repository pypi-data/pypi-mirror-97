import sys
import json

from testwizard.commands_core import CommandBase
from .FindPatternResult import FindPatternResult

class FindPatternExCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FindPatternEx")

    def execute(self, filename, mode, x, y, width, height):
        if filename is None:
            raise Exception("filename is required")
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

        requestObj = [filename, mode, x, y, width, height]

        result = self.executeCommand(requestObj, "Could not execute command")

        return FindPatternResult(result, "FindPatternEx was successful", "FindPatternEx failed")