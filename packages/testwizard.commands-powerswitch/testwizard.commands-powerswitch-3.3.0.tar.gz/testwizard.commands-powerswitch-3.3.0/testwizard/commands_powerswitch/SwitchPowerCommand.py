import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class SwitchPowerCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "SwitchPower")

    def execute(self, on):
        if on is None:
            raise Exception("on is required")

        requestObj = [on]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "SwitchPower was successful", "SwitchPower failed")
