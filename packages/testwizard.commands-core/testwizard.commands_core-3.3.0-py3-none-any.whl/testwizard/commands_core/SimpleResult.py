import json
import sys

from .ResultBase import ResultBase

class SimpleResult(ResultBase):
    def __init__(self, result, successMessage, failMessage):
        if "errorMessage" in result:
            failMessage = result["errorMessage"]

        ResultBase.__init__(self, result["ok"] is True, successMessage, failMessage)