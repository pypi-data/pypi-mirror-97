#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#This file is part of newdle
#Copyright © 2020 Nokia Corporation and/or its subsidiary(-ies). All rights reserved. *
#
# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@nokia-bell-labs.com>
#   Mélanie Cambus    <melanie.cambus@nokia.com>

import numpy as np

def make_map_word_id(s :str, map_word_id :dict = None, cur_id :int = None) -> tuple:
    """
    Computes unique indexes for each word of a string.
    Args:
        s: A string correpsponding to a text.
        map_word_id: An existing dict of words and corresponding indexes.
        cur_id: Lowest int not associated to a word yet.
    Returns:
        A dict of words and worresponding indexes, completed with the words of s.
    """
    if map_word_id is None:
        map_word_id = dict() 
        cur_id = 0
    if cur_id is None:
        cur_id = max(map_word_id.values())
    for w in s.lower().split():     
        id = map_word_id.get(w) 
        if id is None: 
            map_word_id[w] = cur_id 
            cur_id += 1
    return (map_word_id, cur_id)

def sentence_to_ids(s :str, map_word_id :dict):
    """
    Computes unique indexes for each word of a sentence.
    Args:
        s: A string correpsponding to a sentence.
        map_word_id: An existing dict of words and corresponding indexes.
    Returns:
        The map_word_id completed with the words of the sentence s.
    """
    return [[map_word_id[w]] for w in s.lower().split()]

class Direction:
    NONE = 0
    N    = 1
    W    = 2
    NW   = 3

    def __str__(self) -> str:
        if   self == Direction.NW: return "NW"
        elif self == Direction.N : return "N"
        elif self == Direction.W : return "W"
        else: return "?"

    def __repr__(self) -> str:
        return self.__str__()

def lcs_length(x :str, y :str) -> tuple:
    """
    Compute the Longest Common Subsequence (LCS) of two input strings.
    Based on:
    Introduction to Algorithms,
    T. H. Cormen, C. E. Leiserson, R. L. Rivest, pp 317

    Args:
        x: an input string (of length m).
        y: an input string (of length n).
    Returns:
        A tuple (c, b) made of two (m + 1) * (n + 1) tensors:
            c: IntTensor such that c[i, j] contains the length of the LCS x[:i] and y[:j]
            b: IntTensor containing the Direction from which b[i, j] is obtained.
    """
    m = len(x) + 1
    n = len(y) + 1

    c = np.zeros((m, n), dtype=np.intc)
    b = np.zeros((m, n), dtype=np.ubyte)

    # Use np.arange to iterate over ints (torch.arange iterates over floats)
    for i in np.arange(1, m):
        for j in np.arange(1, n):
            if x[i - 1] == y[j - 1]:
                # Get c[i, j] from the North-West cell
                c[i, j] = c[i - 1 , j - 1] + 1
                b[i, j] = Direction.NW
            elif c[i - 1, j] >= c[i, j - 1]:
                # Get c[i, j] from the North cell
                c[i, j] = c[i - 1 , j]
                b[i, j] = Direction.N
            else:
                # Get c[i, j] from the West cell
                c[i, j] = c[i , j - 1]
                b[i, j] = Direction.W
    return (c, b)

def lcs_rec(b :np.array, x :str, i :int, j :int, neutral = "") -> str:
    if   i == 0 or j == 0        : return neutral
    if   b[i, j] == Direction.NW : return lcs_rec(b, x, i - 1, j - 1, neutral=neutral) + x[i - 1]
    elif b[i, j] == Direction.N  : return lcs_rec(b, x, i - 1, j    , neutral=neutral)
    elif b[i, j] == Direction.W  : return lcs_rec(b, x, i    , j - 1, neutral=neutral)
    else: raise RuntimeError("b[%d, %d] = %d is invalid" % (i, j , b[i, j]))

def lcs(x :str, y :str, neutral="", b :np.array = None) -> str:
    """
    Compute the LCS of two input strings.
    Args:
        x: A string.
        y: A string.
        b: The IntTensor obtained by (c, b) = lcs_length(x, y).
            Pass None if not yet computed.
    Returns;
        The string containing the corresponding LCS.
    """
    if b is None:
        (_, b) = lcs_length(x, y)
    return lcs_rec(b, x, len(x), len(y), neutral=neutral)

def my_lcs(ri :str, c :str) -> list:
    sentences = [ri, c]
    map_word_id = None
    cur_id = None
    for s in sentences:
        (map_word_id, cur_id) = make_map_word_id(s, map_word_id, cur_id)
    sequences = [sentence_to_ids(s, map_word_id) for s in sentences]
    return lcs(sequences[0], sequences[1], neutral = list())
