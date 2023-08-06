# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os

DEBUG = True

env = os.environ

HOST = env.get("HOST", "0.0.0.0")
PORT = env.get("PORT", "5000")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = env.get("UPLOAD_FOLDER", os.path.dirname(__file__)+'/upload')
OUTPUT_FOLDER = env.get("OUTPUT_FOLDER", os.path.dirname(__file__)+'/output')
CONFIG_FOLDER = env.get("CONFIG_FOLDER", os.path.dirname(__file__)+'/config')

CELERY_BROKER_URL = env.get("CELERY_BROKER_URL", "redis://localhost:6379"),
CELERY_RESULT_BACKEND = env.get("CELERY_RESULT_BACKEND", "mongodb://root:root@localhost:27017/celery?authSource=admin")


# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

CORS_HEADERS = "Content-Type"

MONGO_URI = env.get("CELERY_RESULT_BACKEND", "mongodb://root:root@localhost:27017/celery?authSource=admin")