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
        print("Initializing quicSocket...")
        self.socket = socket(AF_INET, SOCK_DGRAM)
        print("Socket created.")
        self.connection_id =random.randint(1 ,100)
        print(f"Generated connection ID: {self.connection_id}")
        self.num_pack_send=0
        self.dest_connection_id = None
        self.packetNumber = 0
        self.bufferSize = 9000
        print("Initializing quicSocket end...")

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
        print(f"Sent data: {data}")
        buffer, clientAddress = self.socket.recvfrom(self.bufferSize)
        buffer = quicPacket.unpack(buffer)
        if buffer.dest_connection_id != self.connection_id:
            return

        ## handle ACK

    def receive(self, buffer_size):
        """
        1. Receive data
        2. Send ACK
        :param buffer_size: The size of the buffer to use
        :return: The payload from the received packet or an empty list
        """
        try:
            buffer, clientAddress = self.socket.recvfrom(buffer_size)
            if not buffer:
                return []  # Handle unexpected empty buffer

            buffer = quicPacket.unpack(buffer)
            if buffer.dest_connection_id != self.connection_id:
                return []  # Return empty list if the packet is not meant for this connection

            # print(f"Received data: {buffer.payload}")
            # Send acknowledgment
            self.packetNumber += 1
            ack_packet = quicPacket(self.dest_connection_id, self.packetNumber, [])
            self.socket.sendto(ack_packet.pack(), clientAddress)

            return buffer.payload

        except Exception as e:
            print(f"Error receiving data: {e}")
            return []  # Return an empty list on error


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
