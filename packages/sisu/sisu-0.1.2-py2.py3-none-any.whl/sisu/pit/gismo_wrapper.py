import copy
import re
from pprint import pprint
from gismo.corpus import Corpus
from gismo import Gismo
from functools import partial
from sklearn.feature_extraction.text import CountVectorizer
from gismo.embedding import Embedding
from sisu.preprocessing.covid19 import get_title, get_abstract, get_content, make_clean_doc

COVID19_TEXT_GETTERS = {
    "title": get_title,
    "abstract": get_abstract,
    "content": get_content,
}
"""Getters for the covid dataset. MOVE TO COVID SUBMODULE."""

RE_NOISE = re.compile(r"[,.:;()0-9+=%\[\]_]")
"""regexp for useless text."""

RE_EMAIL = re.compile("https?://[a-zA-Z.:0-9]+|www.[a-zA-Z.:0-9]+.*|www.|.org|[a-zA-Z.:0-9]+/")
"""regexp for email detection."""

RE_REFERENCE = re.compile(r"\[\d+,\s\d+\]|\[\d+\]|\(\d+,\s\d+\)|\(\d+\)")
"""regexp for citations."""


def simplified_document_to_string(doc: dict) -> str:
    """
    Transforms a dict into a string made of its values.

    Parameters
    ----------
    doc: :class:`dict`
        A `dict` representing a document of "depth one", all the values are strings.

    Returns
    -------
    :class:`str`
        Concatenation of `doc` values.

    Examples
    --------

    >>> from sisu.preprocessing.sentences import toy_article
    >>> simplified_document_to_string(toy_article)
    "Predator In the jungle, no-one hears you far cry. And vice-versa. They say to make a long abstract, with the number 42 in it, so here I am. There is no-one in the trees. Is there? Predators don't like to lose."
    """
    return " ".join([str(value) for value in doc.values()])


def sanitize_text(text: str) -> str:
    """
    Sanitize a text. This is done to improve the Embedding quality.

    Parameters
    ----------
    text: :class:`str`
        Text to clean.

    Returns
    -------
    :class:`str`
        The corresponding sanitized `str` instance.

    Examples
    --------
    >>> sanitize_text("This is a mail: santa@northpole.com!")
    'This is a mail santa@northpolecom!'
    >>> sanitize_text("This is a !*[ url: https://www.ens.fr!")
    'This is a !* url /'
    >>> sanitize_text("This are references [3, 17].")
    'This are references  '
    """
    for r in [RE_NOISE, RE_EMAIL, RE_REFERENCE]:
        text = r.sub("", text)
    return text


def document_to_text(document: dict, text_getters=None) -> str:
    """
    NOT WORKING

    Convert a document (e.g. from COVID-19 dataset) to a string.

    Parameters
    ----------
    document: :class:`dict`
        A simplified COVID-19 document.
    text_getters: :class:`dict`, optional
        CODE USES LIST NOT DICT THIS FUNCTION SHOULD PROBABLY BE REMOVED


    Returns
    -------
        The `str` representing the input document.

    Examples
    --------

    NO EXAMPLE, REMOVE THIS FUNCTION.
    """
    if text_getters is None:
        text_getters = COVID19_TEXT_GETTERS
    return "\n".join([sanitize_text(text_getter(document)) for text_getter in text_getters])


def make_gismo(
    documents: list,
    alpha: float = .2,
    other_embedding: Embedding = None,
    is_documents_embedding: bool = False,
    document_to_text=simplified_document_to_string  # All the values by default
) -> Gismo:
    """
    Make a Gismo object from a list of documents.
    Args:
        documents: A `list` of documents with strings in the values.
        alpha: A `float` in [0, 1] indicating the damping factor used in the D-iteration used by Gismo.
        other_embedding: embedding already fitted on a corpus.
        document_to_text: Callback(Document) -> str.
    Returns:
        A Gismo object made from the given documents and embedding.
    """

    def post_document(gismo: Gismo, i: int) -> dict:
        document = gismo.corpus[i]
        return document

    #    print("corpus")
    corpus = Corpus(documents, document_to_text)
    if other_embedding is None:
        #        print("vectorizer")
        vectorizer = CountVectorizer(dtype=float)
        embedding = Embedding(vectorizer=vectorizer)
        #        print("fit_transform")
        embedding.fit_transform(corpus)
    else:
        if is_documents_embedding:
            embedding = Embedding()
            embedding = copy.copy(other_embedding)
        else:
            embedding = Embedding()
            #            print("fit_ext")
            embedding.fit_ext(other_embedding)
            #            print("transform")
            embedding.transform(corpus)
    #    print("gismo")
    gismo = Gismo(corpus, embedding)
    gismo.post_document = post_document
    gismo.diteration.alpha = alpha

    return gismo


def old_make_gismo(
    documents: list,
    alpha: float = .2,
    other_embedding: Embedding = None,
    is_documents_embedding: bool = False,
    document_to_text=simplified_document_to_string  # All the values by default
) -> Gismo:
    """
    Make a Gismo object from a list of documents.
    Args:
        documents: A `list` of documents with strings in the values.
        alpha: A `float` in [0, 1] indicating the damping factor used in the D-iteration used by Gismo.
        other_embedding: embedding already fitted on a corpus.
        document_to_text: Callback(Document) -> str.
    Returns:
        A Gismo object made from the given documents and embedding.
    """

    def post_document(gismo: Gismo, i: int) -> dict:
        document = gismo.corpus[i]
        return document

    #    print("corpus")
    corpus = Corpus(documents, document_to_text)
    if other_embedding is None:
        #        print("vectorizer")
        vectorizer = CountVectorizer(dtype=float)
        embedding = Embedding(vectorizer=vectorizer)
        #        print("fit_transform")
        embedding.fit_transform(corpus)
    else:
        if is_documents_embedding:
            embedding = Embedding()
            embedding = copy.copy(other_embedding)
        else:
            embedding = Embedding()
            #            print("fit_ext")
            embedding.fit_ext(other_embedding)
            #            print("transform")
            embedding.transform(corpus)
    #    print("gismo")
    gismo = Gismo(corpus, embedding)
    gismo.post_document = post_document
    gismo.diteration.alpha = alpha

    return gismo


# An enbedding on bigger corpus and the right stop_words is preferable
def initialize_embedding(
    documents: list,
    stop_words: list = None,
    max_ngram: int = 1,
    min_df: float = 0.02,
    max_df: float = 0.85,
    document_to_text=simplified_document_to_string,  # All the values by default
    preprocessor=None
) -> Embedding:
    """
    Initializes an embedding, fitting it from documents

    Parameters
    ----------
    documents:
        A `list` of `dict` representing documents with strings in the values.
    stop_words:
        A `list` of words to ignore in the vocabulary.
    max_ngram:
        the maximum length of ngrams to take into account (e.g. 2 if bigrams in vocabulary).
    min_df:
        minimum frequency of a word to be considered in the vocabulary,
        if an int the word must be contained in at least min_df documents.
    max_df: maximum frequency of a word to be considered in the vocabulary.
    document_to_text:
        Callback(Document) -> str.
    preprocessor:

    Returns
    -------
    Embedding:
        The embedding fitted on the documents.
    """
    corpus = Corpus(documents, document_to_text)
    vectorizer = CountVectorizer(
        dtype=float,
        stop_words=stop_words,
        ngram_range=(1, max_ngram),
        min_df=min_df,
        max_df=max_df,
        preprocessor=preprocessor
    )
    embedding = Embedding(vectorizer=vectorizer)
    embedding.fit_transform(corpus)
    return embedding
