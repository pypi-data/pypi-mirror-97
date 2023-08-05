import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult

class StartBackgroundCaptureCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "StartBGCapture")
    
    def execute(self, stepSize, captures):
        if stepSize is None:
            raise Exception("stepSize is required")
        if captures is None:
            raise Exception("captures is required")

        requestObj = [stepSize, captures]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "StartBackgroundCapture was successful", "StartBackgroundCapture failed")