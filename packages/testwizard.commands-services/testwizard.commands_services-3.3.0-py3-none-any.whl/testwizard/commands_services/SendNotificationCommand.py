import sys
import json

from testwizard.commands_core import CommandBase
from .SendNotificationResult import SendNotificationResult


class SendNotificationCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Services.SendNotification")

    def execute(self, errorId, description, priority):
        if errorId is None:
            raise Exception("errorId is required")
        if description is None:
            raise Exception("description is required")
        if priority is None:
            raise Exception("priority is required")
        requestObj = [errorId, description, priority]

        result = self.executeCommand(requestObj, "Could not execute command")

        return SendNotificationResult(result, "SendNotification was successful", "SendNotification failed")
