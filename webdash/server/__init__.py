import logging
import datetime

import dateutil.parser
from flask import Flask, Blueprint, request

from .. import config, configure_logging, get_db, jsondumps

bp = Blueprint('webdash', __name__)
db = get_db().webdash

def create_app():
    app = Flask(__name__)
    configure_blueprints(app)
    configure_logging(app.logger)
    return app

def configure_blueprints(app):
    app.register_blueprint(bp, url_prefix = '/')


@bp.route('/data', methods=['GET'])
def poll_data():
    since = dateutil.parser.parse(request.args.get('since'))
    docs = [doc for doc in db.data.find({'fetch_date': {'$gt': since}}, {'_id': False}).sort('fetch_date', 1)]
    return jsondumps(docs),200,{'Content-Type':'application/json'}
    
@bp.route('/', methods=['GET'])
def dashboard():
    return 'hello'

