import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class CameraDetectMotionResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(
            self, result["time"] >= 0 and result["errorCode"] == 0, successMessage, failMessage)

        self.time = result["time"]
        self.hasMotion = result["hasMotion"]
        self.motionRatio = result["motionRatio"]
        self.framesProcessed = result["framesProcessed"]
        self.message = result["message"]