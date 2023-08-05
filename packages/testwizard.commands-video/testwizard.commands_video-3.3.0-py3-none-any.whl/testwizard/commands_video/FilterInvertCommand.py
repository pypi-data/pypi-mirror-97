import sys
import json

from testwizard.commands_core import CommandBase
from .FilterResult import FilterResult


class FilterInvertCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FilterInvert")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return FilterResult(result, "FilterInvert was successful", "FilterInvert failed")
