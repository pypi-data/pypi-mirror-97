from pprint import pprint
from argparse import ArgumentParser
import atexit
import os
import sys
import datetime
import time

from .Session import Session
from .SideCarFileReader import SideCarFileReader

from .Errors import TestSystemError
from .ResultCodes import ResultCodes

class TestWizard(object):
    def __enter__(self):
        parser = ArgumentParser()
        parser.add_argument("-s", "--sidecar", dest="sidecar", help="location of the sidecar file" )
        parser.add_argument("-t", "--testrun", dest="testrun", help="testrun" )
        args = parser.parse_args()

        scriptFilePath = self.__getScriptFilePath()
        sideCarFilePath = self.__getSideCarFilePath(args, scriptFilePath)
        workingDirectory = self.__getWorkingDirectory()

        metadata = SideCarFileReader.read(sideCarFilePath)
        if not 'outputFolder' in metadata:
            metadata["outputFolder"] = self.__constructOutputFolder(scriptFilePath)

        self.session = Session(scriptFilePath, workingDirectory, metadata, args.testrun)

        return self

    def __exit__(self, type, value, traceback):
        if isinstance(value, TestSystemError):
            self.session.setResult(ResultCodes.SYSTEMERROR, str(value))
        elif isinstance(value, Exception):
            self.session.setResult(ResultCodes.SCRIPTERROR, str(value))

        self.session.dispose()

    def __getScriptFilePath(self):
        return os.path.abspath(sys.argv[0])

    def __getWorkingDirectory(self):
        return os.getcwd()

    def __getSideCarFilePath(self, args, scriptFilePath):
        if args.sidecar is not None:
            return args.sidecar
        
        return os.path.splitext(scriptFilePath)[0] + ".json"

    def __constructOutputFolder(self, scriptFilePath):
        strDate = datetime.datetime.now().isoformat()
        timestr = time.strftime("%Y%m%d-%H%M%S")
        strDate.replace("-", "")
        strDate.replace(":", "")
        strDate.replace(".", "")

        return os.getcwd() + "/Runs/" + os.path.splitext(os.path.basename(scriptFilePath))[0] + "_" + timestr
