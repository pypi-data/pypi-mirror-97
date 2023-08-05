import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class AcceptAlert(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.AcceptAlert")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "acceptAlert was successful", "acceptAlert failed")
