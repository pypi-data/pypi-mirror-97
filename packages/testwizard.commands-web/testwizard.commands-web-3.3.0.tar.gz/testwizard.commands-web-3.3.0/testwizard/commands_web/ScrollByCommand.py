import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class ScrollBy(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.ScrollBy")

    def execute(self, x, y):
        if x is None:
            raise Exception("x is required")
        if y is None:
            raise Exception("y is required")

        requestObj = [x, y]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "ScrollBy was successful", "ScrollBy failed")
