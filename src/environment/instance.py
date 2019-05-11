import os
from dotenv import load_dotenv

load_dotenv()
# Load the development "mode". Use "development" if not specified
env = {
    "PYTHON_ENV": os.getenv("PYTHON_ENV", "development"),
    "SECRET": os.getenv("SECRET"),
    "DUMP_PATH": os.getenv("DUMP_PATH"),
    "MODEL_PATH": os.getenv("MODEL_PATH"),
    "INDEX_URL": os.getenv("INDEX_URL"),
    'PROPERTY_INDEX': os.getenv('PROPERTY_INDEX'),
    'INDEX_HOST': os.getenv("INDEX_HOST"),
    'INDEX_PORT': os.getenv("INDEX_PORT"),
    'MODEL_NAME': os.getenv("MODEL_NAME")
}

# Configuration for each environment
# Alternatively use "python-dotenv"
all_environments = {
    "development": { "port": 5000, "debug": True, "swagger-url": "/main/swagger" },
    "production": { "port": 8080, "debug": False, "swagger-url": None  }
}

# The config for the current environment
environment_config = all_environments[env['PYTHON_ENV']]
