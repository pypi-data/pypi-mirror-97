import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class DismissAlert(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.DismissAlert")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "DismissAlert was successful", "DismissAlert failed")
