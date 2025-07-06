import os
import pytest
from configence import Configence


class TestBasicConfig:
    """Test basic configuration functionality."""

    def test_string_config(self):
        """Test string configuration parsing."""
        configence = Configence(is_model=False)
        
        # Test with default value
        result = configence.str("MY_HERO", 'Son Goku')
        assert result == 'Son Goku'
        
        # Test with environment variable
        os.environ["MY_HERO"] = "Vegeta"
        result = configence.str("MY_HERO", 'Son Goku')
        assert result == 'Vegeta'
        
        # Cleanup
        del os.environ["MY_HERO"]

    def test_int_config(self):
        """Test integer configuration parsing."""
        configence = Configence(is_model=False)
        
        # Test with default value
        result = configence.int("POWER_LEVEL", 9001)
        assert result == 9001
        
        # Test with environment variable
        os.environ["POWER_LEVEL"] = "8000"
        result = configence.int("POWER_LEVEL", 9001)
        assert result == 8000
        
        # Cleanup
        del os.environ["POWER_LEVEL"]

    def test_bool_config(self):
        """Test boolean configuration parsing."""
        configence = Configence(is_model=False)
        
        # Test with default value
        result = configence.bool("IS_STRONG", True)
        assert result is True
        
        # Test with environment variable
        os.environ["IS_STRONG"] = "false"
        result = configence.bool("IS_STRONG", True)
        assert result is False
        
        # Test with "1" and "0"
        os.environ["IS_STRONG"] = "1"
        result = configence.bool("IS_STRONG", False)
        assert result is True
        
        os.environ["IS_STRONG"] = "0"
        result = configence.bool("IS_STRONG", True)
        assert result is False
        
        # Cleanup
        del os.environ["IS_STRONG"]

    def test_float_config(self):
        """Test float configuration parsing."""
        configence = Configence(is_model=False)
        
        # Test with default value
        result = configence.float("SPEED", 3.14)
        assert result == 3.14
        
        # Test with environment variable
        os.environ["SPEED"] = "2.718"
        result = configence.float("SPEED", 3.14)
        assert result == 2.718
        
        # Cleanup
        del os.environ["SPEED"]

    def test_list_config(self):
        """Test list configuration parsing."""
        configence = Configence(is_model=False)
        
        # Test with default value
        result = configence.list("EVENTS", ["event1", "event2"])
        assert result == ["event1", "event2"]
        
        # Test with environment variable
        os.environ["EVENTS"] = "event3,event4,event5"
        result = configence.list("EVENTS", ["event1", "event2"])
        assert result == ["event3", "event4", "event5"]
        
        # Cleanup
        del os.environ["EVENTS"]

    def test_prefix_config(self):
        """Test configuration with prefix."""
        configence = Configence(prefix="NEW_", is_model=False)
        
        # Test that prefix is applied
        os.environ["NEW_MY_HERO"] = "Gohan"
        result = configence.str("MY_HERO", 'Son Goku')
        assert result == 'Gohan'
        
        # Test that non-prefixed env var is ignored
        os.environ["MY_HERO"] = "Vegeta"
        result = configence.str("MY_HERO", 'Son Goku')
        assert result == 'Gohan'  # Should still use prefixed value
        
        # Cleanup
        del os.environ["NEW_MY_HERO"]
        del os.environ["MY_HERO"] 