# encoding: utf-8

import os

from kolibri_dnn import macros as k
import pandas as pd
from typing import Tuple, List
from tensorflow.python.keras.utils import get_file
from kolibri_dnn import utils
from kolibri.data.dataset import Dataset
from kolibri.data.document import Document
from kolibri.data.dataset_readers.dataset_reader import DatasetReader
from overrides import overrides
from kolibri.data.fields import TextField, SequenceLabelField, LabelField
from kolibri.tokenizer.token_ import Token
from kolibri.data.token_indexers import SingleIdTokenIndexer

CORPUS_PATH = os.path.join(k.DATA_PATH, 'corpus')


class ConllDataReader(DatasetReader):

    def __init__(self):

        super().__init__({'tokens': SingleIdTokenIndexer()})
        self.target_index = 1

    @overrides
    def _read(self, file_path: str):

        x_data, y_data = [], []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                rows = line.split(' ')
                if len(rows) > 1:
                    x_data.append(rows[0])
                    y_data.append(rows[self.target_index])

                else:
                    doc = self.text_to_document(x_data, y_data)
                    x_data = []
                    y_data = []

                    yield doc

    @overrides
    def text_to_document(self, words, ner_tags):
        fields = {}
        # wrap each token in the file with a token object
        tokens = TextField([Token(w) for w in words], self._token_indexers)

        # Instances in AllenNLP are created using Python dictionaries,
        # which map the token key to the Field type
        fields["tokens"] = tokens
        fields["label"] = SequenceLabelField(ner_tags, tokens)

        return Document(fields)


class CONLL2003ENCorpus(ConllDataReader):
    __corpus_name__ = 'conll2003_en'
    __zip_file__name = 'https://www.dropbox.com/s/c65bzd23ho73c0l/conll2003.tar.gz?dl=1'

    def __init__(self, subset_name, task_name):

        super().__init__()
        self.corpus_path = get_file(self.__corpus_name__,
                                    self.__zip_file__name,
                                    cache_dir=k.DATA_PATH,
                                    untar=True)

        if subset_name not in {'train', 'test', 'valid'}:
            raise ValueError()

        self.file_path = os.path.join(self.corpus_path, f'{subset_name}.txt')

        if task_name not in {'pos', 'chunking', 'ner'}:
            raise ValueError()

        self.target_index = ['pos', 'chunking', 'ner'].index(task_name) + 1

    def get_conll_dataset(self):
        return self.get_dataset(self.file_path)


class Sentiment140Corpus(DatasetReader):
    """

    """

    __corpus_name__ = 'Sentiments140'
    __zip_file__name = "https://www.dropbox.com/s/egk8cwupfs05g00/Sentiments140.tar.gz?dl=1"

    def __init__(self, subset_name='sentiment140_sample'):

        super().__init__({'tokens': SingleIdTokenIndexer()})
        self.corpus_path = get_file(self.__corpus_name__,
                                    self.__zip_file__name,
                                    cache_dir=k.DATA_PATH,
                                    untar=True)

        if subset_name not in {'sentiment140_sample', 'all'}:
            raise ValueError()


        self.file_path = os.path.join(self.corpus_path, f'{subset_name}.csv')


    def _read(self, file_path):
        """
        Load dataset as sequence classification format, char level tokenized

        Returns:
            dataset_features and dataset labels
        """



        df = pd.read_csv(file_path)
        for i, d in df.iterrows():
            x_data = [item for item in d[' text'].split()]
            y_data = d['target']
            yield self.text_to_document(x_data, y_data)


    @overrides
    def text_to_document(self, words, tag):
        fields = {}
        # wrap each token in the file with a token object
        tokens = TextField([Token(w) for w in words], self._token_indexers)

        # Instances in AllenNLP are created using Python dictionaries,
        # which map the token key to the Field type
        fields["tokens"] = tokens
        fields["label"] = LabelField(str(tag))

        return Document(fields)

    def get_sent_dataset(self):
        return self.get_dataset(self.file_path)


class ConsumerComplaintsCorpus(DatasetReader):
    """

    """

    __corpus_name__ = 'consumer_complaints'
    __zip_file__name = "https://www.dropbox.com/s/v2qnany822887k3/consumer_complaints.tar.gz?dl=1"

    def __init__(self, subset_name='sample'):

        super().__init__({'tokens': SingleIdTokenIndexer()})
        self.corpus_path = get_file(self.__corpus_name__,
                                    self.__zip_file__name,
                                    cache_dir=k.DATA_PATH,
                                    untar=True)

        if subset_name not in {'sample', 'validate', 'train', 'test'}:
            raise ValueError()


        self.file_path = os.path.join(self.corpus_path, f'{subset_name}.csv')
        self.df = pd.read_csv(self.file_path)
        self.length=len(self.df.index)


    def _read(self, file_path):
        """
        Load dataset as sequence classification format, char level tokenized

        Returns:
            dataset_features and dataset labels
        """

        for i, d in self.df.iterrows():
            x_data = [item for item in d['Consumer_complaint'].split()]
            y_data = d['Issue']
            yield self.text_to_document(x_data, y_data)


    @overrides
    def text_to_document(self, words, tag):
        fields = {}
        # wrap each token in the file with a token object
        tokens = TextField([Token(w) for w in words], self._token_indexers)

        # Instances in AllenNLP are created using Python dictionaries,
        # which map the token key to the Field type
        fields["tokens"] = tokens
        fields["label"] = LabelField(str(tag))

        return Document(fields)

    def get_sent_dataset(self):
        return self.get_dataset(self.file_path)


if __name__ == "__main__":

    conll = ConsumerComplaintsCorpus()
    dataset=conll.get_sent_dataset()
    for d in dataset.get_data():
        print(d[0])

        print(d[1])

#    dataset = conll.get_sent_dataset()
    for d in dataset.get_data():
        print(d[0])

        print(d[1])
    print("Hello world")

