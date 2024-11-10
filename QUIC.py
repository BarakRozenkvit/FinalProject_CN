import json
import pickle
import random
import struct
from socket import AF_INET, SOCK_DGRAM, socket
from sys import getsizeof


class quicSocket:

    def __init__(self,buffer_size):
        """
        self.socket: UDP socket of quic Socket
        self.connection_id: unique id of the socket
        self.dest_connection_id: the unique id of the destination connection
        """
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.connection_id = random.randint(1, 100)
        self.buffer_size = buffer_size
        self.PacketNumber = 0


        # Data for Validation
        self.dest_connection_id = None
        self.bytes_received=0
        self.bytes_sent=0

    def connect(self, serverAddress):
        """
        1. send connection request
        2. wait for response and save the dest_conncetion_id
        :param serverAddress: address of the server
        :return: void
        """

        self.send(['S'],serverAddress)
        buffer,clientAddress = self.receive()

    def accept(self):
        """
        1. receive connection request and save the dest_conncetion_id
        2. send connection accept
        :param buffer_size:
        :return:
        """
        buffer,clientAddress = self.receive()
        self.send(['S','A'],clientAddress)
        return clientAddress

    def send(self,packet_flags, serverAddress, data=[]):
        """
        1. send data
        :param serverAddress
        :param data
        :return:
        """
        self.PacketNumber += 1
        if len(packet_flags) == 1:
            packet_flags.append('0')

        if 'A' in packet_flags:
            print("Send ACK for: " ,self.bytes_received+1)
            print("Bytes Received: ", self.bytes_received)
            print("Bytes Sent: " , self.bytes_sent)
            data.insert(0,ACK(self.bytes_received+1))
        
        if 'S' in packet_flags:
            print("Send SYN")
            packet = quicPacket(packet_flags, self.connection_id, self.PacketNumber, data)
        elif 'M' in packet_flags:
            print("Send DATA")
            packet = quicPacket(packet_flags, self.dest_connection_id, self.PacketNumber, data)
        elif 'F' in packet_flags:
            print("Send FIN")
            packet = quicPacket(packet_flags, self.dest_connection_id, self.PacketNumber, data)

        data_to_send = packet.pack()
        self.bytes_sent+=len(data_to_send)
        self.socket.sendto(data_to_send, serverAddress)

    def receive(self):
        """
        1. receive data
        :param buffer_size
        :return:
        """
        buffer, clientAddress = self.socket.recvfrom(self.buffer_size)
        buffer = quicPacket.unpack(buffer)
        
        if 'S' in buffer.flags:
            print("Got SYN")
            self.dest_connection_id = buffer.dest_connection_id

        elif 'M' in  buffer.flags:
            print("Got DATA")
            if buffer.dest_connection_id != self.connection_id:
                ## Wrong client
                return
            
        elif 'F' in buffer.flags:
            print("Got FIN")
            i =0
            
        if 'A' in buffer.flags:
            print("Got ACK for: " ,buffer.payload[0].num_of_bytes)
            print("Bytes Received: ", self.bytes_received)
            print("Bytes Sent: " , self.bytes_sent)
            
            if not self.bytes_sent+1==buffer.payload[0].num_of_bytes:
                print("Didnt got some packet")

        

        return buffer, clientAddress


class quicPacket:
    """
     Header Size = 9 Bytes
    QUIC Packet easy version for QUIC Short packet and QUIC Long packet
    """

    def __init__(self, flag, dst_connection_id, packet_number, payload):
        self.flags = flag # 3 Characters
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
        p = 10
        type,ack, dest_connection, packet_number = struct.unpack("!ccii", data[0:p])
        flags = [type.decode(),ack.decode()]
        payload = []
        if 'A' in flags:
            num_of_bytes= struct.unpack("!i", data[p:p + 4])
            p += 4
            payload.append(ACK(num_of_bytes))
        if 'M' in flags:
            while p < size:
                stream_id, length, offset = struct.unpack("!iii", data[p:p + 12])
                p += 12
                stream_data = data[p:p + length].decode("utf-8")
                p += length
                payload.append(Stream(stream_id, offset, length, stream_data))

        return quicPacket(flags, dest_connection, packet_number, payload)


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