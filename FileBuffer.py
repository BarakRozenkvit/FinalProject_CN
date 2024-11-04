import queue
import random
import time

from FileHandler import FileHandler
from QUIC import Stream


class FileBuffer:

    def __init__(self,path):
        """
        :param path: path to file
        self.buffer: [(data1,seqNum1),(data2,seqNum2),(data3,seqNum3)]
        self.streamID: uniqe ID to assign Stream Object
        self.packageSize: size of each package of data from file
        self.fileHandler: FileHandler Object
        """
        self.buffer = queue.Queue()
        self.packageSize = random.randint(1000,2000) ## Parameter to Divide Chunks of data for each flow (flow == file)
        self.streamID = random.randint(1,100)
        self.fileHandler = FileHandler(path)

    def isEmpty(self):
        """
        this function checks if buffer is empty
        :return:
        """
        return self.buffer.empty()

    def fillBuffer(self):
        """
        this function fills the buffer
        :return:
        """
        while not self.fileHandler.EOF:
            data = (self.fileHandler.getData(self.packageSize), self.fileHandler.getSequenceNumber())
            self.buffer.put(data)

    def toStream(self):
        """
        1. pop 0 index from list (Queue)
        2. convert to Stream
        :return: Stream Object
        """
        data = self.buffer.get(block=False)
        return Stream(self.streamID,data[1],len(data[0]),data[0])

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
        self.running = True

    def manage(self):
        """
        run this process while the flag self.running is True
        for each buffer, if its empty or below threshold,
        lock the buffer to the thread, fill it and release the buffer
        :return: void
        """
        for fileBuffer in self.fileBuffers:
            fileBuffer.fillBuffer()

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
        while payload_size >=0:
            res = 0
            idx = list(range(0,len(self.fileBuffers)))
            random.shuffle(idx)
            for i in idx:
                if (payload_size  - self.fileBuffers[i].packageSize < 0 or self.fileBuffers[i].buffer.qsize() == 0):
                    res+=1
                    continue

                add = self.fileBuffers[i].toStream()
                streamsToSend.append(add)
                payload_size -= self.fileBuffers[i].packageSize

            if( res == len(self.fileBuffers)):
                break

        return streamsToSend




if __name__ == '__main__':
    b = BufferManager(["Files/1.txt","Files/2.txt","Files/3.txt","Files/4.txt"])
    b.manage()
    # t = Thread(target=b.manage)
    # t.start()
    i=0
    g=[1]
    while g!=[]:
        time.sleep(0.00000005)
        g = b.pack(3000)
        i+=1
        t = 0
        for l in g:
            t+=l.length

        print(t,g)

    print(i)
    for f in b.fileBuffers:
        print(f.fileHandler.EOF)

    b.running = False







