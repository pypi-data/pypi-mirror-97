# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@nokia-bell-labs.com>
#   Mélanie Cambus    <melanie.cambus@nokia.com>
#   Fabien Mathieu    <fabien.mathieu@normalesup.org>

# Precision : intersection over card(summary)

# Getting words from a text without symbols

import re
from nltk import tokenize


NO_END_SENTENCE = {"al.", "i.e.", "e.g.", "resp.", "fig.", "ie.", "eg.", "(fig."}
"""
Words ending with a dot that do not indicate the end of a sentence.
"""


def words(text):
    """
    Makes the vocabulary (words) constituting a text.

    Parameters
    ----------
    text: :class:`str`
        A :class:`str` corresponding to a text.

    Returns
    -------
    :class:`list`
        A list of :class:`str` corresponding to the vocabulary (list of lower cases words).

    Examples
    --------
    >>> words("Hello world!")
    ['hello', 'world']

    >>> words("1+one = TWO")
    ['one', 'two']
    """
    return [w for w in (
        re.sub(r"[^A-Za-z]+", "", word.lower())  # Removing punctuation, numbers and math symbols
        for word in text.split(" ")
    ) if w]


def make_sentences(text, no_end_words=None):
    """
    Extract sentences from a text.

    Parameters
    ----------
    text: :class:`str`
        A :class:`str` corresponding to a full text.
    no_end_words: :class:`set`, optional
        A :class:`set` of words that could wrongfully trigger end of sentence.

    Returns
    -------
    :class:`list`
        A list of :class:`str` corresponding to the text's sentences.

    Examples
    --------

    >>> make_sentences("One sentence, i.e. words with no dot, as Toto and al. say. Or no (cf fig. 2)?")
    ['One sentence, i.e. words with no dot, as Toto and al. say.', 'Or no (cf fig. 2)?']
    """
    if no_end_words is None:
        no_end_words = NO_END_SENTENCE
    sentences = tokenize.sent_tokenize(text.replace("·", ". "))
    s_index = 0
    while s_index + 1 < len(sentences) and len(sentences) > 1:
        sentence = sentences[s_index]
        last_word = sentence.rsplit(maxsplit=1)[-1].lower()
        if last_word in no_end_words:
            sentences[s_index] = " ".join([sentence, sentences[s_index + 1]])
            sentences.pop(s_index + 1)
        else:
            s_index += 1
    return sentences


def make_sentences_wiki(text, no_end_words=None) -> list:
    """
    Extract sentences from a text, with wiki code handling.

    Parameters
    ----------
    text: :class:`str`
        A :class:`str` corresponding to a full text.
    no_end_words: :class:`set`, optional
        A :class:`set` of words that could wrongfully trigger end of sentence.

    Returns
    -------
    :class:`list`
        A list of :class:`str` corresponding to the text's sentences.

    Examples
    --------

    >>> make_sentences_wiki("and hyraxes.== Name and taxonomy ==")
    ['and hyraxes ', ' Name and taxonomy ==']
    """
    sentences = make_sentences(text=text, no_end_words=no_end_words)

    new_sentences = list()

    for index, sentence in enumerate(sentences):
        replacements = ('.==', '.===', '.====')
        for r in replacements:
            sentence = sentence.replace(r, ' . ')
        true_sentence = sentence.split(". ")
        new_sentences += true_sentence
    return new_sentences


def num_words(sentence: str) -> int:
    """
    Gets the length of a sentence in number of words

    Parameters
    ----------
    sentence: :class:`str`
        Text to count.

    Returns
    -------
    :class:`int`
        Number of words in sentence.

    Examples
    --------

    >>> num_words("My Taylor is rich!")
    4
    """
    return len(words(sentence))
