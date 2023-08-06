#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of newdle
# Copyright © 2020 Nokia Corporation and/or its subsidiary(-ies). All rights reserved. *
#
# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@nokia-bell-labs.com>
#   Mélanie Cambus    <melanie.cambus@nokia.com>

from sisu.preprocessing.tokenizer import make_sentences

toy_article = {'title': "Predator",
               'abstract': "In the jungle, no-one hears you far cry. And vice-versa. "
                           "They say to make a long abstract, with the number 42 in it, so here I am.",
               'content': "There is no-one in the trees. Is there? Predators don't like to lose."}
"""
Article with a simple structure.
"""


# À utiliser ssi abstract est une liste, sinon compte la longueur de la chaîne et renvoie une exception


# Used only to initialize the embedding -> all the unwanted symbols can be taken out

def make_abstract_sentences(document: dict) -> list:
    """
    Cuts a document's abstract into sentences when the document is a dict with the key abstract.

    Parameters
    ----------
    document: :class:`dict`
        Simplified document.

    Returns
    -------
    :class:`list`
        Document's abstract's sentences.

    Examples
    --------

    >>> make_abstract_sentences(toy_article) # doctest: +NORMALIZE_WHITESPACE
    ['In the jungle, no-one hears you far cry.', 'And vice-versa.',
     'They say to make a long abstract, with the number 42 in it, so here I am.']
    """
    return make_sentences(document["abstract"])


def make_content_sentences(document: dict) -> list:
    """
    Cuts a document's content into sentences when the document is a dict with the key content.

    Parameters
    ----------
    document: :class:`dict`
        Simplified document.

    Returns
    -------
    :class:`list`
        Document's content's sentences.

    Examples
    --------

    >>> make_content_sentences(toy_article)
    ['There is no-one in the trees.', 'Is there?', "Predators don't like to lose."]
    """
    return make_sentences(document["content"])
