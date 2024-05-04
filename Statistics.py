

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





