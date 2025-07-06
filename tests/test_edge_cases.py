import os
import pytest
from configence import Configence, configence
from decouple import undefined


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_undefined_value_handling(self):
        """Test handling of undefined values."""
        configence = Configence(is_model=False)
        
        # Test with undefined default
        with pytest.raises(Exception):  # Should raise when no env var and no default
            configence.str("NONEXISTENT_KEY")
        
        # Test with explicit undefined
        with pytest.raises(Exception):
            configence.str("NONEXISTENT_KEY", undefined)

    def test_empty_string_handling(self):
        """Test handling of empty strings."""
        configence = Configence(is_model=False)
        
        # Test empty string as default
        result = configence.str("EMPTY_KEY", "")
        assert result == ""
        
        # Test empty string from environment
        os.environ["EMPTY_KEY"] = ""
        result = configence.str("EMPTY_KEY", "default")
        assert result == ""
        
        # Cleanup
        del os.environ["EMPTY_KEY"]

    def test_none_value_handling(self):
        """Test handling of None values."""
        configence = Configence(is_model=False)
        
        # Test None as default
        result = configence.str("NONE_KEY", None)
        assert result is None
        
        # Test "None" string from environment
        os.environ["NONE_KEY"] = "None"
        result = configence.str("NONE_KEY", "default")
        assert result == "None"
        
        # Cleanup
        del os.environ["NONE_KEY"]

    def test_special_characters_in_keys(self):
        """Test handling of special characters in environment variable keys."""
        configence = Configence(is_model=False)
        
        # Test with special characters
        os.environ["SPECIAL_KEY_123"] = "special_value"
        result = configence.str("SPECIAL_KEY_123", "default")
        assert result == "special_value"
        
        # Cleanup
        del os.environ["SPECIAL_KEY_123"]

    def test_very_long_values(self):
        """Test handling of very long string values."""
        configence = Configence(is_model=False)
        
        long_value = "x" * 10000
        os.environ["LONG_KEY"] = long_value
        result = configence.str("LONG_KEY", "default")
        assert result == long_value
        
        # Cleanup
        del os.environ["LONG_KEY"]

    def test_unicode_values(self):
        """Test handling of unicode values."""
        configence = Configence(is_model=False)
        
        unicode_value = "🚀 火箭 🚀"
        os.environ["UNICODE_KEY"] = unicode_value
        result = configence.str("UNICODE_KEY", "default")
        assert result == unicode_value
        
        # Cleanup
        del os.environ["UNICODE_KEY"]

    def test_boolean_edge_cases(self):
        """Test boolean parsing edge cases."""
        configence = Configence(is_model=False)
        
        # Test various boolean representations
        test_cases = [
            ("TRUE", True),
            ("True", True),
            ("true", True),
            ("1", True),
            ("FALSE", False),
            ("False", False),
            ("false", False),
            ("0", False),
        ]
        
        for env_value, expected in test_cases:
            os.environ["BOOL_KEY"] = env_value
            result = configence.bool("BOOL_KEY", False)
            assert result == expected
            del os.environ["BOOL_KEY"]

    def test_list_edge_cases(self):
        """Test list parsing edge cases."""
        configence = Configence(is_model=False)
        
        # Test empty list
        os.environ["EMPTY_LIST"] = ""
        result = configence.list("EMPTY_LIST", ["default"])
        assert result == []
        
        # Test single item
        os.environ["SINGLE_ITEM"] = "item1"
        result = configence.list("SINGLE_ITEM", [])
        assert result == ["item1"]
        
        # Test custom delimiter
        os.environ["CUSTOM_DELIM"] = "a;b;c"
        result = configence.list("CUSTOM_DELIM", [], delimiter=";")
        assert result == ["a", "b", "c"]
        
        # Cleanup
        del os.environ["EMPTY_LIST"]
        del os.environ["SINGLE_ITEM"]
        del os.environ["CUSTOM_DELIM"]

    def test_model_edge_cases(self):
        """Test model parsing edge cases."""
        from pydantic import BaseModel
        
        class SimpleModel(BaseModel):
            name: str
            value: int

        configence = Configence(is_model=False)
        
        # Test with malformed JSON
        os.environ["MALFORMED_JSON"] = "{invalid json}"
        
        # Should raise an exception for malformed JSON
        default_data = {"name": "default", "value": 42}
        with pytest.raises(Exception):
            result = configence.model("MALFORMED_JSON", SimpleModel, default_data)
        
        # Cleanup
        del os.environ["MALFORMED_JSON"]

    def test_delayed_loading_edge_cases(self):
        """Test delayed loading edge cases."""
        class MyModel(Configence):
            BASE_VALUE = configence.str("BASE_VALUE", "base")
            # Test with existing dependency
            EXISTING_DEP = configence.delay("{BASE_VALUE}")
            # Test with missing dependency - should use the string as-is
            MISSING_DEP = configence.delay("{NONEXISTENT_VALUE}")

        my_config = MyModel()
        
        # Should handle existing dependency
        assert my_config.EXISTING_DEP == "base"
        
        # Should handle missing dependency gracefully by keeping the string as-is
        assert my_config.MISSING_DEP == "{NONEXISTENT_VALUE}"

    def test_prefix_edge_cases(self):
        """Test prefix edge cases."""
        # Test with empty prefix
        configence = Configence(prefix="", is_model=False)
        os.environ["KEY"] = "value"
        result = configence.str("KEY", "default")
        assert result == "value"
        
        # Test with None prefix
        configence = Configence(prefix=None, is_model=False)
        result = configence.str("KEY", "default")
        assert result == "value"
        
        # Cleanup
        del os.environ["KEY"]

    def test_config_model_inheritance(self):
        """Test Configence model inheritance."""
        class BaseConfig(Configence):
            BASE_KEY = configence.str("BASE_KEY", "base_value")

        class DerivedConfig(BaseConfig):
            DERIVED_KEY = configence.str("DERIVED_KEY", "derived_value")

        derived = DerivedConfig()
        
        assert derived.BASE_KEY == "base_value"
        assert derived.DERIVED_KEY == "derived_value"
        
        # Test with environment variables
        os.environ["BASE_KEY"] = "env_base"
        os.environ["DERIVED_KEY"] = "env_derived"
        
        derived = DerivedConfig()
        assert derived.BASE_KEY == "env_base"
        assert derived.DERIVED_KEY == "env_derived"
        
        # Cleanup
        del os.environ["BASE_KEY"]
        del os.environ["DERIVED_KEY"]

    def test_attribute_setting(self):
        """Test setting attributes on config models."""
        class MyModel(Configence):
            MY_KEY = configence.str("MY_KEY", "default")

        my_config = MyModel()
        
        # Test setting attribute
        my_config.MY_KEY = "new_value"
        assert my_config.MY_KEY == "new_value"
        
        # Test that internal entry is also updated
        assert my_config._entries["MY_KEY"].value == "new_value"

    def test_on_load_override(self):
        """Test overriding on_load method."""
        class MyModel(Configence):
            BASE_VALUE = configence.str("BASE_VALUE", "base")
            
            def on_load(self):
                self.DYNAMIC_VALUE = "dynamic"

        my_config = MyModel()
        
        assert my_config.BASE_VALUE == "base"
        assert my_config.DYNAMIC_VALUE == "dynamic" 