import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class AuthenticateUrl(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.AuthenticateUrl")

    def execute(self, username, password, link):
        if username is None:
            raise Exception("username is required")
        if password is None:
            raise Exception("password is required")
        if link is None:
            raise Exception("link is required")

        requestObj = [username, password, link]

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "AuthenticateUrl was successful", "AuthenticateUrl failed")
