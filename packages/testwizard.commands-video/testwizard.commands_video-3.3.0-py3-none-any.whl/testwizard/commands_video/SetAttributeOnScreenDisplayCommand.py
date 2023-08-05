import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkResult import OkResult


class SetAttributeOnScreenDisplayCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "SetAttributeOnScreenDisplay")

    def execute(self, attributeType, osdArea,  textColor, backgroundColor, duration):
        if attributeType is None:
            raise Exception("attributeType is required")

        requestObj = [attributeType]
        if osdArea is not None:
            requestObj = [attributeType, osdArea]
            if textColor is not None:
                requestObj = [attributeType, osdArea, textColor]
                if backgroundColor is not None:
                    requestObj = [attributeType, osdArea, textColor, backgroundColor]
                    if duration is not None:
                        requestObj = [attributeType, osdArea, textColor, backgroundColor, duration]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkResult(result, "SetAttributeOnScreenDisplay was successful", "SetAttributeOnScreenDisplay failed")
