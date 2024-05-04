import sys
import time

from FileBuffer import BufferManager
from QUIC import quicSocket
from threading import Thread

SERVER_ADDRESS = ('',12000)
BUFFER_SIZE = 9000

if __name__ == '__main__':
    print("Creating database of files to send...")
    buffer_manager = BufferManager(["Files/1.txt", "Files/2.txt","Files/3.txt", "Files/4.txt", "Files/5.txt"])
    manage_storage_thread = Thread(target=buffer_manager.manage,daemon=True)
    manage_storage_thread.start()

    print("Creating server socket...")
    server = quicSocket()

    print("The server is binding to ", SERVER_ADDRESS)
    server.socket.bind(SERVER_ADDRESS)
    print("The sever is ready to accept new incoming connections.")
    clientAddress = server.accept(BUFFER_SIZE)
    print("The server connceted to peer")

    data = server.receive(BUFFER_SIZE)
    if (data != "GET"):
        print("unrecognized request")
        exit(1)

    res = 0
    while True:

        payload = buffer_manager.pack(5000)

        if(payload == []):
            server.send(clientAddress,"EXIT")
            break

        server.send(clientAddress,payload)

    print(res)
    server.socket.close()















