import pytest
from unittest.mock import patch, MagicMock
from configence import Configence, configence
from typer import Typer


class TestCLIIntegration:
    """Test CLI integration functionality."""

    def test_get_cli_object(self):
        """Test getting CLI object from Configence model."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)

        my_config = MyModel()
        cli_object = my_config.get_cli_object()
        
        # Should return a click group object
        assert hasattr(cli_object, 'commands')
        assert hasattr(cli_object, 'params')

    def test_get_cli_object_with_multiple_configs(self):
        """Test getting CLI object with multiple config objects."""
        class Model1(Configence):
            HERO = configence.str("HERO", 'Goku')

        class Model2(Configence):
            POWER = configence.int("POWER", 9001)

        config1 = Model1()
        config2 = Model2()
        
        cli_object = config1.get_cli_object([config2])
        
        # Should return a click group object
        assert hasattr(cli_object, 'commands')
        assert hasattr(cli_object, 'params')

    def test_get_cli_object_with_typer_app(self):
        """Test getting CLI object with typer app."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')

        my_config = MyModel()
        
        # Create a mock typer app
        typer_app = Typer()
        
        @typer_app.command()
        def test_command():
            return "test"
        
        cli_object = my_config.get_cli_object(typer_app=typer_app)
        
        # Should return a click group object
        assert hasattr(cli_object, 'commands')
        assert hasattr(cli_object, 'params')

    def test_cli_method(self):
        """Test the cli() method."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')

        my_config = MyModel()
        
        # Mock the get_cli_object method to avoid actual CLI execution
        with patch.object(my_config, 'get_cli_object') as mock_get_cli:
            mock_cli = MagicMock()
            mock_get_cli.return_value = mock_cli
            
            my_config.cli()
            
            # Should call get_cli_object and then call the result
            mock_get_cli.assert_called_once()
            mock_cli.assert_called_once()

    def test_cli_with_help(self):
        """Test CLI with help text."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')

        my_config = MyModel()
        
        help_text = "Test help text"
        cli_object = my_config.get_cli_object(help=help_text)
        
        # Should return a click group object
        assert hasattr(cli_object, 'commands')
        assert hasattr(cli_object, 'params')

    def test_cli_with_on_start_callback(self):
        """Test CLI with on_start callback."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')

        my_config = MyModel()
        
        callback_called = False
        
        def on_start(ctx, **kwargs):
            nonlocal callback_called
            callback_called = True
        
        cli_object = my_config.get_cli_object(on_start=on_start)
        
        # Should return a click group object
        assert hasattr(cli_object, 'commands')
        assert hasattr(cli_object, 'params')

    def test_config_entry_cli_options(self):
        """Test that config entries have proper CLI option kwargs."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku', description="The hero name")
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001, description="Power level")

        my_config = MyModel()
        
        # Check that entries have CLI option kwargs
        hero_entry = my_config._entries["MY_HERO"]
        power_entry = my_config._entries["POWER_LEVEL"]
        
        hero_kwargs = hero_entry.get_cli_option_kwargs()
        power_kwargs = power_entry.get_cli_option_kwargs()
        
        assert "help" in hero_kwargs
        assert hero_kwargs["help"] == "The hero name"
        assert "help" in power_kwargs
        assert power_kwargs["help"] == "Power level"
        assert "default" in hero_kwargs
        assert "default" in power_kwargs

    def test_config_entry_with_flags(self):
        """Test config entries with CLI flags."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku', flags=["-h", "--hero"])

        my_config = MyModel()
        hero_entry = my_config._entries["MY_HERO"]
        
        # Check that flags are set
        assert hero_entry.flags == ["-h", "--hero"]

    def test_config_entry_cli_type(self):
        """Test config entry CLI type handling."""
        class MyModel(Configence):
            MY_HERO = configence.str("MY_HERO", 'Son Goku')
            POWER_LEVEL = configence.int("POWER_LEVEL", 9001)
            IS_STRONG = configence.bool("IS_STRONG", True)

        my_config = MyModel()
        
        # Check CLI types
        hero_entry = my_config._entries["MY_HERO"]
        power_entry = my_config._entries["POWER_LEVEL"]
        bool_entry = my_config._entries["IS_STRONG"]
        
        assert hero_entry.get_cli_type() == str
        assert power_entry.get_cli_type() == int
        assert bool_entry.get_cli_type() == bool 