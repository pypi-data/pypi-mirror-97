import sys
import json

from testwizard.commands_core import CommandBase
from .SendRCKeyResult import SendRCKeyResult


class SendRCKeyCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "SendRCKey")

    def execute(self, keyName):
        if keyName is None:
            raise Exception("keyName is required")

        requestObj = [keyName]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SendRCKeyResult(result, "SendRCKey was successful", "SendRCKey failed")
