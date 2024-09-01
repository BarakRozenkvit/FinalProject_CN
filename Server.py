import sys
import time
from FileBuffer import BufferManager
from QUIC import quicSocket
from threading import Thread

SERVER_ADDRESS = ('', 12000)
BUFFER_SIZE = 9000

if __name__ == '__main__':
    print("Creating database of files to send...")
    buffer_manager = BufferManager(["Files/1.txt", "Files/2.txt","Files/3.txt", "Files/4.txt", "Files/5.txt"])
    manage_storage_thread = Thread(target=buffer_manager.manage, daemon=True)
    manage_storage_thread.start()

    print("Creating server socket...")
    server = quicSocket()

    print("The server is binding to ", SERVER_ADDRESS)
    server.socket.bind(SERVER_ADDRESS)
    print("The server is ready to accept new incoming connections.")
    clientAddress = server.accept(BUFFER_SIZE)
    print("The server connected to peer")

    while True:
        # Pack data into streams with a total payload size of up to 5000 bytes
        payload = buffer_manager.pack(5000)

        if not payload:  # Check if the payload is empty
            print("All data sent, sending exit signal to client.")
            server.send(clientAddress, ["EXIT"])  # Send exit signal to client
            break

        server.send(clientAddress, payload)
        # time.sleep(0.1)  # Adding a small delay to manage flow and avoid flooding the client

    server.socket.close()
    print("Server socket closed. Transmission complete.")
