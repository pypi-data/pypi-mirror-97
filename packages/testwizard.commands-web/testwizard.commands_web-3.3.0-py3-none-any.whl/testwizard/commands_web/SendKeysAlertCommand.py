import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class SendKeysAlert(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.SendKeysAlert")

    def execute(self, text):
        if text is None:
            raise Exception("text is required")

        requestObj = [text]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "SendKeysAlert was successful", "SendKeysAlert failed")
