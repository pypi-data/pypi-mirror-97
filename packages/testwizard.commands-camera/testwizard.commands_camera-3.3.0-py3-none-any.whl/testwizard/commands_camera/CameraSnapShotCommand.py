import sys
import json

from testwizard.commands_core import CommandBase
from .CameraSnapShotResult import CameraSnapShotresult


class CameraSnapShotCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Camera.SnapShot")

    def execute(self, filename):
        if filename is None:
            raise Exception("filename is required")

        requestObj = [filename]

        result = self.executeCommand(requestObj, "Could not execute command")

        return CameraSnapShotresult(result, "Camera.SnapShot was successful", "Camera.SnapShot failed")
