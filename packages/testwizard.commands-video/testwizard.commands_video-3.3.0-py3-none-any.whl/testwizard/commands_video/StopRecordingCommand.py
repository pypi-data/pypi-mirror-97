import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkResult import OkResult


class StopRecordingCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "StopRecording")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkResult(result, "StopRecording was successful", "StopRecording failed")
