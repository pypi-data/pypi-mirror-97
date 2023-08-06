# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: base_processor.py
# time: 2019-05-21 11:27

import collections
import logging
import operator
from typing import List, Optional, Union, Dict, Any

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from kolibri.data.vocabulary import Vocabulary

from kolibri_dnn import utils



class BaseIndexer(object):
    """
    Corpus Pre Processor class
    """

    def __init__(self,  **kwargs):

        self.vocabulary=None
        self.dataset_info={}
        self.sequence_length = kwargs.get('sequence_length', None)



    def build_index(self, vocabulary):

        self.vocabulary = vocabulary

        rec_len = self.vocabulary.recommended_padding_lengths
        self.dataset_info['RECOMMEND_LEN']=rec_len['tokens']



    @property
    def label2idx(self):
        token2idx=None
        if self.vocabulary:
            token2idx= self.vocabulary.get_token_to_index_vocabulary('labels')
        return token2idx

    @property
    def idx2label(self):
        idx2token=None
        if self.vocabulary:
            idx2token= self.vocabulary.get_index_to_token_vocabulary('labels')
        return idx2token

    def process_x_dataset(self, x_data,  max_len=None, subset=None) -> np.ndarray:
        if max_len is None:
            max_len = self.dataset_info['RECOMMEND_LEN']
        numerized_samples=[]
        if subset is not None:
            target = [x_data[i] for i in subset if i < len(x_data)]
        else:
            target=x_data[:]

        for d in target:
            numerized_samples.append([self.vocabulary.get_token_index(t, 'tokens') for t in d])

        return pad_sequences(numerized_samples, max_len, padding='post', truncating='post')

    def process_y_dataset(self,
                          data: Union[List[List[str]], List[str]],
                          max_len: Optional[int],
                          subset: Optional[List[int]] = None) -> np.ndarray:
        raise NotImplementedError

    def convert_token_sequences(self,
                                sequences: List[List[str]]):
        raise NotImplementedError

    def convert_label_sequences(self,
                                sequences: List[List[str]]) -> List[List[int]]:
        raise NotImplementedError

    def info(self):
        return {
            'class_name': self.__class__.__name__,
            'config': {
                'label2idx': self.label2idx,
                'dataset_info': self.dataset_info,
                'sequence_length': self.sequence_length
            },
            'module': self.__class__.__module__,
        }


    def reverse_convert_label_sequences(self, sequence, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return f"<{self.__class__}>"

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    print("Hello world")
