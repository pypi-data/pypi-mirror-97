#!/bin/env python3
# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from langauge.core.service import main
from flask_socketio import SocketIO

app = main.create_app(debug=True)
socketio = SocketIO(app)

host = app.config.get("HOST")
port = app.config.get("PORT")

if __name__ == '__main__':
    print("Server running at http://%s:%s" % (host, port))
    socketio.run(app, host, port=int(port))
