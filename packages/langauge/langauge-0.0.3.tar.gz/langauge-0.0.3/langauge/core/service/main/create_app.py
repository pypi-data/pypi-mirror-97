# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from flask import Flask
from flask_restplus import Api

from langauge.core.service.main.database import mongo
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app(debug=True):
    """
    Create an application.
    
    :param debug: whether to run Flask in debug Mode.
    :type debug: boolean
    """
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.debug = debug
    app.config.from_object('configs')

    from langauge.core.service.endpoints.job_status import celery_task_ns
    from langauge.core.service.endpoints.ner import ner_ns
    from langauge.core.service.endpoints.config import config_ns
    # blueprint = Blueprint('api', __name__)
    api = Api(title='LanGauge API', version='1.0')
    api.add_namespace(celery_task_ns)
    api.add_namespace(ner_ns)
    api.add_namespace(config_ns)
    # main.register_blueprint(blueprint)
    api.init_app(app)

    socketio.init_app(app)

    mongo.init_app(app)

    return app
