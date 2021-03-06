import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .util import bcolors
from flask_socketio import SocketIO
from .config import config_by_name
from app.main.base_logger import logger, LOGLEVEL

logger = logger.getLogger(__name__)


env_name = (os.getenv('ENVIRONMENT') or 'dev').upper()
config_env = config_by_name[env_name]

bcrypt = Bcrypt()
if LOGLEVEL == 'DEBUG':
    socketio = SocketIO(logger=True, engineio_logger=True)
else:
    socketio = SocketIO()


if env_name == "PROD":
    print(f"{bcolors.FAIL}{bcolors.BOLD}***** WARNING *****\n***** USING PRODUCTION *****{bcolors.ENDC}")
else:
    print(f"{bcolors.WARNING}USING ENVIRONMENT: {env_name}{bcolors.ENDC}")

from .model import Base

db = SQLAlchemy(metadata=Base.metadata)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_env)
    socketio.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    logger.debug('create app')
    return app
