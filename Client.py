import random
import time
from turtledemo.penrose import start

from QUIC import quicSocket, Stream
from FileBuffer import BufferManager
import Statistics

SERVER_ADDRESS = ('localhost', 12000)
BUFFER_SIZE = 9000
NUM_FLOWS = 3


def main(num_flows):

    print(f"Starting client with {num_flows} flows...")
    client = quicSocket()
    client.connect(SERVER_ADDRESS)
    print("Client connected to server.")

    # Send the number of flows requested to the server
    client.send(SERVER_ADDRESS, [str(num_flows)])
    print(f"Sent number of flows {num_flows} to server.")

    bytes_received = 0
    all_streams_data = []  # For storing the received stream data
    statistics = Statistics.Statistics()

    while True:
        data = client.receive(BUFFER_SIZE)
        if isinstance(data, list) and len(data) == 1 and data[0] == "EXIT":
            print("Exit signal received. Closing connection.")
            break

        for item in data:
            if isinstance(item, Stream):
                stream_id = item.stream_id
                statistics.add_stream(stream_id)
                statistics.update_stream(stream_id, len(item.stream_data),item.stream_data)

    client.socket.close()
    print("Client socket closed.")
    statistics.calculate_statistics()



if __name__ == '__main__':
    main(NUM_FLOWS)  # Adjust the number of flows as needed