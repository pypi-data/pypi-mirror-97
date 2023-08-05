import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class QuitDriver(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.QuitDriver")

    def execute(self):
        requestObj = []

        result = self.executeCommand(requestObj, "Could not execute command")

        return OkErrorCodeAndMessageResult(result, "QuitDriver was successful", "QuitDriver failed")
