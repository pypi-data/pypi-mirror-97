
class CommandBase():
    def __init__(self, testObject, commandName):
        if testObject is None:
            raise Exception("testObject is required")
        if commandName is None:
            raise Exception("commandName is required")
        
        self.__testObject = testObject
        self.__commandName = commandName

    def executeCommand(self, requestObj, errorMessagePrefix):
        return self.__testObject.executeCommand(self.__commandName, requestObj, errorMessagePrefix)
