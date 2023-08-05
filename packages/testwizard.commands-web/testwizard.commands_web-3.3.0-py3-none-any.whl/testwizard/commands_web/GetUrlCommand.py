import sys
import json

from testwizard.commands_core import CommandBase
from .GetUrlResult import GetUrlResult


class GetUrl(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.GetUrl")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetUrlResult(result, "GetUrl was successful", "GetUrl failed")
