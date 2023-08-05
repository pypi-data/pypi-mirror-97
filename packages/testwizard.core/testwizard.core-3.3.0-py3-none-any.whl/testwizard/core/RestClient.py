import jsons
import http.client

from .Errors import TestSystemError

class RestClient:
    def __init__(self, baseUri):
        self._baseUri = baseUri

    def __createConnection(self):
        return http.client.HTTPConnection(self._baseUri)

    def __get(self, relativeUrl, errorMessagePrefix):
        conn = self.__createConnection()
        try:
            response = self.__send(conn, "GET", relativeUrl, None,  errorMessagePrefix)
            return response.read().decode('utf-8')
        finally:
            conn.close()

    def getText(self, relativeUrl, errorMessagePrefix):
        text = self.__get(relativeUrl, errorMessagePrefix)
        return str(text)

    def getJson(self, relativeUrl, errorMessagePrefix):
        text = self.__get(relativeUrl, errorMessagePrefix)
        return jsons.loads(text)

    def post(self, relativeUrl, requestObj, errorMessagePrefix):
        conn = self.__createConnection()
        try:
            self.__send(conn, "POST", relativeUrl, requestObj, errorMessagePrefix)
        finally:
            conn.close()

    def postJson(self, relativeUrl, requestObj, errorMessagePrefix):
        conn = self.__createConnection()
        try:
            response = self.__send(conn, "POST", relativeUrl, requestObj, errorMessagePrefix)
            text = response.read().decode('utf-8')
            return jsons.loads(text)
        finally:
            conn.close()

    def put(self, relativeUrl, requestObj, errorMessagePrefix):
        conn = self.__createConnection()
        try:
            self.__send(conn, "PUT", relativeUrl, requestObj, errorMessagePrefix)
        finally:
            conn.close()

    def delete(self, relativeUrl, requestObj, errorMessagePrefix):
        conn = self.__createConnection()
        try:
            self.__send(conn, "DELETE", relativeUrl, requestObj, errorMessagePrefix)
        finally:
            conn.close()

    def __send(self, conn, method, relativeUrl, requestObj, errorMessagePrefix):
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        if requestObj is None:
            requestBody = None
        else:
            requestBody = jsons.dumps(requestObj)

        try:
            conn.request(method, relativeUrl, requestBody, headers)
        except:
            raise Exception("Could not connect to robot")
        response = conn.getresponse()
        if response.status != 200:
            self.__throwHttpRequestError(response, errorMessagePrefix)

        return response

    def __throwHttpRequestError(self, response, message):
        if response.status == 0:
            message += ": Could not connect to robot"
            raise TestSystemError(message)
        elif response.status == 500:
            errorObj = jsons.loads(response.read())
            if "message" in errorObj:
                message += ": " + errorObj["message"]
            if "exceptionMessage" in errorObj:
                message += ": " + errorObj["exceptionMessage"]
            if self.__isSytemException(errorObj):
                raise TestSystemError(message)
        elif response.status == 409:
            message += ": All executors are busy"
            raise TestSystemError(message)
        elif response.reason:
            text = response.read()
            try:
                errorObj = jsons.loads(text)
                if "message" in errorObj:
                    message += ": " + errorObj["message"]
                if "exceptionMessage" in errorObj:
                    message += ": " + errorObj["exceptionMessage"]
                message += ": " + errorObj
            except:
                message += ": " + str(text)
        raise Exception(message)

    def __isSytemException(self, ex):
        return ex["exceptionType"] == "TestWizard.Automation.Extensibility.Exceptions.TestSystemException"
