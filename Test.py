import unittest
import time
import random
from threading import Thread
from Client1 import start_client
from Server1 import BUFFER_SIZE, SERVER_ADDRESS
from QUIC import quicSocket, Stream
from FileBuffer import BufferManager
import os


class TestQUIC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This method will be run once before any test methods are executed
        cls.server_thread = Thread(target=cls.run_server, daemon=True)
        cls.server_thread.start()
        time.sleep(2)  # Allow time for server to start up

    @classmethod
    def tearDownClass(cls):
        # Ensure server is stopped
        cls.server_running = False
        cls.server_thread.join()

    @classmethod
    def run_server(cls):
        # This method runs the server in a separate thread
        from Server1 import BUFFER_SIZE, SERVER_ADDRESS, quicSocket, BufferManager
        cls.server_running = True
        print("Starting server...")
        buffer_manager = BufferManager(["Files/1.txt", "Files/2.txt", "Files/4.txt", "Files/5.txt"])
        manage_storage_thread = Thread(target=buffer_manager.manage, daemon=True)
        manage_storage_thread.start()

        server = quicSocket()
        server.socket.bind(SERVER_ADDRESS)
        client_address = server.accept(BUFFER_SIZE)

        while cls.server_running:
            payload = buffer_manager.pack(5000)
            if not payload:
                server.send(client_address, ["EXIT"])
                break
            server.send(client_address, payload)
            time.sleep(0.1)  # Small delay to manage flow

        server.socket.close()
        print("Server closed.")

    def test_client_receives_data(self):
        num_flows = 1  # Adjust number of flows for testing
        print(f"Testing with {num_flows} flows...")
        start_client(num_flows)

        # Verify the file received matches expected content
        for i in range(1, 5):
            server_file = f"Files/{i}.txt"
            client_file = f"Files/res.txt"

            if os.path.exists(server_file):
                with open(server_file, 'rb') as f:
                    server_data = f.read()

                if os.path.exists(client_file):
                    with open(client_file, 'rb') as f:
                        client_data = f.read()

                    self.assertEqual(server_data, client_data, f"Data mismatch for file {i}.txt")

    def test_client_receives_exit_signal(self):
        num_flows = 1  # Adjust number of flows for testing
        print(f"Testing exit signal with {num_flows} flows...")
        start_client(num_flows)

        # You can add specific checks for exit signal if necessary


if __name__ == '__main__':
    unittest.main()
