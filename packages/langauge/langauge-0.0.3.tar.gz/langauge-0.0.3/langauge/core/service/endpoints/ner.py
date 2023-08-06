# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import absolute_import

import json
import logging
import os
from itertools import islice

from flask import request, url_for
from langauge.core.service.main.worker import celery
from langauge.core.service.endpoints.job_status import task_already_running
from werkzeug.utils import secure_filename
from flask_restplus import Resource, Namespace

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = os.environ

"""
Exposes two endpoints, one for the actual run and another one for the preview. 
Takes in common inputs: model and the channel information. 
"""
ner_ns = Namespace('ner',
                   description='All requests related to Named Entity Recognition Task')



@ner_ns.route('/<model>/<channel>')
@ner_ns.param('model', 'The model identifier')
@ner_ns.param('channel', 'The channel identifier')
class ModelRun(Resource):
    @ner_ns.doc('Create & submits an async inference task')
    def post(self, model, channel):
        logger.info("in /ner/ModelRun")
        try:
            if not (int(channel) == 0 or int(channel) == 1):
                channel = '0'
        except ValueError:
            channel = '0'

        file = request.files['file']

        # input file setup
        target = os.path.join(env.get('UPLOAD_FOLDER'), 'ner', model)
        if not os.path.isdir(target):
            os.makedirs(target)
        filename = secure_filename(file.filename)
        input_dest = "/".join([target, filename])
        file.save(input_dest)

        # output file setup
        output = os.path.join(env.get('OUTPUT_FOLDER'))
        if not os.path.isdir(output):
            os.makedirs(output)

        if not task_already_running(str(channel)):
            # call async task
            logger.info("starting async task")
            task = celery.send_task(model.split("_")[0],
                                    args=[model, input_dest, output])
            return url_for('task_status', task_id=task.id), 202, {}
        else:
            logger.info('another task already running')
            return "wait for the task to complete", 425, {}


@ner_ns.route('/preview/<model>/<num_lines>/<channel>')
@ner_ns.param('model', 'The model identifier')
@ner_ns.param('num_lines', 'initial number of lines to be executed for the preview')
@ner_ns.param('channel', 'The channel identifier')
class ModelPreview(Resource):
    @ner_ns.doc('Create & submits an async inference preview')
    def post(self, model, num_lines, channel):
        logger.info("in /preview/ner/ModelPreview")
        try:
            if not (int(channel) == 0 or int(channel) == 1):
                channel = '0'
        except ValueError:
            channel = '0'
        try:
            num_lines = int(num_lines)
        except ValueError:
            num_lines = 5

        file = request.files['file']

        target = os.path.join(env.get('UPLOAD_FOLDER'), 'ner', model)
        if not os.path.isdir(target):
            os.makedirs(target)
        filename = secure_filename(file.filename)
        input_dest = "/".join([target, filename])
        file.save(input_dest)
        with open(input_dest, 'r') as infile:
            head = list(islice(infile, num_lines))

        # output file setup
        output = os.path.join(env.get('OUTPUT_FOLDER'))
        if not os.path.isdir(output):
            os.makedirs(output)

        if not task_already_running(str(channel)):
            task = celery.send_task(model.split("_")[0]+'.preview',
                                    args=[model, head, output])
            return url_for('task_status', task_id=task.id), 202, {}
        else:
            return "wait for the task to complete", 425, {}

