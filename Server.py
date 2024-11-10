import sys
import os
import time
from FileBuffer import BufferManager
from QUIC import quicSocket, Stream ,ACK
from threading import Thread

SERVER_ADDRESS = ('', 12000)
BUFFER_SIZE= 5000

def main():
    cwd = os.getcwd() + "/Files"
    files_to_send = [os.path.join(cwd, f) for f in os.listdir(cwd) if
                 os.path.isfile(os.path.join(cwd, f))]

    print("Creating server socket...")
    server = quicSocket(BUFFER_SIZE)

    print("The server is binding to ", SERVER_ADDRESS)
    server.socket.bind(SERVER_ADDRESS)
    print("The server is ready to accept new incoming connections.")
    clientAddress = server.accept()
    print("The server connected to peer")

    buffer, clientAddress = server.receive()
    try:
        num_flows_requested = int(buffer.payload[1].stream_data)
    except:
        print("Number of flows requested Invalid")
        exit()

    print("Creating database of files to send...")
    buffer_manager = BufferManager(files_to_send[:num_flows_requested])
    buffer_manager.manage()

    while True:
        # Pack data into streams with a total payload size of up to 5000 bytes
        payload = buffer_manager.pack(BUFFER_SIZE)
        print(f"Packed payload: {payload}")

        if not payload:  # Check if the payload is empty
            print("All data sent, sending exit signal to client.")
            info_stream = Stream(1, 2, 4, "EXIT")
            server.send(['D'],clientAddress, [info_stream])  # Send exit signal to client
            break

        server.send(['D'],clientAddress, payload)
        print("Sent payload to client.")

    server.socket.close()
    print("Server socket closed. Transmission complete.")


if __name__ == '__main__':
    main()