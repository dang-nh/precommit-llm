"""
Tests for the config utilities.
"""
import os
import tempfile
import unittest
from unittest.mock import patch

import yaml

from llm_precommit.utils.config import load_config, should_analyze_file, create_default_config_file
from llm_precommit.constants import DEFAULT_API_KEY_ENV_VAR, DEFAULT_INCLUDE_EXTENSIONS, DEFAULT_EXCLUDE_PATTERNS


class TestConfig(unittest.TestCase):
    """Tests for configuration utilities."""

    def test_load_config_default(self):
        """Test that load_config returns default values when no config file exists."""
        with patch("os.path.isfile", return_value=False):
            config = load_config()
            self.assertEqual(config.get("api_key_env_var"), DEFAULT_API_KEY_ENV_VAR)
            self.assertEqual(config.get("include_extensions"), DEFAULT_INCLUDE_EXTENSIONS)
            self.assertEqual(config.get("exclude_patterns"), DEFAULT_EXCLUDE_PATTERNS)
            self.assertFalse(config.get("verbose"))
            self.assertFalse(config.get("check_all_files"))
            self.assertFalse(config.get("fail_on_issues"))

    def test_load_config_from_file(self):
        """Test loading config from a file."""
        test_config = {
            "api_key_env_var": "TEST_API_KEY",
            "verbose": True,
            "check_all_files": True,
            "fail_on_issues": True,
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
            yaml.dump(test_config, temp)
            temp_path = temp.name
        
        try:
            config = load_config(temp_path)
            self.assertEqual(config.get("api_key_env_var"), "TEST_API_KEY")
            self.assertTrue(config.get("verbose"))
            self.assertTrue(config.get("check_all_files"))
            self.assertTrue(config.get("fail_on_issues"))
        finally:
            os.unlink(temp_path)

    def test_should_analyze_file(self):
        """Test file filtering for analysis."""
        config = {
            "include_extensions": [".py", ".js"],
            "exclude_patterns": ["node_modules/", "test_*"],
            "max_file_size_kb": 100,
        }
        
        # Test file extension matching
        with patch("os.path.isfile", return_value=True), \
             patch("os.path.getsize", return_value=1024):  # 1KB
            self.assertTrue(should_analyze_file("file.py", config))
            self.assertTrue(should_analyze_file("file.js", config))
            self.assertFalse(should_analyze_file("file.txt", config))
        
        # Test exclude patterns
        with patch("os.path.isfile", return_value=True), \
             patch("os.path.getsize", return_value=1024):
            self.assertFalse(should_analyze_file("node_modules/file.js", config))
            self.assertFalse(should_analyze_file("test_file.py", config))
        
        # Test file size limit
        with patch("os.path.isfile", return_value=True), \
             patch("os.path.getsize", return_value=1024 * 200):  # 200KB
            self.assertFalse(should_analyze_file("file.py", config))


if __name__ == "__main__":
    unittest.main() 