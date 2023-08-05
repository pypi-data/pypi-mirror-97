import sys
import json

from testwizard.commands_core import CommandBase
from .GetVideoResolutionResult import GetVideoResolutionResult


class GetVideoResolutionCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "GetVideoResolution")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetVideoResolutionResult(result, "GetVideoResolution was successful", "GetVideoResolution failed")
