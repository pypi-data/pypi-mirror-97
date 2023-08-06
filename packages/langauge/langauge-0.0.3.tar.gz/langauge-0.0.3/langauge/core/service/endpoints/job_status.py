# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import logging
import os

from flask import jsonify, send_file, abort
from flask_restplus import Resource, Namespace, reqparse

from langauge.core.service.main.database import mongo
from langauge.core.service.main.worker import celery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = os.environ
"""
Provides all the task related information. 
"""
celery_task_ns = Namespace('celery', description='All task related information')


@celery_task_ns.route('/<task_id>', endpoint='task_status')
@celery_task_ns.param('task_id', 'The status identifier')
class TaskStatus(Resource):
    @celery_task_ns.doc('Provides status information of a particular task')
    def get(self, task_id):
        task = celery.AsyncResult(task_id)
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            response['id'] = task_id
            if 'preview' in task.info:
                response['preview'] = task.info['preview']
            if 'time' in task.info:
                response['time'] = task.info['time']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
        return jsonify(response)


@celery_task_ns.route('/fileDownload/<task_id>')
@celery_task_ns.param('task_id', 'The task_id identifier')
class DownloadFile(Resource):
    @celery_task_ns.doc('Provides file related to a particular task')
    def get(self, task_id):
        outputs = env.get('OUTPUT_FOLDER')  # + task_id + '-00000-of-00001'
        file = ""
        for i in os.listdir(outputs):
            if os.path.isfile(os.path.join(outputs, i)) and task_id in i:
                file = os.path.join(outputs, i)
                break
        try:
            return send_file(file,
                             mimetype='text/csv',
                             attachment_filename='results.txt',
                             as_attachment=True)
        except:
            abort(404)



def task_already_running(channel):
    """
    Checks the number of tasks already runing. Returns true if its more than 4, otherwise false.
        
    :param channel: channel that submitted that task
    """
    i = celery.control.inspect()
    if i.active() is not None:
        for key, value in i.active().items():
            if len(value) >= 4:
                logger.log("there are already 2 task runing, Please submit after some time !!")
                return True
            # for task in value:
            #     if task.get('id') == channel:
            #         return True
        return False


parser = reqparse.RequestParser()
parser.add_argument('page_size', type=int,
                    help="number of records per page",
                    default=10, required=True)
parser.add_argument('page_num', type=int,
                    help="the page identifier",
                    default=1, required=True)


@celery_task_ns.route('/history')
@celery_task_ns.expect(parser)
class TaskHistory(Resource):
    @celery_task_ns.doc('Get all the task history')
    def get(self):
        args = parser.parse_args()
        # Calculate number of documents to skip
        skips = args.get('page_size') * (args.get('page_num') - 1)
        documents = mongo.db.celery_taskmeta.find()
        taskList = []
        for history in documents:
            if 'preview' in history.get('result'):
                continue
            history['id'] = history.pop('_id')
            result = json.loads(history.pop('result'))
            history['model'] = result.get('model', '')
            history['task'] = result.get('task', '')
            taskList.append(history)
        # return taskList
        return taskList[skips:skips+args.get('page_size')]


@celery_task_ns.route('/search/<task_id>')
@celery_task_ns.param('task_id', 'The task_id identifier')
class GetTask(Resource):
    @celery_task_ns.doc('Get the task related to the specific task id ')
    def get(self, task_id):
        from bson.json_util import dumps
        documents = mongo.db.celery_taskmeta.find(
            {'_id': {"$regex": task_id, "$options": "$i"}}
        )
        taskList = []
        documents = json.loads(dumps(documents))
        logger.info(documents)
        for document in documents:
            logger.info(document)
            document['id'] = document.pop('_id')
            taskList.append(document)
            logger.info(taskList)
        return taskList


@celery_task_ns.route('/history/total')
class GetTask(Resource):
    @celery_task_ns.doc('Get the total number of tasks')
    def get(self):
        documents = mongo.db.celery_taskmeta.find()
        count = 0
        for history in documents:
            if 'preview' in history.get('result'):
                continue
            count = count+1
        return count