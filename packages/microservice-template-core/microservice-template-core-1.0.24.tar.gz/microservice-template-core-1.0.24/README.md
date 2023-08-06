# Foobar

Microservice template core is a Python library for easy start of microservice with Flask, Logger, Tracer inside

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install microservice_template_core
```

## Usage

```python
from microservice_template_core import Core
from microservice_template_core.settings import FlaskConfig

if __name__ == '__main__':
    FlaskConfig.FLASK_DEBUG = True
    app = Core()
    app.run()
```

## State 
In development


## License
