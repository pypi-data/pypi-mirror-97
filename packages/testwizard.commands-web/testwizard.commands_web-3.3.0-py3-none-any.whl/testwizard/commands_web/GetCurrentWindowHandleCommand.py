import sys
import json

from testwizard.commands_core import CommandBase
from .GetCurrentWindowHandleResult import GetCurrentWindowHandleResult


class GetCurrentWindowHandle(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(
            self, testObject, "Selenium.GetCurrentWindowHandle")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetCurrentWindowHandleResult(result, "GetCurrentWindowHandle was successful", "GetCurrentWindowHandle failed")
