import sys
import json

from testwizard.commands_core import CommandBase
from .GetWindowHandlesResult import GetWindowHandlesResult


class GetWindowHandles(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.GetWindowHandles")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetWindowHandlesResult(result, "GetWindowHandles was successful", "GetWindowHandles failed")
