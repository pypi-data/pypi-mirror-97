import sys
import json

from testwizard.commands_core import CommandBase
from .TextOCRResult import TextOCRResult


class TextOCRCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "TextOCR")

    def execute(self, dictionary):
        if dictionary is None:
            raise Exception("dictionary is required")

        requestObj = [dictionary]

        result = self.executeCommand(requestObj, "Could not execute command")

        return TextOCRResult(result, "TextOCR was successful", "TextOCR failed")
