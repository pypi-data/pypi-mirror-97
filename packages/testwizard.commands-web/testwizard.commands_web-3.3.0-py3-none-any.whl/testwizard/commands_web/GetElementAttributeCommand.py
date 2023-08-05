import sys
import json

from testwizard.commands_core import CommandBase
from .GetElementAttributeResult import GetElementAttributeResult


class GetElementAttribute(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.GetElementAttribute")

    def execute(self, selector, name):
        if selector is None:
            raise Exception("selector is required")
        if name is None:
            raise Exception("name is required")

        requestObj = [selector, name]

        result = self.executeCommand(requestObj, "Could not execute command")

        return GetElementAttributeResult(result, "GetElementAttribute was successful", "GetElementAttribute failed")
