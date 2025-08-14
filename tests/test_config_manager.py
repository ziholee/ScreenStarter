import unittest
import os
import json

# We need to add the parent directory to the path to import main
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from monitor_selector.main import ConfigManager

class TestConfigManager(unittest.TestCase):
    def setUp(self):
        """Set up a temporary config file for testing."""
        # The ConfigManager expects the file to be in the root, so we create it there.
        self.config_path = 'config.json'
        # Ensure no old config file is present
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def tearDown(self):
        """Clean up the temporary config file."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_load_non_existent_config(self):
        """Test that loading a non-existent config returns an empty dict."""
        self.assertFalse(os.path.exists(self.config_path))
        config = ConfigManager.load_config()
        self.assertEqual(config, {})

    def test_save_and_load_config(self):
        """Test that saving and then loading a config works correctly."""
        sample_config = {
            "/usr/bin/firefox": 1,
            "C:\\Program Files\\app.exe": 0
        }
        ConfigManager.save_config(sample_config)
        self.assertTrue(os.path.exists(self.config_path))

        loaded_config = ConfigManager.load_config()
        self.assertEqual(loaded_config, sample_config)

    def test_load_invalid_json(self):
        """Test that loading a corrupt/invalid JSON file returns an empty dict."""
        with open(self.config_path, 'w') as f:
            f.write("{'invalid_json': True,}") # Invalid JSON with single quotes and trailing comma

        config = ConfigManager.load_config()
        self.assertEqual(config, {})

if __name__ == '__main__':
    unittest.main()
