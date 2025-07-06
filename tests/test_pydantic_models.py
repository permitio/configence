import os
import pytest
from pydantic import BaseModel, Field
from typing import List
from configence import Configence, configence


class TestPydanticModels:
    """Test Pydantic model integration."""

    def test_pydantic_model_config(self):
        """Test configuration with Pydantic models."""
        class MyPydantic(BaseModel):
            entries: List[int] = Field(..., description="list of integers")
            name: str

        configence = Configence(is_model=False)
        
        # Test with default value
        default_data = {
            "entries": [1, 3, 43, 5, 7],
            "name": "Moses"
        }
        result = configence.model("JSON", MyPydantic, default_data)
        
        assert isinstance(result, MyPydantic)
        assert result.entries == [1, 3, 43, 5, 7]
        assert result.name == "Moses"

    def test_pydantic_model_from_env(self):
        """Test Pydantic model parsing from environment variable."""
        class MyPydantic(BaseModel):
            entries: List[int] = Field(..., description="list of integers")
            name: str

        configence = Configence(is_model=False)
        
        # Test with environment variable containing JSON
        env_data = '{"entries": [2, 4, 6, 8], "name": "Vegeta"}'
        os.environ["JSON"] = env_data
        
        result = configence.model("JSON", MyPydantic, {
            "entries": [1, 3, 43, 5, 7],
            "name": "Moses"
        })
        
        assert isinstance(result, MyPydantic)
        assert result.entries == [2, 4, 6, 8]
        assert result.name == "Vegeta"
        
        # Cleanup
        del os.environ["JSON"]

    def test_pydantic_model_in_config_model(self):
        """Test Pydantic model within a Configence model class."""
        class MyPydantic(BaseModel):
            entries: List[int] = Field(..., description="list of integers")
            name: str

        class MyModel(Configence):
            JSON = configence.model(
                "JSON",
                MyPydantic,
                {
                    "entries": [1, 3, 43, 5, 7],
                    "name": "Moses"
                }
            )

        my_config = MyModel()
        assert isinstance(my_config.JSON, MyPydantic)
        assert my_config.JSON.entries == [1, 3, 43, 5, 7]
        assert my_config.JSON.name == "Moses"

    def test_pydantic_model_validation_error(self):
        """Test Pydantic model validation error handling."""
        class MyPydantic(BaseModel):
            entries: List[int] = Field(..., description="list of integers")
            name: str

        configence = Configence(is_model=False)
        
        # Test with invalid JSON in environment variable
        os.environ["JSON"] = '{"invalid": "data"}'
        
        # Should fall back to default when validation fails
        default_data = {
            "entries": [1, 3, 43, 5, 7],
            "name": "Moses"
        }
        
        # This should raise a validation error, so we test that it does
        with pytest.raises(Exception):
            result = configence.model("JSON", MyPydantic, default_data)
        
        # Cleanup
        del os.environ["JSON"]

    def test_pydantic_model_with_enum(self):
        """Test Pydantic model with enum fields."""
        from enum import Enum

        class PowerLevel(Enum):
            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"

        class Character(BaseModel):
            name: str
            power_level: PowerLevel

        configence = Configence(is_model=False)
        
        # Test with default value
        default_data = {
            "name": "Goku",
            "power_level": "high"
        }
        result = configence.model("CHARACTER", Character, default_data)
        
        assert isinstance(result, Character)
        assert result.name == "Goku"
        assert result.power_level == PowerLevel.HIGH

    def test_pydantic_model_with_nested_models(self):
        """Test Pydantic model with nested models."""
        class Address(BaseModel):
            street: str
            city: str

        class Person(BaseModel):
            name: str
            age: int
            address: Address

        configence = Configence(is_model=False)
        
        # Test with default value
        default_data = {
            "name": "Goku",
            "age": 30,
            "address": {
                "street": "Kame House",
                "city": "Kame Island"
            }
        }
        result = configence.model("PERSON", Person, default_data)
        
        assert isinstance(result, Person)
        assert result.name == "Goku"
        assert result.age == 30
        assert isinstance(result.address, Address)
        assert result.address.street == "Kame House"
        assert result.address.city == "Kame Island" 