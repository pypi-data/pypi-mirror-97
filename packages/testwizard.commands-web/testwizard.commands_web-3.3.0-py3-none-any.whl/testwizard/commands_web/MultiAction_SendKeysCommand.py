import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class MultiAction_SendKeys(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_Sendkeys")

    def execute(self, inputString, selector):
        if inputString is None:
            raise Exception("inputString is required")

        requestObj = [inputString]
        if selector is not None:
            requestObj = [selector, inputString]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "MultiAction_SendKeys was successful", "MultiAction_SendKeys failed")
