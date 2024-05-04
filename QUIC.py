import pickle
import random
from socket import AF_INET,SOCK_DGRAM,socket


class quicSocket:

    def __init__(self):
        """
        self.socket: UDP socket of quic Socket
        self.connection_id: unique id of the socket
        self.dest_connection_id: the unique id of the destination connection
        """
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.connection_id = random.randint(1,100)
        self.dest_connection_id = None
        self.packetNumber = 0
        self.bufferSize = 9000

    def connect(self,serverAddress):
        """
        1. send connection request
        2. wait for response and save the dest_conncetion_id
        :param serverAddress: address of the server
        :return: void
        """
        self.packetNumber += 1
        packet = quicPacket(self.connection_id,self.packetNumber,[])
        self.socket.sendto(packet.pack(),serverAddress)

        buffer, serverAddress = self.socket.recvfrom(self.bufferSize)
        buffer = quicPacket.unpack(buffer)
        self.dest_connection_id = buffer.dest_connection_id
        print("Connection successfully established to", serverAddress)

    def accept(self,buffer_size):
        """
        1. receive connection request and save the dest_conncetion_id
        2. send connection accept
        :param buffer_size:
        :return:
        """
        buffer, clientAddress = self.socket.recvfrom(self.bufferSize)
        buffer = quicPacket.unpack(buffer)
        self.dest_connection_id = buffer.dest_connection_id

        print("got Connection request from", clientAddress)
        self.packetNumber += 1
        packet = quicPacket(self.connection_id, self.packetNumber, [])
        self.socket.sendto(packet.pack(), clientAddress)
        return clientAddress

    def send(self,serverAddress,data):
        """
        1. send data
        2. wait for ACK
        :param serverAddress
        :param data
        :return:
        """
        self.packetNumber += 1
        packet = quicPacket(self.dest_connection_id,self.packetNumber,data)
        self.socket.sendto(packet.pack(),serverAddress)

        buffer, clientAddress = self.socket.recvfrom(self.bufferSize)
        buffer = quicPacket.unpack(buffer)
        if buffer.dest_connection_id != self.connection_id:
            return

        ## handle ACK



    def receive(self, buffer_size):
        """
        1. receive data
        2. send ACK
        :param buffer_size
        :return:
        """
        buffer, clientAddress = self.socket.recvfrom(self.bufferSize)
        buffer = quicPacket.unpack(buffer)
        if buffer.dest_connection_id != self.connection_id:
            return

        # send ack
        self.packetNumber += 1
        packet = quicPacket(self.dest_connection_id, self.packetNumber, [])
        self.socket.sendto(packet.pack(),clientAddress)

        return buffer.payload


class quicPacket:
    """
    QUIC Packet easy version for QUIC Short packet and QUIC Long packet
    """
    def __init__(self,dst_connection_id,packet_number,payload):
        self.flags = None
        self.dest_connection_id = dst_connection_id
        self.packet_number = packet_number
        self.payload = payload

    def pack(self):
        """
        serialize the packet
        :return:
        """
        return pickle.dumps(self)

    @staticmethod
    def unpack(packet):
        """
        deserialize the packet
        :param packet:
        :return:
        """
        return pickle.loads(packet)

class Stream:

    def __init__(self,ID,offset,length,data):
        """
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
    """
    ?
    """
    def __init__(self):
        self.largestACK = 0
        self.ACKdelay = None
        self.ACKRangCount = None
        self.firstACKRange = None
        self.ACkRange = []
