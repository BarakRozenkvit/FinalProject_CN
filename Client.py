import random
import time
from QUIC import quicSocket
from QUIC import Stream
from FileBuffer import BufferManager
import Statistics

SERVER_ADDRESS = ('localhost', 12000)
BUFFER_SIZE = 9000


def start_client(num_flows):
    print(f"Starting client with {num_flows} flows...")
    client = quicSocket()
    client.connect(SERVER_ADDRESS)
    print("Client connected to server.")

    packet_size = random.randint(1000, 2000)  # Random packet size between 1000 and 2000 bytes

    bytes_received = 0
    all_streams_data = []  # For storing the received stream data
    statistics = Statistics.Statistics()

    while True:
        data = client.receive(BUFFER_SIZE)
        if isinstance(data, list) and len(data) == 1 and data[0] == "EXIT":
            print("Exit signal received. Closing connection.")
            break

        if isinstance(data, list):
            for stream in data:
                if isinstance(stream, Stream):
                    bytes_received += len(stream.stream_data)
                    all_streams_data.append(stream)
                    statistics.unpack([stream])

    print(f"Overall bytes received: {bytes_received}")

    statistics.hagit_check()


    print("Statistics per stream:")
    for stream in statistics.streams:
        print(f"Stream ID: {stream.stream_id}, Data length: {len(stream.stream_data)}")

    client.socket.close()


if __name__ == '__main__':
    # for num_flows in range(1, 11):
    start_client(1)
    time.sleep(2)  # Wait between tests
