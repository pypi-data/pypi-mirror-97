import json
import sys

from .ResultBase import ResultBase

class OkErrorCodeAndMessageResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        ResultBase.__init__(self, result["ok"] is True, successMessage, failMessage)

        if self.success is True:
            return

        if "message" in result:
            self.message = result["message"]

        if "errorCode" in result:
            self.message = self.getMessageForErrorCode(self.message, result["errorCode"])