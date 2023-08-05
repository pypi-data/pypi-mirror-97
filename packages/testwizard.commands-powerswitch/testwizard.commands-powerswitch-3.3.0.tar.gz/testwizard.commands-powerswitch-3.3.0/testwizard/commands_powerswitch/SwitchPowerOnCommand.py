import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class SwitchPowerOnCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "SwitchPowerOn")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "SwitchPowerOn was successful", "SwitchPowerOn failed")
