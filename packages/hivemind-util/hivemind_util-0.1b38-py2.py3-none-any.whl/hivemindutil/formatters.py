import re
import os.path


class FileHandle():
    def __init__(self, f):
        self.path, fileName = os.path.split(f)
        self.name, self.extension = os.path.splitext(fileName)

    def __str__(self):
        filePath = self.getFilePath().replace('(', '((').replace(')', '))')
        return f'!file({filePath})'

    def getFilePath(self):
        return f'{self.path}/{self.getFullName()}' if self.path else self.getFullName()

    def getFullName(self):
        return f'{self.name}{self.extension}'

    @staticmethod
    def isFileHandle(s):
        match = re.match(r'^!file\((?P<file>.+)\)$', fileHandle)
        return True if match else False

    @staticmethod
    def parse(fileHandle):
        match = re.match(r'^!file\((?P<file>.+)\)$', fileHandle)
        if match:
            f = match.group('file')
            return FileHandle(f.replace('((', '(').replace('))', ')'))
        else:
            raise Exception(f'{fileHandle} is not a valid FileHandle')


class HivemindApiUrl(object):
    def __init__(self, baseurl):
        _, self.instance, _ = self.cleanBaseUrl(baseurl).split('.', maxsplit=2)

    @staticmethod
    def cleanBaseUrl(url):
        url = url.rstrip('/')
        if url[:4].lower() != 'http':
            url = 'https://' + url
        return url

    def getStudioApiUrl(self):
        return f'https://studio.{self.instance}/hvmd.io'

    def getFilesApiUrl(self):
        return f'https://files-client-api.{self.instance}.hvmd.io'

    def getChainingApiUrl(self):
        return f'https://chaining-client-api.{self.instance}.hvmd.io'
