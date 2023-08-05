import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForAudioResult import WaitForAudioResult


class WaitForPeakAudioCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "WaitForPeakAudio")

    def execute(self, level, timeout):
        if level is None:
            raise Exception("level is required")
        if timeout is None:
            raise Exception("timeout is required")

        requestObj = [level, timeout]

        result = self.executeCommand(requestObj, "Could not execute command")

        return WaitForAudioResult(result, "WaitForPeakAudio was successful", "WaitForPeakAudio failed")
