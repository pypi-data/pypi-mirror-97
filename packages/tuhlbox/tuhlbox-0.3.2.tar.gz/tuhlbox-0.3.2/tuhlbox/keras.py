"""Contains models that use keras for neural networks."""
import logging

import numpy as np
from dstoolbox.transformers import Padder2d
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import (LSTM, Bidirectional, Conv1D, Dense,
                                     Dropout, Embedding, Flatten,
                                     GlobalMaxPooling1D, MaxPooling1D)
from tensorflow.keras.models import Sequential
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

logger = logging.getLogger(__name__)


def _count_num_words(x):
    return int(max([max(document) for document in x])) + 1


class MaxLengthPadder(TransformerMixin, BaseEstimator):
    """Padding Transformer that pads to max length of documents."""

    def __init__(self, pad_value, min_length=5):
        """
        Initialize the transformer.

        Args:
            pad_value: Value to use for padding shorter sequences
            min_length: optional minimum length to pad to.
        """
        self.pad_value = pad_value
        self.min_length = min_length

    def fit(self, x, y=None, **fit_params):
        """Fit the transformer."""
        return self

    def transform(self, documents):
        """
        Pad documents to the maximum length found within documents.

        Args:
            documents: list of sequences

        Returns: list of padded sequences

        """
        max_len = max([len(document) for document in documents]
                      + [self.min_length])
        print('max len is', max_len)
        padder = Padder2d(max_len=max_len, pad_value=self.pad_value)
        return padder.transform(documents)


class KerasModel(BaseEstimator, ClassifierMixin):
    """A generic model that can use external model_fn functions."""

    def __init__(
        self,
        model_fn=None,
        embedding_dim=300,
        epochs=10,
        batch_size=2,
        validation_data=None,
        exclude_embedding=False,
    ):
        """
        Initialize the model.

        Args:
            model_fn: a keras model building function. See keras for details.
            embedding_dim: the dimension of the (first) embedding layer.
            epochs: epoch to train.
            batch_size: batch size of network training
            validation_data: optional data that will be passed to the model's
                fit function to get running validation scores during fitting.
            exclude_embedding: if set, does not use a first embedding layer.
        """
        # passed parameters
        self.epochs = epochs
        self.embedding_dim = embedding_dim
        self.model_fn = model_fn
        self.batch_size = batch_size  # for sklearn cloning
        self.model_kwargs = {}
        self.validation_data = validation_data
        self.exclude_embedding = exclude_embedding

    def fit(self, x, y, **fit_params):
        """Fit the model."""
        num_words = _count_num_words(x)
        sequence_length = len(x[0])

        if not self.exclude_embedding:
            embedding_layer = Embedding(
                num_words,
                self.embedding_dim,
                input_length=sequence_length,
                trainable=True,
            )
            self.model_kwargs['embedding_layer'] = embedding_layer

        self.model_kwargs['num_classes'] = len(set(y))
        self.model_kwargs['epochs'] = self.epochs
        self.model_kwargs['batch_size'] = self.batch_size
        fit_params['validation_data'] = self.validation_data
        self.model_kwargs['callbacks'] = [
            TensorBoard(
                log_dir='tensorboard-logs',
            )
        ]
        self.model = KerasClassifier(self.model_fn, **self.model_kwargs)
        x = np.asarray(x).astype('float32')
        self.model.fit(x, y, **fit_params)

    def predict(self, x):
        """Predict the data."""
        return self.model.predict(x)

    @property
    def configuration(self):
        """Return a database representation for this model."""
        return self.get_params()


def make_cnn(embedding_layer, num_classes):
    """
    Create a simple CNN network.

    Args:
        embedding_layer: Pre-defined keras embedding layer.
        num_classes: number of classes that are embedded.

    Returns: an already compiled keras CNN model.
    """
    model = Sequential([
        embedding_layer,
        Dropout(0.25),
        Conv1D(500, 3, padding='same'),
        MaxPooling1D(),
        Conv1D(500, 4, padding='same'),
        MaxPooling1D(),
        Conv1D(500, 5, padding='same'),
        GlobalMaxPooling1D(),
        Dense(num_classes, activation='softmax'),
    ])
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    return model


def make_lstm(embedding_layer, num_classes):
    """
    Create a simple LSTM network with two layers.

    Args:
        embedding_layer: Pre-defined keras embedding layer.
        num_classes: number of classes that are embedded.

    Returns: an already compiled keras LSTM model.
    """
    model = Sequential([
        embedding_layer,
        Bidirectional(LSTM(256, activation='relu', return_sequences=True)),
        Dropout(0.25),
        Bidirectional(LSTM(256, activation='relu', return_sequences=True)),
        Flatten(),
        Dropout(0.25),
        Dense(num_classes, activation='softmax'),
    ])
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    return model
