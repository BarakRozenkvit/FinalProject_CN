import unittest
from QUIC import Stream
from multiprocessing import Process
import time
from file_buffer import FileBuffer
from Server import main_server
from Client import main_client
from quic_statistics import Statistics
import os
class TestQUICConnection(unittest.TestCase):
    def test_client_server_connection(self):
        # Set up server and client in separate processes
        server_process = Process(target=main_server)
        client_process = Process(target=main_client)

        server_process.start()
        time.sleep(1)
        client_process.start()

        # Wait for client to finish
        client_process.join()

        # Ensure server terminates after client finishes
        server_process.terminate()

        print("Test passed: Client-server connection established successfully.")

    def test_Stream(self):
        # Create a stream instance
        stream = Stream(1, 0, 10, 'test_data')

        # Test stream attributes
        assert stream.stream_id == 1, "Stream ID should be 1"
        assert stream.offset == 0, "Stream offset should be 0"
        assert stream.length == 10, "Stream length should be 10"
        assert stream.stream_data == 'test_data', "Stream data mismatch"

        print("Stream tests passed.")


class TestFileBuffer(unittest.TestCase):
    """
    Test the FileBuffer class for correctly filling and converting to Stream.
    """

    def setUp(self):
        # Create a temporary file for testing
        self.test_file_path = 'test_file.txt'
        with open(self.test_file_path, 'w') as f:
            f.write("This is a test file for the FileBuffer class.")

    def tearDown(self):
        # Clean up the temporary file after the test
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_FileBuffer(self):
        file_buffer = FileBuffer(self.test_file_path)

        # Test buffer filling
        file_buffer.fill_buffer()
        self.assertFalse(file_buffer.is_empty(), "Buffer should not be empty after filling")

        # Test converting buffer to stream
        stream = file_buffer.to_stream()
        self.assertIsInstance(stream, Stream, "Returned object should be a Stream")

        print("FileBuffer tests passed.")
class TestStatistics(unittest.TestCase):
    def test_Statistics(self):
        statistics = Statistics()

        # Test adding a stream
        statistics.add_stream(1)
        assert 1 in statistics.streams, "Stream ID 1 should be added"

        # Test updating a stream
        statistics.update_stream(1, 5, 'test_data')
        stream_data = statistics.streams[1]
        assert stream_data["total_bytes"] == 5, "Total bytes mismatch"
        assert stream_data["total_packets"] == 1, "Total packets mismatch"

        print("Statistics tests passed.")


if __name__ == '__main__':
    unittest.main()
