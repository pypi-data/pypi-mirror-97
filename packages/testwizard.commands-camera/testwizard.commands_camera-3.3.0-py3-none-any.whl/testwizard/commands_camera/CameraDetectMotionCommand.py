import sys
import json

from testwizard.commands_core import CommandBase
from .CameraDetectMotionResult import CameraDetectMotionResult


class CameraDetectMotionCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Camera.DetectMotion")
    
    def execute(self, x, y, width, height, duration, distanceThreshold):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")
        if duration is None:
            raise Exception("duration is required")

        if distanceThreshold is None:
            requestObj = [x, y, width, height, duration]
        else:
            requestObj = [x, y, width, height, duration, distanceThreshold]

        result = self.executeCommand(requestObj, "Could not execute command")

        return CameraDetectMotionResult(result, "CameraDetectMotion was successful", "CameraDetectMotion failed")