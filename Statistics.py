

class Statistics:
    def __init__(self):
        self.streams = []

    def unpack(self,payload):
        """
        convert the data from packet to Buffer Manager
        :param payload: data from quicPacket
        :return: BufferManager Object
        """
        for stream in payload:
            found = False
            for idx in self.streams:
                if idx.stream_id == stream.stream_id:
                    idx.stream_data += stream.stream_data
                    found = True

            if not found:
                self.streams.append(stream)

    def hagit_check(self):
        for stream in self.streams:
            with open(f"Files/{stream.stream_id}.txt", "wb") as f:
                data_to_write = stream.stream_data
                if isinstance(data_to_write, str):
                    data_to_write = data_to_write.encode()
                f.write(data_to_write)





