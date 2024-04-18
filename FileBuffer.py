import random
import sys
import time
from threading import Thread
from QUIC import Stream
from FileHandler import FileHandler


class FileBuffer:

    def __init__(self,path):
        """
        :param path: path to file
        self.buffer: buffer
        self.streamID: uniqe ID to assign Stream Object
        self.fileHandler: FileHandler Object
        """
        self.buffer = []
        self.bufferMaxSize = 5
        self.packageSize = random.randint(1000,2000)
        self.streamID = random.randint(1,20)
        self.fileHandler = FileHandler(path)
        self.threshold = 2

    def isEmpty(self):
        """
        this function checks if buffer is empty
        :return:
        """
        if len(self.buffer) == 0:
            return True
        return False

    def isBelowThreshold(self):
        """
        this function checks if buffer is below threshold
        :return:
        """
        if len(self.buffer) < self.threshold:
            return True
        else:
            return False

    def fillBuffer(self,size):
        """
        this function fills the buffer
        :return:
        """
        self.buffer = self.fileHandler.getData(size)

    def clearBuffer(self):
        """
        this function clears the buffer
        :return:
        """
        self.buffer.clear()

    def toStream(self):
        """
        1. convert the function to Stream Foramt
        2. clears the buffer
        :return: Stream Object
        """

    def toFileBuffer(self,stream):
        """
        convert the stream to FileBuffer
        :param stream: Stream Object
        :return: FileBuffer Object
        """
class BufferManager:

    def __init__(self,file_list):
        """
        1. initialize the file list to empty
        2. for every file in file list create FileBuffer object
        :param file_list: list of files
        """
        self.file_buffers = []
        for i in range(0, len(file_list)):
            self.file_buffers.append(FileBuffer(file_list[i]))


    ### Implement this functions async
    def manage(self):
        """
        iterate through all the file_buffers, if buffer is empty, fill it
        :return: void
        """

    def pack(self,payload_size):
        """
        while the total data packed is less than payload_size iterate through all the file_buffers,
        if buffer is available for packing, convert it to Stream object and clear the buffer
        :return: Stream array
        """

    def unpack(self,payload):
        """
        convert the data from packet to Buffer Manager
        :param payload: data from quicPacket
        :return: BufferManager Object
        """







