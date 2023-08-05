import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class MultiAction_MoveToElementOffset(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_MoveToElementOffset")

    def execute(self, selector, xOffset, yOffset):
        if selector is None:
            raise Exception("selector is required")
        if xOffset is None:
            raise Exception("xOffset is required")
        if yOffset is None:
            raise Exception("yOffset is required")

        requestObj = [selector, xOffset, yOffset]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "MultiAction_MoveToElementOffset was successful", "MultiAction_MoveToElementOffset failed")
