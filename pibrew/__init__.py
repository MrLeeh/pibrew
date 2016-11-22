import os

import arrow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

from config import config
from .brewcontroller import BrewController


# Flask Plugins
db = SQLAlchemy()
bootstrap = Bootstrap()
socketio = SocketIO()
brew_controller = BrewController()


from . import events # noqa


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('PIBREW_CONFIG', 'development')
    app.config.from_object(config[config_name])

    # init flask plugins
    db.init_app(app)
    bootstrap.init_app(app)
    socketio.init_app(app)
    brew_controller.init_app(app)

    # create blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    # start the background task
    socketio.start_background_task(target=process_controller)

    return app


def process_controller():
    interval = brew_controller.app.config['PROCESS_INTERVAL']
    while(1):
        current_time = arrow.now()
        brew_controller.process()
        socketio.emit(
            'update',
            {
                'time': current_time.for_json(),
                'temp_setpoint': brew_controller.temp_setpoint,
                'temp_current': brew_controller.temp_current
            }
        )
        socketio.sleep(interval)