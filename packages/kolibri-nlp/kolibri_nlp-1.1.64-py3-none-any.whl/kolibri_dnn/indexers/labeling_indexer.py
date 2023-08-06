# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# version: 1.0
# license: Apache Licence
# file: corpus.py
# time: 2019-05-17 11:28

import collections
import logging
import operator
from typing import List, Dict, Optional

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

import kolibri_dnn
from kolibri_dnn import utils
from kolibri_dnn.indexers.base_indexer import BaseIndexer


class LabelingIndexer(BaseIndexer):
    """
    Corpus Pre Processor class
    """

    def info(self):
        info = super(LabelingIndexer, self).info()
        info['task'] = kolibri_dnn.LABELING
        return info


    def process_y_dataset(self, y_data, max_len=None, subset=None) -> np.ndarray:
        if max_len is None:
            max_len=self.dataset_info['RECOMMEND_LEN']

        if subset is not None:
            target = [y_data[i] for i in subset if i < len(y_data)]
        else:
            target = y_data[:]

        numerized_samples=self.convert_label_sequences([d for d in target])

        padded_seq = pad_sequences(
            numerized_samples, max_len, padding='post', truncating='post')
        return to_categorical(padded_seq)


    def convert_label_sequences(self,
                                sequences: List[List[str]]) -> List[List[int]]:
        result = []
        for seq in sequences:
            result.append([self.vocabulary.get_token_index(token, 'labels') for token in seq])
        return result

    def reverse_numerize_label_sequences(self,
                                         sequences,
                                         lengths=None):
        result = []

        for index, seq in enumerate(sequences):
            labels = []
            for idx in seq:
                labels.append(self.idx2label()[idx])
            if lengths is not None:
                labels = labels[:lengths[index]]
            result.append(labels)
        return result


if __name__ == "__main__":
    print('hello world')
