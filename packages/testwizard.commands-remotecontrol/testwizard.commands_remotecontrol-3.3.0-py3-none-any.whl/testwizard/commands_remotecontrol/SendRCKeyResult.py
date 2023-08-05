import json
import sys

from testwizard.commands_core.ResultBase import ResultBase


class SendRCKeyResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["sent"] is True, successMessage, failMessage)

        if self.success is True:
            return

        self.message = self.getMessageForErrorCode(self.message, result["errorCode"])
