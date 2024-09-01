import random
import sys
import time
from threading import Thread, Lock
from QUIC import Stream
from FileHandler import FileHandler
class FileBuffer:

    def __init__(self,path):
        """
        :param path: path to file
        self.buffer: [(data1,seqNum1),(data2,seqNum2),(data3,seqNum3)]
        self.streamID: uniqe ID to assign Stream Object
        self.packageSize: size of each package of data from file
        self.fileHandler: FileHandler Object
        """
        self.buffer = []
        self.bufferMaxSize = 5
        self.threshold = 2
        self.packageSize = random.randint(1000,2000)
        self.streamID = random.randint(1,2000)
        self.fileHandler = FileHandler(path)

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

    def fillBuffer(self):
        """
        this function fills the buffer
        :return:
        """
        count = self.bufferMaxSize - len(self.buffer)
        for i in range(1,count):
            if not (self.fileHandler.EOF):
                data = (self.fileHandler.getData(self.packageSize),self.fileHandler.getSequenceNumber())
                self.buffer.append(data)

    def clearBuffer(self):
        """
        this function clears the buffer
        :return:
        """
        self.buffer.clear()

    def toStream(self):
        """
        1. pop 0 index from list (Queue)
        2. convert to Stream
        :return: Stream Object
        """
        data = self.buffer.pop(0)
        return Stream(self.streamID,data[1],len(data[0]),data[0])

    @staticmethod
    def toFileBuffer(stream):
        """
        convert the stream to FileBuffer
        :param stream: Stream Object
        :return: FileBuffer Object
        """
        # open(stream.stream_id + ".txt","w").close()
        fileBuffer = FileBuffer("")
        fileBuffer.streamID = stream.stream_id
        fileBuffer.packageSize = stream.length
        fileBuffer.buffer = [stream.stream_data]
        return fileBuffer

class BufferManager:

    def __init__(self,file_list):
        """
        1. initialize the file list to empty
        2. for every file in file list create FileBuffer object
        :param file_list: list of files
        """
        self.fileBuffers = []
        self.minPackageSize = 2000
        self.res = 0
        for i in range(0, len(file_list)):
            fileBuffer = FileBuffer(file_list[i])
            self.res += fileBuffer.fileHandler.fileSize
            if fileBuffer.packageSize < self.minPackageSize:
                self.minPackageSize = fileBuffer.packageSize
            self.fileBuffers.append(fileBuffer)
        self.lock = Lock()
        self.running = True

    ### Implement this functions async
    def manage(self):
        """
        run this process while the flag self.running is True
        for each buffer, if its empty or below threshold,
        lock the buffer to the thread, fill it and release the buffer
        :return: void
        """
        while self.running:
            for fileBuffer in self.fileBuffers:
                if fileBuffer.isEmpty() or fileBuffer.isBelowThreshold():
                    self.lock.acquire()
                    fileBuffer.fillBuffer()
                    self.lock.release()


    def pack(self,payload_size):
        """
        while the payload size is greater than the minimum of package size of all the packages of all files
        and self.running is True:
        1. shuffle the list, for every buffer, lock the buffer to thread
        2. if fileBuffer is not empty and the package size is smaller than payload size, convert to Stream and
        add to list
        3. if all buffers are empty stop this function
        :return: Stream array
        """
        streamsToSend = []
        while payload_size > self.minPackageSize and self.running:
            EmptyBuffers = True
            random.shuffle(self.fileBuffers)
            for fileBuffer in self.fileBuffers:
                self.lock.acquire()
                if (not fileBuffer.isEmpty()) and fileBuffer.packageSize < payload_size:
                    EmptyBuffers = False
                    streamsToSend.append(fileBuffer.toStream())
                    payload_size -= fileBuffer.packageSize
                self.lock.release()
            if EmptyBuffers:
                break
        return streamsToSend

    # def unpack(self,payload):
    #     """
    #     convert the data from packet to Buffer Manager
    #     :param payload: data from quicPacket
    #     :return: BufferManager Object
    #     """
    #     for stream in payload:
    #         found = False
    #         for fileBuffer in self.fileBuffers:
    #             if fileBuffer.streamID == stream.stream_id:
    #                 fileBuffer.buffer.append(stream.stream_data)
    #                 found = True
    #
    #         if not found:
    #             self.fileBuffers.append(FileBuffer.toFileBuffer(stream))







if __name__ == '__main__':
    b = BufferManager(["Files/1.txt","Files/2.txt","Files/3.txt","Files/4.txt","Files/5.txt"])
    t = Thread(target=b.manage)
    t.start()
    i=0
    g=[1]
    while g!=[]:
        time.sleep(0.00000005)
        g = b.pack(5000)
        i+=1
        t = 0
        for l in g:
            t+=l.length

        print(t,g)

    print(i)
    for f in b.fileBuffers:
        print(f.fileHandler.EOF)

    b.running = False







