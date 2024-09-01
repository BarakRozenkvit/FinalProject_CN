import time
import threading
from QUIC import quicSocket
import socket
# Constants
SERVER_ADDRESS = ('localhost', 12000)
BUFFER_SIZE = 9000
NUM_FLOWS_LIST = range(1, 11)  # Testing from 1 to 10 flows


def start_server():
    server = quicSocket()
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.socket.bind(SERVER_ADDRESS)
    try:
        while True:
            print("Waiting for data...")
            result = server.receive(BUFFER_SIZE)
            print(f"Received data: {result}")
            if not result:
                continue

            if isinstance(result, list) and len(result) == 1 and result[0] == "EXIT":
                print("Exit signal received. Closing connection.")
                break

    except Exception as e:
        print(f"Server encountered an error: {e}")
    finally:
        server.socket.close()
        print("Server socket closed.")

def start_client(num_flows):
    print("Starting client with", num_flows, "flows...")
    client = quicSocket()
    client.connect(SERVER_ADDRESS)
    print("Client connected to server.")

    for i in range(num_flows):
        # Generate random data for each flow
        data = b"Data with size" + bytes(str(i + 1), 'utf-8')
        print(f"Sending data for flow {i + 1}: {data}")
        client.send(SERVER_ADDRESS, data)
        print(f"Sent data for stream {i + 1} to server.")

    client.send(SERVER_ADDRESS, b"EXIT")  # Send EXIT as bytes
    print("Sent exit signal to server.")
    client.socket.close()


if __name__ == "__main__":
    for num_flows in NUM_FLOWS_LIST:
        print(f"Running test with {num_flows} flows...")
        server_thread = threading.Thread(target=start_server, daemon=True)
        client_thread = threading.Thread(target=start_client, args=(num_flows,), daemon=True)

        server_thread.start()
        time.sleep(1)  # Ensure server starts before client
        client_thread.start()

        client_thread.join()
        server_thread.join()
        print("Test with", num_flows, "flows completed.\n")
