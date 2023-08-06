from typing import List, Optional

import numpy as np
from tensorflow.keras.utils import to_categorical

import kolibri_dnn
from kolibri_dnn import utils
from kolibri_dnn.indexers.base_indexer import BaseIndexer
from sklearn.preprocessing import MultiLabelBinarizer


class ClassificationIndexer(BaseIndexer):
    """
    Corpus Pre Processor class
    """

    def __init__(self, multi_label=False, **kwargs):
        super(ClassificationIndexer, self).__init__(**kwargs)
        self.multi_label = multi_label
        if self.label2idx:
            self.multi_label_binarizer: MultiLabelBinarizer = MultiLabelBinarizer(classes=list(self.label2idx.keys()))
            self.multi_label_binarizer.fit([])
        else:
            self.multi_label_binarizer: MultiLabelBinarizer = None

    def info(self):
        info = super(ClassificationIndexer, self).info()
        info['task'] = kolibri_dnn.CLASSIFICATION
        info['config']['multi_label'] = self.multi_label
        return info


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
        return [self.label2idx[l] for l in sequences]

    def reverse_numerize_label_sequences(self, sequences, **kwargs):
        if self.multi_label:
            return self.multi_label_binarizer.inverse_transform(sequences)
        else:
            return [self.idx2label[label] for label in sequences]


if __name__ == "__main__":
    print('Hello World')
