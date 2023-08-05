import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class MultiAction_DragAndDropToOffset(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_DragAndDropToOffset")

    def execute(self, sourceSelector, targetXOffset, targetYOffset):
        if sourceSelector is None:
            raise Exception("sourceSelector is required")
        if targetXOffset is None:
            raise Exception("targetXOffset is required")
        if targetYOffset is None:
            raise Exception("targetYOffset is required")

        requestObj = [sourceSelector, targetXOffset, targetYOffset]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "MultiAction_DragAndDropToOffset was successful", "MultiAction_DragAndDropToOffset failed")
