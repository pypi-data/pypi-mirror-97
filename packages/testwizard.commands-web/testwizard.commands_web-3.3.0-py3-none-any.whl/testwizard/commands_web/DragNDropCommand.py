import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class DragNDrop(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.DragNDrop")

    def execute(self, sourceSelector, targetSelector):
        if sourceSelector is None:
            raise Exception("sourceSelector is required")
        if targetSelector is None:
            raise Exception("targetSelector is required")

        requestObj = [sourceSelector, targetSelector]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "DragNDrop was successful", "DragNDrop failed")
