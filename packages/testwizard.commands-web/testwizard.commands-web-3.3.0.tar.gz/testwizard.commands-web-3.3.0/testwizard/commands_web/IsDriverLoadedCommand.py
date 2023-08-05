import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class IsDriverLoaded(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.IsDriverLoaded")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "IsDriverLoaded was successful", "IsDriverLoaded failed")
