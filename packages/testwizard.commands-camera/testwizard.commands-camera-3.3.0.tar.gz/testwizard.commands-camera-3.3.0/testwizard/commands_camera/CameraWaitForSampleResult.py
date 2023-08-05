import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class CameraWaitForSampleResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(
            self, result["time"] >= 0 and result["errorCode"] == 0, successMessage, failMessage)

        self.time = result["time"]
        self.distance = result["distance"]
        self.hasMatch = result["hasMatch"]
        self.hasTimeout = result["hasTimeout"]
        self.message = result["message"]
