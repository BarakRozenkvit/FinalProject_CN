import os
from file_buffer import BufferManager
from quic import quicSocket,ACK,quicPacket

SERVER_ADDRESS = ('', 12000)
BUFFER_SIZE= 2100

def main():
    cwd = os.getcwd() + "/Files"
    files_to_send = [os.path.join(cwd, f) for f in os.listdir(cwd) if
                 os.path.isfile(os.path.join(cwd, f))]

    print("Starting Server")
    server = quicSocket(BUFFER_SIZE)

    print("The server is binding to ", SERVER_ADDRESS)
    server.socket.bind(SERVER_ADDRESS)
    print("The server is ready to accept new incoming connections...")
    client_address = server.accept()
    print("The server connected to peer")

    buffer, client_address = server.receive()
    
    try:
        num_flows_requested = int(buffer.payload[1].stream_data)
    except:
        server.send(['F'],client_address,[]) # Send exit signal to client
        exit()

    print("Creating database of files to send...")
    buffer_manager = BufferManager(files_to_send[:num_flows_requested])
    buffer_manager.manage()

    while True:
        payload = buffer_manager.pack(BUFFER_SIZE- ACK.size - quicPacket.size)
        
        if not payload:  # Check if the payload is empty
            print("All data sent, sending exit signal to client.")
            server.send(['F'],client_address,[]) # Send exit signal to client
            buffer,client_address = server.receive()
            if 'A' in buffer.flags and 'F' in buffer.flags:
                break

        server.send(['D'],client_address, payload)
        buffer, client_address = server.receive()

    server.socket.close()
    print("Server socket closed. Transmission complete.")


if __name__ == '__main__':
    main()