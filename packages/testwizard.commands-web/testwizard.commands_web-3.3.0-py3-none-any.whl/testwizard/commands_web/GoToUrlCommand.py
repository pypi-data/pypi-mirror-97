import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class GoToUrl(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.GoToUrl")

    def execute(self, url):
        if url is None:
            raise Exception("url is required")

        requestObj = [url]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "GoToUrl was successful", "GoToUrl failed")
