import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkResult import OkResult


class SetTextOnScreenDisplayCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "SetTextOnScreenDisplay")

    def execute(self, osdText, osdArea,  textColor, backgroundColor, duration):
        if osdText is None:
            raise Exception("osdText is required")

        requestObj = [osdText]
        if osdArea is not None:
            requestObj = [osdText, osdArea]
            if textColor is not None:
                requestObj = [osdText, osdArea, textColor]
                if backgroundColor is not None:
                    requestObj = [osdText, osdArea, textColor, backgroundColor]
                    if duration is not None:
                        requestObj = [osdText, osdArea, textColor, backgroundColor, duration]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkResult(result, "SetTextOnScreenDisplay was successful", "SetTextOnScreenDisplay failed")
