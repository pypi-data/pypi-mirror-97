import sys
import json

from testwizard.commands_core import CommandBase
from .GetPowerSwitchStatusResult import GetPowerSwitchStatusResult

class GetPowerSwitchStatusCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "GetPowerSwitchStatus")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetPowerSwitchStatusResult(result, "GetPowerSwitchStatus was successful", "GetPowerSwitchStatus failed")