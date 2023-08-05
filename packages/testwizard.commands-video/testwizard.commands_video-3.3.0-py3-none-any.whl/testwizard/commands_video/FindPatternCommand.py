import sys
import json

from testwizard.commands_core import CommandBase
from .FindPatternResult import FindPatternResult

class FindPatternCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FindPattern")
    
    def execute(self, filename, mode):
        if filename is None:
            raise Exception("filename is required")
        if mode is None:
            raise Exception("mode is required")

        requestObj = [filename, mode]

        result = self.executeCommand(requestObj, "Could not execute command")        

        return FindPatternResult(result, "FindPattern was successful", "FindPattern failed")   