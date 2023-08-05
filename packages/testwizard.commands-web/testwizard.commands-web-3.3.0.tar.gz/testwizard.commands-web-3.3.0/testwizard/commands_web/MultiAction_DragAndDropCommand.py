import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class MultiAction_DragAndDrop(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_DragAndDrop")

    def execute(self, sourceSelector, targetSelector):
        if sourceSelector is None:
            raise Exception("sourceSelector is required")
        if targetSelector is None:
            raise Exception("targetSelector is required")

        requestObj = [sourceSelector, targetSelector]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "MultiAction_DragAndDrop was successful", "MultiAction_DragAndDrop failed")
