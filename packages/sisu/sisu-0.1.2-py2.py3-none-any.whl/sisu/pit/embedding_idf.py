import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from gismo.corpus import Corpus
from gismo.embedding import auto_vect, Embedding, idf_fit, idf_transform, l1_normalize


class IdfEmbedding(Embedding):
    """
    This class leverages the :class:`~sklearn.feature_extraction.text.CountVectorizer`
    class to build the dual embedding of a :class:`~gismo.corpus.Corpus`.

    * Documents are embedded in the space of features;
    * Features are embedded in the space of documents.

    It is almost identical to Gismo's :class:`~gismo.embedding.Embedding` except that there is no ITF weights.

    Parameters
    ----------
    vectorizer: :class:`~sklearn.feature_extraction.text.CountVectorizer`, optional
                Custom :class:`~sklearn.feature_extraction.text.CountVectorizer`
                to override default behavior (recommended).
                Having a :class:`~sklearn.feature_extraction.text.CountVectorizer`
                adapted to the :class:`~gismo.corpus.Corpus` is good practice.
    filename: :py:class:`str`, optional
        If set, load embedding from corresponding file.
    path: :py:class:`str` or :py:class:`~pathlib.Path`, optional
        If set, specify the directory where the embedding is located.
    """
    def __init__(self, vectorizer: CountVectorizer = None, filename=None, path='.'):
        super().__init__(vectorizer, filename, path)
        # if filename is not None:
        #     self.load(filename=filename, path=path)
        # else:
        #     self.vectorizer = vectorizer
        #     self.n = 0  # Number of documents
        #     self.m = 0  # Number of features
        #     self.x = None  # TF-IDTF X embedding of documents into features, normalized
        #     self.x_norm = None  # memory of X norm for hierarchical merge
        #     self.y = None  # Y embedding of features into documents
        #     self.y_norm = None  # memory of Y norm for hierarchical merge
        #     self.idf = None  # idf vector
        #     self.features = None  # vocabulary list
        #     self._result_found = True  # keep track of projection successes

    def fit_transform(self, corpus: Corpus):
        """


        Parameters
        ----------
        corpus

        Returns
        -------

        Examples
        --------
        >>> from gismo.common import toy_source_text
        >>> corpus=Corpus(toy_source_text)
        >>> embedding = IdfEmbedding()
        >>> embedding.fit_transform(corpus)
        >>> embedding.x  # doctest: +NORMALIZE_WHITESPACE
        <5x21 sparse matrix of type '<class 'numpy.float64'>'
            with 25 stored elements in Compressed Sparse Row format>
        >>> embedding.features[:8]
        ['blade', 'chinese', 'comparing', 'demon', 'folklore', 'gizmo', 'gremlins', 'inside']
        """
        if self.vectorizer is None:
            self.vectorizer = auto_vect(corpus)

        # THE FIT PART
        # Start with a simple CountVectorizer X
        x = self.vectorizer.fit_transform(corpus.iterate_text())
        # Release stop_words_ from vectorizer
        self.vectorizer.stop_words_ = None
        # Populate vocabulary
        self.features = self.vectorizer.get_feature_names()
        # Extract number of documents and features
        (self.n, self.m) = x.shape
        # PART OF TRANSFORM, MUTUALIZED: Apply sublinear smoothing
        x.data = 1 + np.log(x.data)
        # Compute transposed CountVectorizer Y
        self.y = x.tocsc()
        # Compute IDF
        self.idf = idf_fit(self.y.indptr, self.n)

        # THE TRANSFORM PART
        idf_transform(indptr=self.y.indptr, data=self.y.data, idf_vector=self.idf)
        # back to x
        self.x = self.y.tocsr(copy=True)
        # Transpose y
        self.y = self.y.T
        # Normalize
        self.x_norm = l1_normalize(indptr=self.x.indptr, data=self.x.data)
        self.y_norm = l1_normalize(indptr=self.y.indptr, data=self.y.data)

    def transform(self, corpus: Corpus):
        """
        Ingest a corpus of documents using existing features.
        Requires that the embedding has been fitted beforehand.

        * TF-IDF embedding of documents is computed and stored.
        * TF-ITF embedding of features is computed and stored.

        Parameters
        ----------
        corpus: :class:`~gismo.corpus.Corpus`
            The corpus to ingest.

        Example
        -------
        >>> from gismo.common import toy_source_text
        >>> corpus=Corpus(toy_source_text)
        >>> embedding = IdfEmbedding()
        >>> embedding.fit_transform(corpus)
        >>> [embedding.features[i] for i in embedding.x.indices[:8]]
        ['gizmo', 'mogwaï', 'blade', 'sentence', 'sentence', 'shadoks', 'comparing', 'gizmo']
        >>> small_corpus = Corpus(["I only talk about Yoda", "Gizmo forever!"])
        >>> embedding.transform(small_corpus)
        >>> [embedding.features[i] for i in embedding.x.indices]
        ['yoda', 'gizmo']
        """
        # The fit part
        assert corpus

        # THE FIT PART
        # Start with a simple CountVectorizer X
        x = self.vectorizer.transform(corpus.iterate_text())
        # Release stop_words_ from vectorizer
        self.vectorizer.stop_words_ = None
        # Extract number of documents and features
        (self.n, _) = x.shape
        # PART OF TRANSFORM, MUTUALIZED: Apply sublinear smoothing
        x.data = 1 + np.log(x.data)
        # Compute transposed CountVectorizer Y
        self.y = x.tocsc()

        # THE TRANSFORM PART
        idf_transform(indptr=self.y.indptr, data=self.y.data, idf_vector=self.idf)
        # back to x
        self.x = self.y.tocsr(copy=True)
        # Transpose y
        self.y = self.y.T
        # Normalize
        self.x_norm = l1_normalize(indptr=self.x.indptr, data=self.x.data)
        self.y_norm = l1_normalize(indptr=self.y.indptr, data=self.y.data)
