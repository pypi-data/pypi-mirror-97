import sys
import json

from testwizard.commands_core import CommandBase
from .DetectMotionResult import DetectMotionResult

class DetectMotionCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "DetectMotion")
    
    def execute(self, x, y, width, height, minDifference, timeout, motionDuration, tolerance, distanceMethod, minDistance):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")
        if minDifference is None:
            raise Exception("minDifference is required")
        if timeout is None:
            raise Exception("timeout is required")

        requestObj = [x, y, width, height, minDifference, timeout]
        if motionDuration is not None:
            requestObj = [x, y, width, height, minDifference, timeout, motionDuration]
            if tolerance is not None:
                requestObj = [x, y, width, height, minDifference, timeout, motionDuration, tolerance]
                if distanceMethod is not None:
                    requestObj = [x, y, width, height, minDifference, timeout, motionDuration, tolerance, distanceMethod]
                    if minDistance is not None:
                        requestObj = [x, y, width, height, minDifference, timeout, motionDuration, tolerance, distanceMethod, minDistance]

        result = self.executeCommand(requestObj, "Could not execute command")

        return DetectMotionResult(result, "DetectMotion was successful", "DetectMotion failed")