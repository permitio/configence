# Configence

Easy Python configuration interface built on top of python-decouple and click / typer.
Adding typing support and parsing with Pydantic and Enum.
Combine config values from .env, .ini, env-vars, and cli options
(Override order: .env < .ini < env-vars < cli)


## Simple config values


```python
from configence import Configence

# init confi as simple parser (Without model class)
configence = Configence(is_model=False)

# parse a string value from env-var, or '.env' '.ini' files
# MY_HERO will contain a string read from env, or the default - 'Son Goku'
MY_HERO = configence.str("MY_HERO", 'Son Goku')

# parse an int
POWER_LEVEL = configence.int("POWER_LEVEL", 9001, description="The scouter power reading")

# parse a pydantic model
# you can pass a valid JSON to the envvar

# define model
from pydantic import BaseModel
class MyPydantic(BaseModel):
    entries: List[int] = Field(..., description="list of integers")
    name: str
# parse the model from JSON passed to env-var (or default)
JSON = configence.model(
    "JSON",
    MyPydantic,
    {
        "entries":[ 1,3,43,5,7],
        "name": "Moses"
    }
)
```
### Add prefix to env vars
```python
from configence import Configence

# init confi as simple parser (Without model class)
# And with Prefix
configence = Configence(prefix="NEW_" is_model=False)

# parse a string value from env-var, or '.env' '.ini' files
# instead of loading the envar MY_HERO - will read from NEW_MY_HERO (due to prefix)
MY_HERO = configence.str("MY_HERO", 'Son Goku')
```

## Configence models
For more advanced parsing (e.g delayed loading), separating into groups, configence use configence models  (classes that derive from Configence and have value members)
The values are only loaded when the class is initialized.

```python
from configence import Configence, configence

class MyModel(Configence):
    # parse values
    MY_HERO = configence.str("MY_HERO", 'Son Goku')
    POWER_LEVEL = configence.int("POWER_LEVEL", 9001)
    # mix in real consts
    MY_CONST = "Bulma!"

# get the parsed values into an object
# can also apply prefix here
my_config = MyModel()
```

### Delayed loading
When you have config values that depend on one another; you can use `configence.delay()` to make sure they are loaded in when their dependencies are parsed.
Delayed values are loaded in the order they are written (e.g. higher lines first)
Delayed values can be default-value strings, default-value functions, or whole configence-entries

```python
class MyModel(Configence):
    MY_HERO = configence.str("MY_HERO", 'Son Goku')
    POWER_LEVEL = configence.int("POWER_LEVEL", 9001)
    # delay loaded default-value string
    SHOUT = configence.delay("{MY_HERO} is over {POWER_LEVEL}")
    # delay loaded default-value function
    EVENTS = configence.list("EVENTS", configence.delay(lambda MY_HERO="", SHOUT="": [MY_HERO, SHOUT]) )
    # delay loaded whole entry
    HAS_LONG_SHOUT = configence.delay(lambda SHOUT="":
        configence.bool("HAS_LONG_SHOUT", len(SHOUT) > 12 )
    )
```
## Configence cli parsing
on-top of envars you can also use command line
```python
# will trigger a command line interface
MyModel.cli()
```
