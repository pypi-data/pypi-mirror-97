import json
import sys

from testwizard.commands_core.ResultBase import ResultBase

class WaitForAudioResult(ResultBase):
    def __init__(self, result , successMessage, failMessage):
        self.rightLevel = result["rightLevel"]
        self.leftLevel = result["leftLevel"]
        self.time = result["time"]

        ResultBase.__init__(self, self.time >= 0, successMessage, failMessage)
