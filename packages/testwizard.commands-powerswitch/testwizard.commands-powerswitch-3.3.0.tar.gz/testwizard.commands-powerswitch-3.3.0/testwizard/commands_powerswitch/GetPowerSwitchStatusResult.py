import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class GetPowerSwitchStatusResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["status"] >= 0, successMessage, failMessage)

        self.status = result["status"]
