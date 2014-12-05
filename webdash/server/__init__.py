import logging

from flask import Flask, Blueprint

bp = Blueprint('webdash', __name__)

def create_app(config=None, **kwargs):
    app = Flask(__name__)
    configure_app(app, config, **kwargs)
    configure_logging(app)
    configure_blueprints(app)
    return app

def configure_logging(app):
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper())
    app.logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s (%(pathname)s:%(lineno)d)')

    log_path = app.config['LOG_PATH']
    log_dir = os.path.dirname(log_path)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    handler = logging.handlers.TimedRotatingFileHandler(log_path, when='midnight', interval=1, backupCount=365)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)


def configure_app(app, config, **kwargs):
    app.config.from_pyfile('conf/default.cfg')
    app.config.from_pyfile('local.cfg', silent=True)
    app.config.from_envvar('WEBDASH_CONFIG', silent=True)
    if config:
        app.config.from_object(config)
    app.config.update(kwargs)

def configure_blueprints(app):
    app.register_blueprint(bp, url_prefix = '/')

@bp.route('/', methods=['GET'])
def dashboard():
    return 'hello'
