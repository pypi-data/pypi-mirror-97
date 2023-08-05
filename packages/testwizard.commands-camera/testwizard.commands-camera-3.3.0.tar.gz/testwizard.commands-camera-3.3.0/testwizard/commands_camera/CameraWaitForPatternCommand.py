import sys
import json

from testwizard.commands_core import CommandBase
from .CameraWaitForSampleResult import CameraWaitForSampleResult


class CameraWaitForPatternCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Camera.WaitForPattern")

    def execute(self, filePath, x, y, width, height, timeout, distanceThreshold):
        if filePath is None:
            raise Exception("filename is required")
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
            requestObj = [filePath, x, y, width, height, timeout]
        else:
            requestObj = [filePath, x, y, width, height, timeout, distanceThreshold]

        result = self.executeCommand(requestObj, "Could not execute command")

        return CameraWaitForSampleResult(result, "WaitForPattern was successful", "WaitForPattern failed")
