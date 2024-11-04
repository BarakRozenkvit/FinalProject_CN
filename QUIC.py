import json
import pickle
import random
import struct
from socket import AF_INET, SOCK_DGRAM, socket
from sys import getsizeof


class quicSocket:

    def __init__(self):
        """
        self.socket: UDP socket of quic Socket
        self.connection_id: unique id of the socket
        self.dest_connection_id: the unique id of the destination connection
        """
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.connection_id = random.randint(1, 100)
        self.dest_connection_id = None
        self.PacketNumber = 0
        # self.lastNumberPacketReceive=0
        self.bufferSize = 9000
        self.largestACK = 0
        self.last_num_of_bytes_Received=0
        self.totalBytesSend=0

    def connect(self, serverAddress):
        """
        1. send connection request
        2. wait for response and save the dest_conncetion_id
        :param serverAddress: address of the server
        :return: void
        """
        self.PacketNumber += 1
        packet = quicPacket('S', self.connection_id, self.PacketNumber, [ACK(self.last_num_of_bytes_Received)])
        data_to_send = packet.pack()
        self.socket.sendto(data_to_send, serverAddress)

        data, serverAddress = self.socket.recvfrom(self.bufferSize)
        buffer = quicPacket.unpack(data)

        if not self.totalBytesSend + 1 == buffer.payload[0].num_of_bytes:
            print("Didnt got some packet")
            exit(1)
        self.dest_connection_id = buffer.dest_connection_id

    def accept(self, buffer_size):
        """
        1. receive connection request and save the dest_conncetion_id
        2. send connection accept
        :param buffer_size:
        :return:
        """

        data, clientAddress = self.socket.recvfrom(self.bufferSize)
        buffer = quicPacket.unpack(data)
        if self.largestACK + 1 == buffer.packet_number:
            self.largestACK += 1
        else:
            print("Didnt got ack")
            exit(1)
        self.dest_connection_id = buffer.dest_connection_id

        self.PacketNumber += 1
        packet = quicPacket('S', self.connection_id, self.PacketNumber, [ACK()])
        self.socket.sendto(packet.pack(), clientAddress)
        return clientAddress

    def send(self, serverAddress, data=[]):
        """
        1. send data
        :param serverAddress
        :param data
        :return:
        """
        self.PacketNumber += 1
        data.insert(0,ACK(self.last_num_of_bytes_Received+1))
        packet = quicPacket('S', self.dest_connection_id, self.PacketNumber, data)
        data_to_send = packet.pack()
        self.socket.sendto(data_to_send, serverAddress)
        self.totalBytesSend+=len(data_to_send)


    def receive(self, buffer_size):
        """
        1. receive data
        :param buffer_size
        :return:
        """
        buffer, clientAddress = self.socket.recvfrom(self.bufferSize)
        buffer = quicPacket.unpack(buffer)
        if buffer.dest_connection_id != self.connection_id:
            return
        if not self.totalBytesSend+1==buffer.payload[0].num_of_bytes:
            print("Didnt got some packet")

        return buffer.payload


class quicPacket:
    """
     Header Size = 9 Bytes
    QUIC Packet easy version for QUIC Short packet and QUIC Long packet
    """

    def __init__(self, flag, dst_connection_id, packet_number, payload):
        self.flags = flag  # Character
        self.dest_connection_id = dst_connection_id  # Integer
        self.packet_number = packet_number  # Integer
        self.payload = payload

    def pack(self):
        """
        serialize the packet
        :return:
        """
        data = struct.pack("!cii", self.flags.encode(), self.dest_connection_id, self.packet_number)
        for frame in self.payload:
            if type(frame) == Stream:
                encoded = frame.stream_data.encode()
                data += struct.pack("!iii", frame.stream_id, len(encoded), frame.offset)
                data += encoded
            if type(frame) == ACK:
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
        p = 9
        flag, dest_connection, packet_number = struct.unpack("!cii", data[0:p])
        payload = []
        num_of_bytes= struct.unpack("!i", data[p:p + 4])
        p += 4
        payload.append(ACK(num_of_bytes))
        while p < size:
            stream_id, length, offset = struct.unpack("!iii", data[p:p + 12])
            p += 12
            stream_data = data[p:p + length].decode("utf-8")
            p += length
            payload.append(Stream(stream_id, offset, length, stream_data))

        return quicPacket(flag.decode(), dest_connection, packet_number, payload)


class Stream:

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
    def __init__(self, num_of_bytes):
        self.num_of_bytes=num_of_bytes