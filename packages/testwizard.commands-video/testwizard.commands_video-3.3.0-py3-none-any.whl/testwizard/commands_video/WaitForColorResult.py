import json
import sys

from testwizard.commands_core.ResultBase import ResultBase

class WaitForColorResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["time"] >= 0 and result["errorCode"] == 0, successMessage, failMessage)

        self.time = result["time"]
        self.similarity = result["similarity"]
        self.color = Color(result["color"])

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])

class Color(object):
    def __init__(self, color):
       self.__r = int(color["r"])
       self.__g = int(color["g"])
       self.__b = int(color["b"])

    @property
    def r(self):
        return self.__r

    @property
    def g(self):
        return self.__g

    @property
    def b(self):
        return self.__b
