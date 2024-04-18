import os
import random


class FileHandler:

    def __init__(self,path):
        """
        self.path: file path
        self.reader: file reader
        self.packageSize: package size that is random between 1000 and 2000
        self.fileSize: file size
        self.EOF: if we reach EOF
        """
        self.path = path
        self.reader = open(path,"r")
        self.fileSize = os.path.getsize(self.path)
        self.EOF = False

    def getData(self,size):
       """
       chek if file reader has got to the end of the file,
       if not, return the size paramter of data
       if yes set self.EOF to True
       :return:
       """
       if not (self.reader.tell() == self.fileSize):
            return self.reader.read(size)
       else:
           self.EOF = True

    def getSequenceNumber(self):
        """
        get the first next byte of the package to send
        :return:
        """
        return self.reader.tell() + 1