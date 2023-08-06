# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: scoring_processor.py
# time: 11:10 上午

from typing import List, Optional

import numpy as np
from tensorflow.keras.utils import to_categorical
import kolibri_dnn
from kolibri_dnn import utils
from kolibri_dnn.indexers.base_indexer import BaseIndexer


def is_numeric(obj):
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all(hasattr(obj, attr) for attr in attrs)


class ScoringIndexer(BaseIndexer):
    """
    Corpus Pre Processor class
    """

    def __init__(self, output_dim=None, **kwargs):
        super(ScoringIndexer, self).__init__(**kwargs)
        self.output_dim = output_dim

    def info(self):
        info = super(ScoringIndexer, self).info()
        info['task'] = kolibri_dnn.SCORING
        return info

    def _build_label_dict(self,
                          label_list: List[List[float]]):
        """
        Build label2idx dict for sequence labeling task

        Args:
            label_list: corpus label list
        """
        if self.output_dim is None:
            label_sample = label_list[0]
            if isinstance(label_sample, np.ndarray) and len(label_sample.shape) == 1:
                self.output_dim = label_sample.shape[0]
            elif is_numeric(label_sample):
                self.output_dim = 1
            elif isinstance(label_sample, list):
                self.output_dim = len(label_sample)
            else:
                raise ValueError('Scoring Label Sample must be a float, float array or 1D numpy array')
        # np_labels = np.array(label_list)
        # if np_labels.max() > 1 or np_labels.min() < 0:
        #     raise ValueError('Scoring Label Sample must be in range[0,1]')

    def process_y_dataset(self,
                          data: List[str],
                          max_len: Optional[int] = None,
                          subset: Optional[List[int]] = None) -> np.ndarray:
        if subset is not None:
            target = utils.get_list_subset(data, subset)
        else:
            target = data
        if self.multi_label:
            return self.multi_label_binarizer.fit_transform(target)
        else:
            numerized_samples = self.numerize_label_sequences(target)
            return to_categorical(numerized_samples, len(self.label2idx))

    def numerize_token_sequences(self,
                                 sequences: List[List[str]]):

        result = []
        for seq in sequences:
            if self.add_bos_eos:
                seq = [self.token_bos] + seq + [self.token_eos]
            unk_index = self.token2idx[self.token_unk]
            result.append([self.token2idx.get(token, unk_index) for token in seq])
        return result

    def numerize_label_sequences(self,
                                 sequences: List[str]) -> List[int]:
        """
        Convert label sequence to label-index sequence
        ``['O', 'O', 'B-ORG'] -> [0, 0, 2]``

        Args:
            sequences: label sequence, list of str

        Returns:
            label-index sequence, list of int
        """
        return [self.label2idx[l.label] for l in sequences]

    def reverse_numerize_label_sequences(self, sequences, **kwargs):
        if self.multi_label:
            return self.multi_label_binarizer.inverse_transform(sequences)
        else:
            return [self.idx2label[label] for label in sequences]



if __name__ == "__main__":
    print('Hello World')

