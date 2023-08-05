import sys
import json

from testwizard.commands_core import CommandBase
from .FindAllPatternLocationsResult import FindAllPatternLocationsResult


class FindAllPatternLocationsCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FindAllPatternLocations")

    def execute(self, filename, mode, similarity):
        if filename is None:
            raise Exception("filename is required")
        if mode is None:
            raise Exception("mode is required")
        if similarity is None:
            raise Exception("similarity is required")

        requestObj = [filename, mode, similarity]

        result = self.executeCommand(requestObj, "Could not execute command")

        return FindAllPatternLocationsResult(result, "FindAllPatternLocations was successful", "FindAllPatternLocations failed")
