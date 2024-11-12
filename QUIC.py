import random
import struct
from socket import AF_INET, SOCK_DGRAM, socket

class quicSocket:

    def __init__(self,buffer_size):
        """
        self.socket: UDP socket of quic Socket
        self.connection_id: unique id of the socket
        self.buffer size: size of the buffer
        self.dest_connection_id: the unique id of the destination connection
        """
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.connection_id = random.randint(1, 100)
        self.buffer_size = buffer_size
        self.packet_number = 0

        # Data for Validation
        self.dest_connection_id = None
        self.bytes_received=0
        self.bytes_sent=0

    def connect(self, server_address):
        """
        send SYN to Server
        """
        self.send(['S'],server_address,[])
        self.receive()

    def accept(self):
        """
        Receive SYN from client and send SYN ACK to client
        """
        _buffer,client_address = self.receive()
        self.send(['S','A'],client_address,[])
        return client_address

    def send(self,packet_flags, server_address, data):
        """
        Build Quic packet according to flags and data and send it
        """
        self.packet_number += 1
        packet = quicPacket(packet_flags,self.dest_connection_id,self.packet_number,data)
        if len(packet_flags) == 1:
            packet_flags.append('0')

        if 'A' in packet_flags:
            # Insert ACK frame into 0 idx in payload
            packet.payload.insert(0,ACK(self.bytes_received+1))

        if 'S' in packet_flags:
            # if SYN send my connection id
            packet.dest_connection_id=self.connection_id

        data_to_send = packet.pack()
        self.bytes_sent += len(data_to_send)
        self.socket.sendto(data_to_send, server_address)

    def receive(self):
        """
        Receive buffer
        """
        buffer, client_address = self.socket.recvfrom(self.buffer_size)
        self.bytes_received += len(buffer)
        buffer = quicPacket.unpack(buffer)

        if 'S' in buffer.flags:
            # if got SYN replace the dst connection id with new one
            self.dest_connection_id = buffer.dest_connection_id

        elif 'D' in  buffer.flags:
            # if got data from other client
            if buffer.dest_connection_id != self.connection_id:
                print("Connection is taken by another client")

        if 'A' in buffer.flags:
            # if got ACK packet check if packet is lost
            if not self.bytes_sent+1==buffer.payload[0].num_of_bytes:
                print("a Packet is Lost")

        return buffer, client_address


class quicPacket:
    """
     Header Size = 10 Bytes
    QUIC Packet easy version for QUIC Short packet and QUIC Long packet
    """
    size=10
    def __init__(self, flag, dst_connection_id, packet_number, payload):
        self.flags = flag # 2 Characters
        self.dest_connection_id = dst_connection_id  # Integer
        self.packet_number = packet_number  # Integer
        self.payload = payload

    def pack(self):
        """
        serialize the packet
        :return:
        """
        data = struct.pack("!ccii", self.flags[0].encode(),self.flags[1].encode(), self.dest_connection_id, self.packet_number)
        for frame in self.payload:
            if isinstance(frame,Stream):
                encoded = frame.stream_data.encode()
                data += struct.pack("!iii", frame.stream_id, len(encoded), frame.offset)
                data += encoded
            if isinstance(frame,ACK):
                data += struct.pack("!i", frame.num_of_bytes)
        return data

    @staticmethod
    def unpack(data):
        """
        deserialize the packet
        :param packet:
        :return:
        """
        size = len(data)
        i = quicPacket.size
        mode ,ack, dest_connection, packet_number = struct.unpack("!ccii", data[0:i])
        flags = [mode.decode(),ack.decode()]
        payload = []
        if 'A' in flags:
            num_of_bytes = struct.unpack("!i", data[i:i + ACK.size])
            i += ACK.size
            payload.append(ACK(num_of_bytes[0]))
        if 'D' in flags:
            while i < size:
                stream_id, length, offset = struct.unpack("!iii", data[i:i + Stream.size])
                i += Stream.size
                stream_data = data[i:i + length].decode("utf-8")
                i += length
                payload.append(Stream(stream_id, offset, length, stream_data))

        return quicPacket(flags, dest_connection, packet_number, payload)


class Stream:
    size=12
    def __init__(self, ID, offset, length, data):
        """
        Header Size = 12 Bytes
        :param ID: unique stream id
        :param offset: sequence number of data
        :param length: length of data
        :param data: data
        """
        self.stream_id = ID
        self.offset = offset
        self.length = length
        self.stream_data = data


class ACK:
    size=4
    def __init__(self, num_of_bytes):
        self.num_of_bytes=num_of_bytes