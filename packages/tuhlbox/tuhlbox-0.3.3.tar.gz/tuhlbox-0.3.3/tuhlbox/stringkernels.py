"""Transformers calculating string kernels."""
import logging
from collections import defaultdict

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

logger = logging.getLogger(__name__)


def presence_kernel(x, y, ngram_min, ngram_max):
    """Calculate the presence kernel, Ionescu & Popescu 2017."""
    result = np.zeros((len(x), len(y)), dtype=int)
    for i, string in enumerate(x):
        if type(string) == str:
            string = string.lower()
        ngrams1 = set()
        for ngram_size in range(ngram_min, ngram_max + 1):
            for index in range(len(string) - ngram_size + 1):
                ngram = string[index: index + ngram_size]
                if type(ngram) != str:
                    ngram = str(ngram)
                ngrams1.add(ngram)
        for j, counterstring in enumerate(y):
            if type(counterstring) == str:
                counterstring = counterstring.lower()
            ngrams2 = set()
            for ngram_size in range(ngram_min, ngram_max + 1):
                for index in range(len(counterstring) - ngram_size + 1):
                    ngram = counterstring[index: index + ngram_size]
                    if type(ngram) != str:
                        ngram = str(ngram)
                    ngrams2.add(ngram)
            result[i, j] = len(ngrams1.intersection(ngrams2))
    return result


def spectrum_kernel(x, y, ngram_min, ngram_max):
    """Calculate the spectrum kernel, Ionescu & Popescu 2017."""
    result = np.zeros((len(x), len(y)), dtype=int)
    for i, string in enumerate(x):
        if type(string) == str:
            string = string.lower()
        ngrams = defaultdict(int)
        for ngram_size in range(ngram_min, ngram_max + 1):
            for index in range(len(string) - ngram_size + 1):
                ngram = string[index: index + ngram_size]
                if type(ngram) != str:
                    ngram = str(ngram)
                ngrams[ngram] += 1
        for j, counterstring in enumerate(y):
            if type(counterstring) == str:
                counterstring = counterstring.lower()
            for ngram_size in range(ngram_min, ngram_max + 1):
                for index in range(len(counterstring) - ngram_size + 1):
                    ngram = counterstring[index: index + ngram_size]
                    if type(ngram) != str:
                        ngram = str(ngram)
                    result[i, j] += ngrams[ngram]
    return result


def intersection_kernel(x, y, ngram_min, ngram_max):
    """Calculate the intersection kernel, Ionescu & Popescu 2017."""
    result = np.zeros((len(x), len(y)), dtype=int)
    for i, string in enumerate(x):
        if type(string) == str:
            string = string.lower()
        ngrams = defaultdict(int)
        for ngram_size in range(ngram_min, ngram_max + 1):
            for index in range(len(string) - ngram_size + 1):
                ngram = string[index: index + ngram_size]
                if type(ngram) != str:
                    ngram = str(ngram)
                ngrams[ngram] += 1
        for j, counterstring in enumerate(y):
            if type(counterstring) == str:
                counterstring = counterstring.lower()
            ngrams2 = dict(ngrams)
            for ngram_size in range(ngram_min, ngram_max + 1):
                for index in range(len(counterstring) - ngram_size + 1):
                    ngram = counterstring[index: index + ngram_size]
                    if type(ngram) != str:
                        ngram = str(ngram)
                    if ngram in ngrams2 and ngrams2[ngram] > 0:
                        result[i, j] += 1
                        ngrams2[ngram] -= 1
    return result


kernel_map = {
    'presence': presence_kernel,
    'spectrum': spectrum_kernel,
    'intersection': intersection_kernel,
}


class StringKernelTransformer(BaseEstimator, TransformerMixin):
    """
    Converts (string) documents to a similarity matrix (kernel).

    Input (fit): List of m strings
    Input (transform): List of n strings
    Output: m x n matrix containing the kernel similarities between the strings
    """

    def __init__(self, kernel_type='intersection', ngram_range=None,
                 normalize=True):
        """
        Initialize the model.

        Args:
            kernel_type: one of 'intersection', 'spectrum' or 'presence'.
            ngram_range: range of n_grams to include
            normalize: whether to normalize the output across the corpus.
        """
        if ngram_range is None:
            ngram_range = (5, 10)
        self.ngram_range = ngram_range
        self.normalize = normalize
        self.kernel_type = kernel_type
        if kernel_type not in kernel_map:
            raise ValueError(f'unknown kernel: {kernel_type}')
        self._kernel = kernel_map[kernel_type]
        self._train_data = None
        self._train_kernel = None

    def fit(self, X, y=None):
        """Fit model."""
        self._train_data = np.array(X)
        self._train_kernel = self._kernel(X, X, *self.ngram_range)
        for i in range(len(X)):
            if self._train_kernel[i, i] == 0:
                logger.error(f'zeros in diagonal at ({i},{i}) for {X[i]}')
        return self

    def transform(self, X, y=None):
        """Transform data."""
        X = np.array(X)
        _st = self._kernel(X, self._train_data, *self.ngram_range)

        if not self.normalize:
            return _st

        _ss = self._train_kernel
        _tt = self._kernel(X, X, *self.ngram_range)

        result = np.copy(_st)
        for i in range(_st.shape[0]):
            if _tt[i, i] == 0:
                logger.error(f'zeros in diagonal at ({i},{i}) for {X[i]}')
            for j in range(_st.shape[1]):
                if _tt[i, i] != 0 and _ss[j, j] != 0:
                    result[i, j] /= np.sqrt(_tt[i, i] * _ss[j, j])

        return result
