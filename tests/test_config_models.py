import os
import pytest
from configence import Configence, configence


class TestConfigModels:
    """Test Configence models functionality."""

    def test_basic_config_model(self):
        """Test basic Configence model class."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)
            MY_CONST = "Bulma!"

        # Test default values
        my_config = MyModel()
        assert my_config.MY_HERO == 'Son Goku'
        assert my_config.POWER_LEVEL == 9001
        assert my_config.MY_CONST == "Bulma!"

        # Test with environment variables
        os.environ["MY_HERO"] = "Vegeta"
        os.environ["POWER_LEVEL"] = "8000"
        
        my_config = MyModel()
        assert my_config.MY_HERO == "Vegeta"
        assert my_config.POWER_LEVEL == 8000
        
        # Cleanup
        del os.environ["MY_HERO"]
        del os.environ["POWER_LEVEL"]

    def test_delayed_loading_string(self):
        """Test delayed loading with string interpolation."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)
            SHOUT = configence.delay("{MY_HERO} is over {POWER_LEVEL}")

        my_config = MyModel()
        assert my_config.SHOUT == "Son Goku is over 9001"

        # Test with environment variables
        os.environ["MY_HERO"] = "Vegeta"
        os.environ["POWER_LEVEL"] = "8000"
        
        my_config = MyModel()
        assert my_config.SHOUT == "Vegeta is over 8000"
        
        # Cleanup
        del os.environ["MY_HERO"]
        del os.environ["POWER_LEVEL"]

    def test_delayed_loading_function(self):
        """Test delayed loading with function."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)
            SHOUT = configence.delay("{MY_HERO} is over {POWER_LEVEL}")
            # Test with a simple delayed function
            EVENTS = configence.delay(lambda MY_HERO="", SHOUT="": [MY_HERO, SHOUT])

        my_config = MyModel()
        expected_events = ["Son Goku", "Son Goku is over 9001"]
        assert my_config.EVENTS == expected_events

    def test_delayed_loading_whole_entry(self):
        """Test delayed loading with whole entry."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)
            SHOUT = configence.delay("{MY_HERO} is over {POWER_LEVEL}")
            # Test with a simple boolean check
            HAS_LONG_SHOUT = configence.delay(lambda SHOUT="": len(SHOUT) > 12)

        my_config = MyModel()
        # "Son Goku is over 9001" has length 22, so should be True
        assert my_config.HAS_LONG_SHOUT is True

        # Test with shorter shout
        os.environ["MY_HERO"] = "Goku"
        os.environ["POWER_LEVEL"] = "100"
        
        my_config = MyModel()
        # "Goku is over 100" has length 15, so should be True
        assert my_config.HAS_LONG_SHOUT is True
        
        # Cleanup
        del os.environ["MY_HERO"]
        del os.environ["POWER_LEVEL"]

    def test_model_with_prefix(self):
        """Test Configence model with prefix."""
        class MyModel(Configence):
            def __init__(self):
                super().__init__(prefix="NEW_")
            
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)

        # Test with prefixed environment variables
        os.environ["NEW_MY_HERO"] = "Gohan"
        os.environ["NEW_POWER_LEVEL"] = "5000"
        
        my_config = MyModel()
        assert my_config.MY_HERO == "Gohan"
        assert my_config.POWER_LEVEL == 5000
        
        # Cleanup
        del os.environ["NEW_MY_HERO"]
        del os.environ["NEW_POWER_LEVEL"]

    def test_model_repr(self):
        """Test model representation."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)

        my_config = MyModel()
        repr_str = repr(my_config)
        
        # Should contain JSON representation of the config
        assert "MY_HERO" in repr_str
        assert "POWER_LEVEL" in repr_str
        assert "Son Goku" in repr_str
        assert "9001" in repr_str

    def test_model_debug_repr(self):
        """Test model debug representation."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)

        my_config = MyModel()
        debug_repr = my_config.debug_repr()
        
        # Should contain class name and formatted output
        assert "MyModel(Configence):" in debug_repr
        assert "MY_HERO" in debug_repr
        assert "POWER_LEVEL" in debug_repr 