# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: models.py
# time: 11:38 上午


import logging
from typing import Dict, Any

from tensorflow import keras

from kolibri_dnn.tasks.scoring.base_model import BaseScoringModel
from kolibri_dnn.layers import L


class BiLSTM_Model(BaseScoringModel):

    @classmethod
    def get_default_hyper_parameters(cls) -> Dict[str, Dict[str, Any]]:
        return {
            'layer_bi_lstm': {
                'units': 128,
                'return_sequences': False
            },
            'layer_dense': {
                'activation': 'linear'
            }
        }

    def build_model_architecture(self):
        output_dim = len(self.indexer.label2idx)
        config = self.hyper_parameters
        embed_model = self.embedding.embed_model

        layer_bi_lstm = L.Bidirectional(L.LSTM(**config['layer_bi_lstm']))
        layer_dense = L.Dense(output_dim, **config['layer_dense'])

        tensor = layer_bi_lstm(embed_model.output)
        output_tensor = layer_dense(tensor)

        self.tf_model = keras.Model(embed_model.inputs, output_tensor)


if __name__ == "__main__":
    print(BiLSTM_Model.get_default_hyper_parameters())
    logging.basicConfig(level=logging.DEBUG)
    from kolibri_dnn.corpus import Sentiment140Corpus
    import kolibri_dnn
    sent_data=Sentiment140Corpus()
    dataset=sent_data.get_sent_dataset()

    from kolibri_dnn.indexers.classification_indexer import ClassificationIndexer
    from kolibri_dnn.embeddings import DefaultEmbedding

    processor = ClassificationIndexer(multi_label=False)
    embed = DefaultEmbedding(task=kolibri_dnn.CLASSIFICATION, sequence_length=30, indexer=processor)
    m = model = BiLSTM_Model()
    # m.build_model(x, y)
    m.fit(dataset, epochs=1)
    print(m.predict(dataset.get_data()[:10][0]))
    # m.evaluate(x, y)
    print(m.predict_top_k_class(dataset.get_data()[:10][0]))



