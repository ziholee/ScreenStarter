import unittest
import os

# We need to add the parent directory to the path to import from monitor_selector
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from monitor_selector.os_specific import get_window_mover, WindowsWindowMover, MacWindowMover, LinuxWindowMover

from unittest.mock import patch

class TestOsSpecific(unittest.TestCase):

    @patch('sys.platform', 'win32')
    def test_get_mover_for_windows(self):
        """Test if the factory returns a WindowsWindowMover on win32."""
        mover = get_window_mover()
        self.assertIsInstance(mover, WindowsWindowMover)

    @patch('sys.platform', 'darwin')
    def test_get_mover_for_mac(self):
        """Test if the factory returns a MacWindowMover on darwin."""
        mover = get_window_mover()
        self.assertIsInstance(mover, MacWindowMover)

    @patch('sys.platform', 'linux')
    def test_get_mover_for_linux(self):
        """Test if the factory returns a LinuxWindowMover on linux."""
        mover = get_window_mover()
        self.assertIsInstance(mover, LinuxWindowMover)

    @patch('sys.platform', 'sunos') # An example of an unsupported OS
    def test_get_mover_for_unsupported_os(self):
        """Test if the factory raises an error for an unsupported OS."""
        with self.assertRaises(NotImplementedError):
            get_window_mover()

if __name__ == '__main__':
    unittest.main()
