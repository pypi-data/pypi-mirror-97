import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class GetElementResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["ok"] is True, successMessage, failMessage)

        self.text = result["text"]
        self.enabled = result["enabled"]
        self.displayed = result["displayed"]
        self.selected = result["selected"]
        self.location = result["location"]
        self.size = result["size"]

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
