import sys
import json

from testwizard.commands_core import CommandBase
from .FindAllPatternLocationsResult import FindAllPatternLocationsResult

class FindAllPatternLocationsExCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FindAllPatternLocationsEx")

    def execute(self, filename, mode, similarity, x, y, width, height):
        if filename is None:
            raise Exception("filename is required")
        if mode is None:
            raise Exception("mode is required")
        if similarity is None:
            raise Exception("similarity is required")
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")

        requestObj = [filename, mode, similarity, x, y, width, height]

        result = self.executeCommand(requestObj, "Could not execute command")

        return FindAllPatternLocationsResult(result, "FindAllPatternLocationsEx was successful", "FindAllPatternLocationsEx failed")