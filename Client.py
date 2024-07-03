import Statistics
from QUIC import quicSocket
from FileBuffer import BufferManager

SERVER_ADDRESS = ("localhost",4444)
BUFFER_SIZE = 20000

if __name__ == '__main__':

    print("Creating socket...")
    client = quicSocket()
    print("try to connect to server...")
    client.connect(SERVER_ADDRESS)
    print("connected to server")

    while True:

        data = client.receive(BUFFER_SIZE)








