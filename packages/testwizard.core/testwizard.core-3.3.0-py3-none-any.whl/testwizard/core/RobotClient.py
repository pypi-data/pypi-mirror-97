import urllib

from .RestClient import RestClient
from .models.CreateTestRunRequest import CreateTestRunRequest

class RobotClient:
    def __init__(self, baseUri):
        self.__client = RestClient(baseUri)

        self.__isDisposed = False
    
    def createTestRun(self, scriptFilePath, workingDirectory, metadata):
        self.__throwIfDisposed()

        requestObj = CreateTestRunRequest(scriptFilePath, workingDirectory, metadata)

        testRun = self.__client.postJson("/api/v2/testruns", requestObj, "Error creating session")

        return testRun["id"]

    def getSessionInfo(self, testRunId):
        self.__throwIfDisposed()

        return self.__client.getJson(f'/api/v2/testruns/{testRunId}/info', 'Error getting session info')

    def getTestObject(self, resourceId):
        self.__throwIfDisposed()

        return self.__client.getJson('/api/v2/testobjects/' + urllib.parse.quote(resourceId), 'Get TestObject by id failed')

    def executeCommand(self, testRunId, resourceName, commandName, requestObj, errorMessagePrefix):
        self.__throwIfDisposed()

        return self.__client.postJson(f'/api/v2/testruns/{testRunId}/testobjects/{urllib.parse.quote(resourceName)}/commands/{commandName}', requestObj, errorMessagePrefix)

    def postTestResult(self, testRunId, requestObj):
        self.__throwIfDisposed()

        self.__client.post(f'/api/v2/testruns/{testRunId}/result', requestObj, 'Error setting test result')

    def tearDown(self, testRunId):
        self.__throwIfDisposed()

        self.__client.delete('/api/v2/testruns/' + testRunId, None, 'Error tearing down session')

    def dispose(self):
        self.__isDisposed = True

        self.__client = None

    def __throwIfDisposed(self):
        if self.__isDisposed is True:
            raise Exception("Cannot access a disposed object.")