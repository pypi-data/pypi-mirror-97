import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class AddChromeExtension(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.AddChromeExtension")

    def execute(self, filepath):
        if filepath is None:
            raise Exception("filepath is required")

        requestObj = [filepath]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SimpleResult(result, "AddChromeExtension was successful", "AddChromeExtension failed")
