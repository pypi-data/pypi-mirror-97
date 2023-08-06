# Flask Atomic Auth

Plugin Flask module for user management. Module exposes API endpoints that allows for
fetching, creation and permission management for users out of the box.

## Installation

`pip install Flask-Atomic-Auth`

## Setup 

Import and bind the extension to your application or in app factory (recommended approach for Flask).

```python
from flask import Flask
from flask_atomic_auth import AAuth

auth = AAuth()

def create_app(env='Develop'):
    app = Flask(__name__, instance_relative_config=True)
    ...
    
    # other extensions
    auth.init_app(app)
    
    ...
    return app
```

Once you have a valid `SQLALCHEMY_DATABASE_URI` configured, the database tables should be 
automatically bound and created in the target database.

## Usage

### Creating Users

