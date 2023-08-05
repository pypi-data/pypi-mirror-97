import sys
import json

from testwizard.commands_core import CommandBase
from .SaveFileResult import SaveFileResult

class StartRecordingCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "StartRecording")
    
    def execute(self, filename):
        if filename is None:
            raise Exception("filename is required")

        requestObj = [filename]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SaveFileResult(result, "StartRecording was successful", "StartRecording failed")