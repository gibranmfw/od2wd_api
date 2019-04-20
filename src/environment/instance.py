import os

# Load the development "mode". Use "development" if not specified
env = {
    "PYTHON_ENV": os.environ.get("PYTHON_ENV", "development"),
    "SECRET": os.environ.get("SECRET"),
    "DUMP_PATH": os.environ.get("DUMP_PATH"),
    "MODEL_PATH": os.environ.get("MODEL_PATH"),
    "INDEX_URL": os.environ.get("INDEX_URL"),
    'PROPERTY_INDEX': os.environ.get('PROPERTY_INDEX'),
    'INDEX_HOST': os.environ.get("INDEX_HOST"),
    'INDEX_PORT': os.environ.get("INDEX_PORT"),
    'MODEL_NAME': os.environ.get("MODEL_NAME")
}

# Configuration for each environment
# Alternatively use "python-dotenv"
all_environments = {
    "development": { "port": 5000, "debug": True, "swagger-url": "/main/swagger" },
    "production": { "port": 8080, "debug": False, "swagger-url": None  }
}

# The config for the current environment
environment_config = all_environments[env['PYTHON_ENV']]