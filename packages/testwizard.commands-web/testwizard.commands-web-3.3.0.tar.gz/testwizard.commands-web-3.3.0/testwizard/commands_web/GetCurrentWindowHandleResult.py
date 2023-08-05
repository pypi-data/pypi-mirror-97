import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class GetCurrentWindowHandleResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["ok"] is True and result["errorCode"] == 0, successMessage, result["message"] or failMessage)

        self.handle = result.get("handle")

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
