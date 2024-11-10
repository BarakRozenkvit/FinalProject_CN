import random
import time

from nacl.bindings import crypto_kx_SEED_BYTES

from QUIC import quicSocket, Stream
from FileBuffer import BufferManager
import Statistics

SERVER_ADDRESS = ('localhost', 12000)
BUFFER_SIZE = 5000
NUM_FLOWS = 1


def main(num_flows):

    print(f"Starting client with {num_flows} flows...")
    client = quicSocket(BUFFER_SIZE)
    client.connect(SERVER_ADDRESS)
    print("Client connected to server.")

    # Send the number of flows requested to the server
    info_stream = Stream(1,2,1,str(num_flows))
    client.send(['D','A'],SERVER_ADDRESS, [info_stream])
    print(f"Sent number of flows {num_flows} to server.")

    bytes_received = 0
    all_streams_data = []  # For storing the received stream data
    statistics = Statistics.Statistics()
    progress = True

    while progress:
        buffer, serverAddress = client.receive()

        if 'F' in buffer.flags:
            client.send(['F','A'],serverAddress)
            progress = False
            break
        for item in buffer.payload:
            if isinstance(item, Stream):
                stream_id = item.stream_id
                statistics.add_stream(stream_id)
                statistics.update_stream(stream_id, len(item.stream_data),item.stream_data)
            
        client.send(['A'],serverAddress,[])
    
    client.socket.close()
    print("Client socket closed.")
    statistics.calculate_statistics()



if __name__ == '__main__':
    main(NUM_FLOWS)  # Adjust the number of flows as needed