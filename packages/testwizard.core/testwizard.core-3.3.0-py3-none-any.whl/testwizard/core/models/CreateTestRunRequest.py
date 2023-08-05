class CreateTestRunRequest:
    def __init__(self, scriptFilePath, workingDirectory, metadata):
        self.__scriptFilePath = scriptFilePath
        self.__workingDirectory = workingDirectory
        self.__tester = metadata.get("tester")
        self.__parameters = metadata.get("parameters")
        self.__resources = metadata.get("resources", {})
        self.__customProperties = metadata.get("customProperties")
        self.__outputFolder = metadata.get("outputFolder")

    @property
    def scriptFilePath(self):
        return self.__scriptFilePath

    @property
    def workingDirectory(self):
        return self.__workingDirectory

    @property
    def tester(self):
        return self.__tester

    @property
    def parameters(self):
        return self.__parameters

    @property
    def resources(self):
        return self.__resources

    @property
    def customProperties(self):
        return self.__customProperties

    @property
    def outputFolder(self):
        return self.__outputFolder
