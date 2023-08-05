import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class AddArgument(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.AddArgument")

    def execute(self, argument):
        if argument is None:
            raise Exception("argument is required")

        requestObj = [argument]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "AddArgument was successful", "AddArgument failed")
