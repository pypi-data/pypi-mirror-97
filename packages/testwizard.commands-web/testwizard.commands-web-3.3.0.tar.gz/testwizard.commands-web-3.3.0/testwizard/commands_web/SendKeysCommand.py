import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class SendKeys(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.SendKeys")

    def execute(self, selector, text):
        if selector is None:
            raise Exception("selector is required")
        if text is None:
            raise Exception("text is required")

        requestObj = [selector, text]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "SendKeys was successful", "SendKeys failed")
