# encoding: utf-8
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz

@version: 1.0
@license: Apache Licence
@file: __init__.py
@time: 2019-05-17 11:15

"""
import os
os.environ['TF_KERAS'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


from kolibri_dnn.macros import TaskType, config

custom_objects = tf.keras.utils.get_custom_objects()
CLASSIFICATION = TaskType.CLASSIFICATION
LABELING = TaskType.LABELING
SCORING = TaskType.SCORING

from kolibri_dnn.version import __version__

from kolibri_dnn import layers
from kolibri_dnn import corpus
from kolibri_dnn import embeddings
from kolibri_dnn import macros
from kolibri_dnn import indexers
from kolibri_dnn import tasks
from kolibri_dnn import utils
from kolibri_dnn import callbacks


