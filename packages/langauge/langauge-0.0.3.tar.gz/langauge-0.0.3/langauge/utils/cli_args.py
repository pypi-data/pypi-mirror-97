# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Definitions of click options shared by several CLI commands.
"""
import click


HOST = click.option("--host", "-h", default="127.0.0.1",
                    help="The network address to listen on (nginx.conf: 127.0.0.1). "
                         "Use 0.0.0.0 to bind to all addresses if you want to access the tracking "
                         "server from other machines.")

PORT = click.option("--port", "-p", default="8080",
                    help="The port to listen on (nginx.conf: 8080).")

BACKEND = click.option("--backend", "-b", default="127.0.0.1:5000",
                    help="The backend address & port to listen on (nginx.conf: 127.0.0.1:5000). ")

BACKENDPORT = click.option("--backendport", "-bp", default="5000",
                    help="The REST backend port to listen on (nginx.conf: 5000).")