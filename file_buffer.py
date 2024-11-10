import queue
import random
from file_handler import FileHandler
from quic import Stream


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
        self.package_size = random.randint(1000,2000) ## Parameter to Divide Chunks of data for each flow (flow == file)
        self.stream_id = random.randint(1,100)
        self.file_handler = FileHandler(path)

    def is_empty(self):
        """
        this function checks if buffer is empty
        :return:
        """
        return self.buffer.empty()

    def fill_buffer(self):
        """
        this function fills the buffer
        :return:
        """
        while not self.file_handler.eof:
            data = (self.file_handler.get_data(self.package_size), self.file_handler.get_sequence_number())
            self.buffer.put(data)

    def to_stream(self):
        """
        1. pop 0 index from list (Queue)
        2. convert to Stream
        :return: Stream Object
        """
        data = self.buffer.get(block=False)
        return Stream(self.stream_id,data[1],len(data[0]),data[0])

class BufferManager:

    def __init__(self,file_list):
        """
        1. initialize the file list to empty
        2. for every file in file list create FileBuffer object
        :param file_list: list of files
        """
        self.file_buffers = []
        self.min_package_size = 2000
        self.res = 0
        for i in file_list:
            file_buffer = FileBuffer(i)
            self.res += file_buffer.file_handler.file_size
            if file_buffer.package_size < self.min_package_size:
                self.min_package_size = file_buffer.package_size
            self.file_buffers.append(file_buffer)
        self.running = True

    def manage(self):
        """
        run this process while the flag self.running is True
        for each buffer, if its empty or below threshold,
        lock the buffer to the thread, fill it and release the buffer
        :return: void
        """
        for file_buffer in self.file_buffers:
            file_buffer.fill_buffer()

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
        streams_to_send = []
        while payload_size >=0:
            res = 0
            idx = list(range(0,len(self.file_buffers)))
            random.shuffle(idx)
            for i in idx:
                if (payload_size  - self.file_buffers[i].package_size < 0 or 
                    self.file_buffers[i].buffer.qsize() == 0):
                    res+=1
                    continue

                add = self.file_buffers[i].to_stream()
                streams_to_send.append(add)
                payload_size -= self.file_buffers[i].package_size
                payload_size -= Stream.size


            if res == len(self.file_buffers):
                break

        return streams_to_send
