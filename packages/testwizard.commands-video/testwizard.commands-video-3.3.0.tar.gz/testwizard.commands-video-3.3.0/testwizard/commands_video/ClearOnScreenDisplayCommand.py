import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkResult import OkResult


class ClearOnScreenDisplayCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "ClearOnScreenDisplay")

    def execute(self, osdArea):
        if osdArea is not None:
            requestObj = [osdArea]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkResult(result, "ClearOnScreenDisplay was successful", "ClearOnScreenDisplay failed")
