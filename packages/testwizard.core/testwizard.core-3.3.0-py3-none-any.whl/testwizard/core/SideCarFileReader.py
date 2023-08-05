import os
import json

class SideCarFileReader:
    @staticmethod
    def read(filePath):
        with open(filePath) as data_file:
            data = json.load(data_file)

        return data