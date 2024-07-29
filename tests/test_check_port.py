import unittest
from unittest.mock import patch
import socket
from ollama.helpers import check_host

class TestCheckHost(unittest.TestCase):
    @patch('ollama.helpers.socket.socket')
    def test_host_open(self, mock_socket):
        # Mock the socket instance
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.return_value = 0

        self.assertTrue(check_host('127.0.0.1', 80))

    @patch('ollama.helpers.socket.socket')
    def test_host_closed(self, mock_socket):
        # Mock the socket instance
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.return_value = 1

        self.assertFalse(check_host('127.0.0.1', 80))

    @patch('ollama.helpers.socket.socket')
    def test_timeout(self, mock_socket):
        # Mock the socket instance
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.side_effect = socket.timeout

        self.assertFalse(check_host('127.0.0.1', 80))

    def test_no_host(self):
        with self.assertRaises(TypeError):
            check_host(None, 80)

    def test_invalid_host(self):
        with self.assertRaises(ValueError):
            check_host('127.0.0.1', -1)

        with self.assertRaises(ValueError):
            check_host('127.0.0.1', 65536)

    @patch('ollama.helpers.socket.socket')
    def test_socket_error(self, mock_socket):
        # Mock the socket instance to raise an error
        mock_instance = mock_socket.return_value
        mock_instance.connect_ex.side_effect = socket.error

        self.assertFalse(check_host('127.0.0.1', 80))

if __name__ == '__main__':
    unittest.main()
