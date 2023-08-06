# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
# pytype: skip-file

from __future__ import absolute_import

import json
import os
import time

import apache_beam as beam
import torch
from apache_beam.options.pipeline_options import PipelineOptions
from celery import Celery
from celery.utils.log import get_task_logger
from transformers import AutoTokenizer, AutoModelForTokenClassification

# loads the pretrained model which is then used for predicting values
# can read more about it here: https://github.com/huggingface/transformers
from langauge.core.dispatcher.options.pipeline_options import get_pipeline_options
from langauge.core.dispatcher.model.utils.download_azure import AzureBlobFileDownloader

logger = get_task_logger(__name__)

env = os.environ
CELERY_BROKER_URL = env.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env.get("CELERY_RESULT_BACKEND", "mongodb://root:root@localhost:27017/celery")

celery = Celery("task",
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)



class Tokenize(beam.DoFn):
    """
    The tokenizer is responsible for all the preprocessing the pretrained model expects, 
    and can be called directly on one (or list) of texts. 
    It outputs a dictionary which is then passed to the model for inference. 
    """

    def __init__(self, model_name):
        self.tokenizer = None
        self.modelName = model_name

    def setup(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelName)

    def process(self, sequence):
        input_ids = torch.tensor(self.tokenizer.encode(sequence)).unsqueeze(0)
        yield {'tokens': self.tokenizer.tokenize(sequence), 'inputs': input_ids}


class Predict(beam.DoFn):
    """
    Loads the pretrained model which is then used for predicting values
    Can read more about it here: https://github.com/huggingface/transformers
    """

    def __init__(self, modelName):
        self.model = None
        self.modelName = modelName

    def setup(self):
        self.model = AutoModelForTokenClassification.from_pretrained(self.modelName)

    def process(self, inputs):
        with torch.no_grad():
            outputs = self.model(inputs['inputs'])
        predictions = outputs[0].argmax(axis=-1)[0][1:-1]
        for token, pred in zip(inputs['tokens'], predictions):
            yield {'token': token, 'prediction': self.model.config.id2label[pred.numpy().item()]}



@celery.task(name='pubMedBERT', bind=True)
def pubmed_run(self, model_name, source, output_loc):
    """
    Task registered with celery.
    Creates & submits a beam pipeline to the provided flink cluster

    :param model_name: the model identifier
    :param source: location of input file
    :param output_loc: location of output file
    """
    logger.info("pubMedBERT started")
    start_time_of_task = time.time()
    sink = "/".join([output_loc, self.request.id.__str__()])
    self.update_state(state='PROGRESS', meta={'task': 'ner', 'model': model_name})

    beam_options = PipelineOptions(get_pipeline_options(model_name))
    if not os.path.exists('/models/' + model_name):
        # Initialize class and upload files
        azure_blob_file_downloader = AzureBlobFileDownloader()
        azure_blob_file_downloader.download_blobs_in_container(model_name + '.tar.xz')
    # time.sleep(120)
    with beam.Pipeline(options=beam_options) as p:
        main_pipeline = (p
                         # | 'Feature extraction' >> feature_extraction
                         | 'Read file' >> beam.io.ReadFromText(source)
                         | 'Tokenize' >> beam.ParDo(Tokenize('/models/' + model_name))
                         | 'Predict' >> beam.ParDo(Predict('/models/' + model_name))
                         # | "print" >> beam.Map(print)
                         # | 'Format as JSON' >> task.Map(json.dumps)
                         | 'Write predictions' >> beam.io.WriteToText(sink)
                         )
    time_taken = time.time() - start_time_of_task
    return {'task': 'ner', 'model': model_name, 'time': time_taken}


@celery.task(name='pubMedBERT.preview', bind=True)
def pubmed_preview(self, model_name, data, output_loc):
    """
    Task registered with celery.
    Creates & submits a beam pipeline to the provided flink cluster
    
    :param model_name: the model identifier
    :param data: list of string
    """
    logger.info("pubMedBERT preview started")
    sink = "/".join([output_loc, self.request.id.__str__()])
    beam_options = PipelineOptions(get_pipeline_options(model_name))
    self.update_state(state='PROGRESS', meta={'task': 'ner', 'model': model_name, 'preview': ''})
    if not os.path.exists('/models/' + model_name):
        # Initialize class and upload files
        azure_blob_file_downloader = AzureBlobFileDownloader()
        azure_blob_file_downloader.download_blobs_in_container(model_name + '.tar.xz')
    with beam.Pipeline(options=beam_options) as p:
        preview_pipeline = (p
                            | "Create" >> beam.Create(data)
                            | 'Strip' >> beam.Map(lambda text: text.strip('\n'))
                            | 'Tokenize' >> beam.ParDo(Tokenize('/models/' + model_name))
                            | 'Predict' >> beam.ParDo(Predict('/models/' + model_name))
                            | 'Combine' >> beam.combiners.ToList()
                            | 'Write predictions' >> beam.io.WriteToText(sink)
                            )

    for i in os.listdir(output_loc):
        if os.path.isfile(os.path.join(output_loc, i)) and self.request.id.__str__() in i:
            file_name = os.path.join(output_loc, i)
            with open(file_name, 'r') as file:
                data = file.read().replace("\'", "\"")
                return {'task': 'ner', 'model': model_name, 'preview': json.dumps(json.loads(data))}

    return {'task': 'ner', 'model': model_name, 'preview': json.dumps([])}
