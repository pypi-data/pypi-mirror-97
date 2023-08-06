import json
import logging
import pydoc
from typing import Union, List, Optional, Dict

import numpy as np
import tensorflow.keras as keras


import kolibri_dnn
from kolibri_dnn.indexers import ClassificationIndexer, LabelingIndexer, ScoringIndexer
from kolibri_dnn.indexers.base_indexer import BaseIndexer

L = keras.layers


class BaseEmbedding(object):
    """Base class for Embedding Model"""

    def info(self) -> Dict:
        return {
            'indexer': self.indexer.info(),
            'class_name': self.__class__.__name__,
            'module': self.__class__.__module__,
            'config': {
                'sequence_length': self.sequence_length,
                'embedding_size': self.embedding_size,
                'task': self.task
            },
            'embed_model': json.loads(self.embed_model.to_json()),
        }

    @classmethod
    def _load_saved_instance(cls,
                             config_dict: Dict,
                             model_path: str,
                             tf_model: keras.Model):

        indexer_info = config_dict['indexer']
        indexer_class = pydoc.locate(f"{indexer_info['module']}.{indexer_info['class_name']}")
        indexer = indexer_class(**indexer_info['config'])

        instance = cls(indexer=indexer,
                       from_saved_model=True, **config_dict['config'])

        embed_model_json_str = json.dumps(config_dict['embed_model'])
        instance.embed_model = keras.models.model_from_json(embed_model_json_str,
                                                            custom_objects=kolibri_dnn.custom_objects)

        # Load Weights from model
        for layer in instance.embed_model.layers:
            layer.set_weights(tf_model.get_layer(layer.name).get_weights())
        return instance

    def __init__(self,
                 task: str = None,
                 sequence_length: Union[int, str] = 'auto',
                 embedding_size: int = 100,
                 indexer: Optional[BaseIndexer] = None,
                 from_saved_model: bool = False):
        self.task = task
        self.embedding_size = embedding_size

        if indexer is None:
            if task == kolibri_dnn.CLASSIFICATION:
                self.indexer = ClassificationIndexer()
            elif task == kolibri_dnn.LABELING:
                self.indexer = LabelingIndexer()
            elif task == kolibri_dnn.SCORING:
                self.indexer = ScoringIndexer()
            else:
                raise ValueError('Need to set the processor param, value: {labeling, classification, scoring}')
        else:
            self.indexer = indexer

        self.sequence_length: Union[int, str] = sequence_length
        self.embed_model: Optional[keras.Model] = None
        self._tokenizer = None

    @property
    def token_count(self) -> int:
        """
        corpus token count
        """
        if self.indexer.vocabulary:
            return self.indexer.vocabulary.get_vocab_size()
        return 0

    @property
    def sequence_length(self) -> Union[int, str]:
        """
        model sequence length
        """
        return self.indexer.sequence_length

    @property
    def label2idx(self) -> Dict[str, int]:
        """
        label to index dict
        """
        return self.indexer.label2idx

    @property
    def token2idx(self) -> Dict[str, int]:
        """
        token to index dict
        """
        return self.indexer.token2idx

    @property
    def tokenizer(self):
        if self._tokenizer:
            return self._tokenizer
        else:
            raise ValueError('This embedding not support built-in tokenizer')

    @sequence_length.setter
    def sequence_length(self, val: Union[int, str]):
        if isinstance(val, str):
            if val == 'auto':
                logging.warning("Sequence length will auto set at 95% of sequence length")
            elif val == 'variable':
                val = None
            else:
                raise ValueError("sequence_length must be an int or 'auto' or 'variable'")
        self.indexer.sequence_length = val

    def _build_model(self, **kwargs):
        raise NotImplementedError

    def analyze_corpus(self,vocabulary):
        """
        Prepare embedding layer and indexer for labeling task

        Args:
            x:
            y:

        Returns:

        """
        self.indexer.build_index(vocabulary=vocabulary)
        if self.sequence_length == 'auto':
            self.sequence_length = self.indexer.dataset_info['RECOMMEND_LEN']
        self._build_model()


    def embed_one(self, sentence: Union[List[str], List[int]]) -> np.array:
        """
        Convert one sentence to vector

        Args:
            sentence: target sentence, list of str

        Returns:
            vectorized sentence
        """
        return self.embed([sentence])[0]

    def embed(self,
              sentence_list: Union[List[List[str]], List[List[int]]],
              debug: bool = False) -> np.ndarray:
        """
        batch embed sentences

        Args:
            sentence_list: Sentence list to embed
            debug: show debug info
        Returns:
            vectorized sentence list
        """
        tensor_x = self.process_x_dataset(sentence_list)

        if debug:
            logging.debug(f'sentence tensor: {tensor_x}')
        embed_results = self.embed_model.predict(tensor_x)
        return embed_results

    def process_x_dataset(self,
                          data: List[List[str]],
                          subset: Optional[List[int]] = None) -> np.ndarray:
        """
        batch process feature data while training

        Args:
            data: target dataset
            subset: subset index list

        Returns:
            vectorized feature tensor
        """
        return self.indexer.process_x_dataset(data, self.sequence_length, subset=subset)

    def process_y_dataset(self,
                          data: List[List[str]],
                          subset: Optional[List[int]] = None) -> np.ndarray:
        """
        batch process labels data while training

        Args:
            data: target dataset
            subset: subset index list

        Returns:
            vectorized feature tensor
        """
        return self.indexer.process_y_dataset(data, max_len=self.sequence_length, subset=subset)

    def reverse_numerize_label_sequences(self,
                                         sequences,
                                         lengths=None):
        return self.indexer.reverse_numerize_label_sequences(sequences, lengths=lengths)

    def __repr__(self):
        return f"<{self.__class__} seq_len: {self.sequence_length}>"

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    print("Hello world")
