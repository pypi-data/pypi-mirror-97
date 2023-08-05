import sys
import json

from testwizard.commands_core import CommandBase
from .CompareResult import CompareResult


class CompareCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Compare")

    def execute(self, x, y, width, height, filename, tolerance):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")
        if filename is None:
            raise Exception("filename is required")
        if tolerance is None:
            raise Exception("tolerance is required")

        requestObj = [x, y, width, height, filename, tolerance]

        result = self.executeCommand(requestObj, "Could not execute command")

        return CompareResult(result, "compare was successful", "compare failed")
