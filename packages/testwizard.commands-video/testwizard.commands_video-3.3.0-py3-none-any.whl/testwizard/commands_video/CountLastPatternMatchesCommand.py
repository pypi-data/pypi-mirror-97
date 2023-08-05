import sys
import json

from testwizard.commands_core import CommandBase
from .CountLastPatternMatchesResult import CountLastPatternMatchesResult


class CountLastPatternMatchesCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "CountLastPatternMatches")

    def execute(self, similarity):
        if similarity is None:
            raise Exception("similarity is required")

        requestObj = [similarity]

        result = self.executeCommand(requestObj, "Could not execute command")

        return CountLastPatternMatchesResult(result, "CountLastPatternMatches was successful", "CountLastPatternMatches failed")
