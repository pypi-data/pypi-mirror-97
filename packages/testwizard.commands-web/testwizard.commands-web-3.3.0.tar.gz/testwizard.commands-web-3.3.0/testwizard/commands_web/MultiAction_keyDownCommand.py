import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class MultiAction_keyDown(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_KeyDown")

    def execute(self, key, selector):
        if key is None:
            raise Exception("key is required")

        requestObj = [key]
        if selector is not None:
            requestObj = [selector, key]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "MultiAction_keyDown was successful", "MultiAction_keyDown failed")
