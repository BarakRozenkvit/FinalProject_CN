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
        if(path != ""):
            self.reader = open(path,"r")
            self.fileSize = os.path.getsize(self.path)
            print(self.path , " : " , self.fileSize)
        self.EOF = False

    def getData(self,size):
       """
       check if file reader has got to the end of the file,
       if not, return the size parameter of data
       if data is less than wanted size, set self.EOF to True
       else yes set self.EOF to True
       :return:
       """
       if not (self.reader.tell() == self.fileSize):
            data = self.reader.read(size)
            if len(data) < size:
                self.EOF = True
                # data += "EOF"
                #print(self.path, " is Finished")
            return data
       else:
           self.EOF = True

    def getSequenceNumber(self):
        """
        get the first next byte of the package to send
        :return:
        """
        return self.reader.tell() + 1

if __name__ == '__main__':
    d = FileHandler("Files/1.txt")
    g =d.getData(88800)
    g = d.getData(880)

    print(1)