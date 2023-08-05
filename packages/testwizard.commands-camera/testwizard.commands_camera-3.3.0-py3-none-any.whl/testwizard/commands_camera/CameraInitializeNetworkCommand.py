import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core import OkErrorCodeAndMessageResult


class CameraInitializeNetworkCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Camera.InitializeNetwork")

    def execute(self):

        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "Camera.InitializeNetwork was successful", "Camera.InitializeNetwork failed")
