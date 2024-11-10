from quic_statistics import Statistics
from quic import quicSocket, Stream

SERVER_ADDRESS = ('localhost', 12000)
BUFFER_SIZE = 2500
NUM_FLOWS = 5


def main():

    print("Starting Client")
    client = quicSocket(BUFFER_SIZE)

    client.connect(SERVER_ADDRESS)
    print("Client connected to server.")

    print("Sending Request for ", NUM_FLOWS," Files")
    client.send(['D','A'],SERVER_ADDRESS, [Stream(1,2,1,str(NUM_FLOWS))])

    statistics = Statistics()

    while True:
        buffer, server_address = client.receive()

        if 'F' in buffer.flags:
            client.send(['F','A'],server_address,[])
            break

        for item in buffer.payload:
            if isinstance(item, Stream):
                stream_id = item.stream_id
                statistics.add_stream(stream_id)
                statistics.update_stream(stream_id, len(item.stream_data),item.stream_data)

        client.send(['A'],server_address,[])

    print("Client Disconnecting")
    client.socket.close()
    statistics.calculate_statistics()

if __name__ == '__main__':
    main()
