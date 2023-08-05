import sys
import json

from testwizard.commands_core import CommandBase
from .GetChildrenResult import GetChildrenResult


class GetChildren(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.GetChildren")

    def execute(self, selector):
        if selector is None:
            raise Exception("selector is required")

        requestObj = [selector]

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetChildrenResult(result, "GetChildren was successful", "GetChildren failed")
