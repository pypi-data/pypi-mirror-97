import time
from enum import Enum
from collections import namedtuple

from .RobotClient import RobotClient
from .ResultCodes import ResultCodes
from .models.TestResult import TestResult

class Session():
    def __init__(self, scriptFilePath, workingDirectory, metadata, testRunId):
        self.metadata = metadata

        self.parameters = {}
        for parameter in metadata.get("parameters", {}):
            self.parameters[parameter['name']] = parameter['value']

        self.customProperties = metadata.get("customProperties", {})

        self.robot = RobotClient("localhost:8500")

        if testRunId is None:
            self.testRunId = self.robot.createTestRun(scriptFilePath, workingDirectory, metadata)
            self.__isSelfManaged = True
        else:
            self.testRunId = testRunId
            self.__isSelfManaged = False

        self.info = self.robot.getSessionInfo(self.testRunId)

        self.__failCount = 0
        self.__errorCount = 0
        self.__results = []

        self.__isDisposed = False

    def sleep(self, seconds):
        time.sleep(seconds)

    @property
    def failCount(self):
        self.__throwIfDisposed()

        return self.__failCount > 0

    @property
    def errorCount(self):
        self.__throwIfDisposed()

        return self.__errorCount > 0

    def addPass(self, message):
        self.__throwIfDisposed()

        self.__results.append(TestResult(ResultCodes.PASS, message))

    def addFail(self, message):
        self.__throwIfDisposed()

        self.__failCount += 1
        self.__results.append(TestResult(ResultCodes.FAIL, message))

    def addError(self, message):
        self.__throwIfDisposed()

        self.__errorCount += 1
        self.__results.append(TestResult(ResultCodes.SCRIPTERROR, message))

    def setResult(self, result, message):
        self.__throwIfDisposed()

        if not isinstance(result, ResultCodes):
            raise Exception(f"Result '{str(result)}' is not of type ResultCodes.")
        
        resultValue = result.value
        if resultValue == ResultCodes.FAIL.value:
            self.__failCount += 1
        elif resultValue == ResultCodes.SCRIPTERROR.value:
            self.__errorCount += 1
        elif resultValue == ResultCodes.SYSTEMERROR.value:
            self.__errorCount += 1

        self.robot.postTestResult(self.testRunId, [ TestResult(result, message) ])

    @property
    def hasFails(self):
        self.__throwIfDisposed()

        return self.__failCount > 0

    @property
    def hasErrors(self):
        self.__throwIfDisposed()

        return self.__errorCount > 0

    def dispose(self):
        self.__isDisposed = True

        if len(self.__results) > 0:
            self.robot.postTestResult(self.testRunId, self.__results)

        if self.__isSelfManaged is True:
            self.robot.tearDown(self.testRunId)

        self.__failCount = None
        self.__errorCount = None
        self.__results = None

        self.testRunId = None
        self.__isSelfManaged = True

        self.robot = None

    def __throwIfDisposed(self):
        if self.__isDisposed is True:
            print("Cannot access a disposed object")
            raise Exception("Cannot access a disposed object.")