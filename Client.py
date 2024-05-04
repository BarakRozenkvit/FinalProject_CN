import Statistics
from QUIC import *
from FileBuffer import BufferManager

SERVER_ADDRESS = ("localhost",12000)
BUFFER_SIZE = 20000

if __name__ == '__main__':
    print("Creating database of files to receive...")
    statictics = Statistics.Statistics()
    print("Creating socket...")
    client = quicSocket()
    print("try to connect to server...")
    client.connect(SERVER_ADDRESS)
    print("connected to server")
    client.send(SERVER_ADDRESS, "GET")

    bytesRecevied = 0
    string = ""
    while True:


        data = client.receive(BUFFER_SIZE)
        if (data == "EXIT"):
            break

        bytes = 0
        for dat in data:
            bytes+=len(dat.stream_data)
            string+=dat.stream_data
        bytesRecevied+=bytes

        statictics.unpack(data)

    print("Overall: %d" % bytesRecevied)
    f = open("Files/res.txt","w")
    f.write(string)
    f.close()
    client.socket.close()








