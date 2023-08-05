class TestResult:
    def __init__(self, result, comment):
        self.__result = result.value
        self.__comment = comment
    
    @property
    def result(self):
        return self.__result
    
    @property
    def comment(self):
        return self.__comment
