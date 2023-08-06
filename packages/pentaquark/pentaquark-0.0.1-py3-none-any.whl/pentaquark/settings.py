import os
import logging.config
from dotenv import load_dotenv

if os.getenv("ENV", "").lower() == "test":
    ENV_FILE = ".env.test"
elif os.getenv("PENTAQUARK_ENV_FILE_PATH"):
    ENV_FILE = os.getenv("PENTAQUARK_ENV_FILE_PATH")
else:
    ENV_FILE = ".env"

load_dotenv(ENV_FILE)

NEO4J_URI = os.getenv("NEO4J_HOST", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")
NEO4J_DEFAULT_DATABASE = os.getenv("NEO4J_DEFAULT_DATABASE", "neo4j")
NEO4J_ENCRYPTED_CONNECTION = os.getenv("NEO4J_ENCRYPTED_CONNECTION", False)

DEBUG = True

APPS = []


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s L%(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG' if DEBUG else "INFO",
            'propagate': False
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
