import sys
import json

from testwizard.commands_core import CommandBase
from .CameraWaitForSampleResult import CameraWaitForSampleResult


class CameraWaitForSampleNoMatchCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Camera.WaitForSampleNoMatch")

    def execute(self, x, y, width, height, timeout, distanceThreshold):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")
        if width is None:
            raise Exception("width is required")
        if height is None:
            raise Exception("height is required")
        if timeout is None:
            raise Exception("timeout is required")

        if distanceThreshold is None:
            requestObj = [x, y, width, height, timeout]
        else:
            requestObj = [x, y, width, height, timeout, distanceThreshold]

        result = self.executeCommand(requestObj, "Could not execute command")

        return CameraWaitForSampleResult(result, "WaitForSampleNoMatch was successful", "WaitForSampleNoMatch failed")
