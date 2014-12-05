import logging

from flask import Flask, Blueprint

from .. import config

bp = Blueprint('webdash', __name__)

def create_app():
    app = Flask(__name__)
    configure_blueprints(app)
    return app

def configure_blueprints(app):
    app.register_blueprint(bp, url_prefix = '/')

@bp.route('/', methods=['GET'])
def dashboard():
    return 'hello'
