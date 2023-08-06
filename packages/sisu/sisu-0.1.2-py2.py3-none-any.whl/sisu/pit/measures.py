#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of newdle
# Copyright © 2020 Nokia Corporation and/or its subsidiary(-ies). All rights reserved. *
#
# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@nokia-bell-labs.com>
#   Mélanie Cambus    <melanie.cambus@nokia.com>

# Precision : intersection over card(summary)

import numpy as np
import matplotlib.pyplot as plt
from gismo.embedding import Embedding
from nltk import skipgrams
from sisu.pit.lcs import my_lcs
from sisu.preprocessing.tokenizer import make_sentences, words


def precision(summary: str, ref: str, vocab: set = None) -> float:
    """
    Computes the precision value of a summary
    Args:
        summary: A `str` corresponding to a summary we want to evaluate.
        ref: A `str` corresponding to a reference summary we use to evaluate.
        vocab: A `set` of `str` corresponding to the words we want to take into account for the evaluation.
    Returns:
        A `float` between 0 and 1 giving the precision.
    """
    vocab_summary = set(words(summary))
    vocab_ref = set(words(ref))
    if vocab is not None:
        return len(vocab_summary & vocab_ref & vocab) / len(vocab_summary & vocab)
    else:
        return len(vocab_summary & vocab_ref) / len(vocab_summary)


# Recall : intersection over card(ref)
def recall(summary: str, ref: str, vocab: set = None) -> float:
    """
    Computes the recall value of a summary
    Args:
        summary: A `str` corresponding to a summary we want to evaluate.
        ref: A `str` corresponding to a reference summary we use to evaluate.
        vocab: A `set` of `str` corresponding to the words we want to take into account for the evaluation.
    Returns:
        A `float` between 0 and 1 giving the recall.
    """
    vocab_summary = set(words(summary))
    vocab_ref = set(words(ref))
    if vocab is not None:
        return len(vocab_summary & vocab_ref & vocab) / len(vocab_ref & vocab)
    else:
        return len(vocab_summary & vocab_ref) / len(vocab_ref)


# F-score : harmonic mean with factor beta
def F_score(summary: str, ref: str, beta: float = 1, vocab: set = None) -> float:
    """
    Computes the Fscore of a summary
    Args:
        summary: A `str` corresponding to a summary we want to evaluate.
        ref: A `str` corresponding to a reference summary we use to evaluate.
        beta: a `float` giving the importance of the precision in comparision to the recall.
        vocab: A `set` of `str` corresponding to the words we want to take into account for the evaluation.
    Returns:
        A `float` between 0 and 1 giving the Fscore.
    """
    return ((1 + beta ** 2) * precision(summary, ref) * recall(summary, ref)) / \
           (recall(summary, ref) + (beta ** 2 * precision(summary, ref)))


def make_gram(summary: str, n: int) -> set:
    """
    Extracts the ngrams of a text
    Args:
        summary: A `str` corresponding to a summary we want the ngrams from.
        n: An `int` giving the length of the ngrams.
    Returns:
        A `set` of `str` corresponding to the ngrams of the summary.
    """
    sum_vocab = summary.split(" ")
    return set(" ".join(sum_vocab[i:i + n]) for i in range(0, len(sum_vocab) - n + 1))


# ROUGE-1 is simply a recall, without any given vocabulary (with stop-words & cie)
def rouge_n(summary: str, ref: str, n: int = 1) -> float:
    """
    Computes the ROUGE-n score of a summary, recall measure with ngrams.
    Args:
        summary: A `str` corresponding to a summary we want to evaluate.
        ref: A `str` corresponding to a reference summary we use to evaluate.
    Returns:
        A `float` between 0 and 1 giving the ROUGE-n score.
    """
    if n == 1:
        return recall(summary, ref)
    else:
        ngrams = make_gram(ref, n)
        if ngrams:
            return len(make_gram(summary, n) & ngrams) / len(ngrams)
        else:
            return 0


def rouge_l(summary: str, ref: str, beta: float = 1) -> float:
    """
    Computes the ROUGE-L score of a summary, F-score with LCS
    Args:
        summary: A `str` corresponding to a summary we want to evaluate.
        ref: A `str` corresponding to a reference summary we use to evaluate.
        beta: a `float` giving the importance of the precision in comparision to the recall.
    Returns:
        A `float` between 0 and 1 giving the ROUGE-L score.
    """
    ref_sentences = make_sentences(ref)
    sum_sentences = make_sentences(summary)
    sum_lcs = 0
    for ref_sentence in ref_sentences:
        sum_lcs += len(my_lcs(ref_sentence, summary)) / len(words(ref_sentence))
    vocab_summary = words(summary)
    vocab_ref = words(ref)
    p = sum_lcs / len(sum_sentences)
    r = sum_lcs / len(ref_sentences)
    if r != 0 or p != 0:
        return ((1 + beta ** 2) * p * r) / (r + (beta ** 2 * p))
    else:
        return 0


# skipgrams(text, n, k) computes the skip-ngrams of the text with C(k, n) combinations (here n<k)
# it returns them as a list of tuples, the text given is a list of words

def rouge_s(summary: str, ref: str, beta: float = 1) -> float:
    """
    Computes the ROUGE-S score of a summary, ROUGE-2 score with skip-bigrams
    Args:
        summary: A `str` corresponding to a summary we want to evaluate.
        ref: A `str` corresponding to a reference summary we use to evaluate.
        beta: a `float` giving the importance of the precision in comparision to the recall.
    Returns:
        A `float` between 0 and 1 giving the ROUGE-S score.
    """
    vocab_summary = words(summary)
    vocab_ref = words(ref)
    summary_skip2 = set(skipgrams(vocab_summary, 2, len(vocab_summary)))
    ref_skip2 = set(skipgrams(vocab_ref, 2, len(vocab_ref)))
    if len(ref_skip2) == set() or summary_skip2 == set():
        return 0
    p = len(summary_skip2 & ref_skip2) / len(summary_skip2)
    r = len(summary_skip2 & ref_skip2) / len(ref_skip2)
    if r != 0 or p != 0:
        return ((1 + beta ** 2) * p * r) / (r + (beta ** 2 * p))
    else:
        return 0


def make_rouge_scores(summaries: list, candidate_key: str, ref_key: str) -> dict:
    """
    Computes ROUGE scores for a list of candidate summaries and the corresponding reference summaries
    Args:
        summaries: A `list` of dictionnaries.
        candidate_key: A string corresponding to the candidate summary in the dictionnaries.
        ref_key: A string corresponding to the reference summary in the dictionnaries.
    Returns:
        A dictionnary containing a list for each score
    """
    scores = {
        "rouge-1": list(),
        "rouge-2": list(),
        #        "rouge-3" : list(),
        #        "rouge-4" : list(),
        "rouge-l": list(),
        "rouge-s": list()
    }
    for (index_d, summaries) in enumerate(summaries):
        hypothesis = summaries[candidate_key]
        abstract = summaries[ref_key]
        scores["rouge-1"].append(rouge_n(hypothesis, abstract, 1))
        scores["rouge-2"].append(rouge_n(hypothesis, abstract, 2))
        #        scores["rouge-3"].append(rouge_n(hypothesis, abstract, 3))
        #        scores["rouge-4"].append(rouge_n(hypothesis, abstract, 4))
        scores["rouge-l"].append(rouge_l(hypothesis, abstract, beta=1))
        scores["rouge-s"].append(rouge_s(hypothesis, abstract, beta=1))
    return scores


# Cosine similarity
def cosine_sim(p: np.ndarray, q: np.ndarray) -> float:
    """
    Computes the cosine similarity between two arrays (vectors) of the same size
    Args:
        p: An array
        q: An array
    Returns:
        The scalar product of the two vectors.
    """
    return float(p.dot(np.transpose(q)))


# Extended Jaccard simialrity
def extended_jaccard(p: np.ndarray, q: np.ndarray) -> float:
    """
    Computes the extended Jaccard similarity between two arrays (vectors) of the same size
    Args:
        p: An array
        q: An array
    Returns:
        The extended Jaccard similarity of the two vectors.
    """
    scal_prod = cosine_sim(p, q)
    return scal_prod / (np.linalg.norm(p) ** 2 + np.linalg.norm(q) ** 2 - scal_prod)


# Computing scores
def make_scores(
    summaries: list,
    candidate_key: str,
    ref_key: str,
    evaluation_method,
    embedding: Embedding
) -> list:
    """
    Computes scores with a certain evaluation method for a list of candidate summaries and the corresponding reference summaries
    Args:
        summaries: A `list` of dictionnaries.
        candidate_key: A string corresponding to the candidate summary in the dictionnaries.
        ref_key: A string corresponding to the reference summary in the dictionnaries.
        evaluation_lethod: A function that computes the score (float from two vectors).
        embedding: An Embedding that will allow us to get the representative vectors of the summaries
    Returns:
        A list containing the score of each summary.
    """
    measures = list()
    for summarie in summaries:
        candidate_vect = (embedding.query_projection(summarie[candidate_key]))[0].toarray()
        ref_vect = (embedding.query_projection(summarie[ref_key]))[0].toarray()
        dim = np.size(ref_vect)
        measures.append(evaluation_method(candidate_vect.reshape(dim), ref_vect.reshape(dim)))
    return measures


# Divergence KL
def smoothing_distrib(p: np.ndarray, smallest_float: float = 5e-324) -> np.ndarray:
    """
    Computes a "smoothed" version of an array, representing a probability distribution, without zero elements.
    Args:
        p: An array representing a probability distribution.
        smallest_float: A float corresponding to the smallest value that can be used.
    Returns:
        An array without zero elements (corresponding to the smoothed distribution.
    """
    dim_p = np.size(p)
    is_positive = np.greater(p, np.zeros(dim_p)).astype(float)
    num_pos_elements = np.sum(is_positive)

    to_add = smallest_float
    to_sub = to_add / num_pos_elements

    is_positive[is_positive == True] = -to_sub
    is_positive[is_positive == False] = to_add

    return np.add(is_positive, p)


def div_kl(p: np.ndarray, q: np.ndarray, smallest_float: float = 5e-324) -> float:
    """
    Computes the KL divergence of an array representing a probability distribution from another.
    Args:
        p: An array representing a probability distribution.
        q: An array representing the probability distribution that p is compared to.
    Returns:
        A float corresponding to the KL divergence of p from q.
    """
    p = smoothing_distrib(p, smallest_float=smallest_float)
    q = smoothing_distrib(q, smallest_float=smallest_float)
    return sum(np.multiply(p, np.log(np.divide(p, q))))


# Plotting scores
def make_scores_plot(scores_gismo: list, scores_textrank: list, score_name: str):
    """
    Plots two lists of scores.
    Args:
        scores_gismo: A list of scores.
        scores_textrank: A list of scores.
        score_name: A string corresponding to the score name.
    """
    x_axes = [i for i in range(0, len(scores_gismo))]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    plt.xlabel("Documents", fontsize="x-large")
    plt.ylabel(score_name, fontsize="x-large")
    plt.title("TextRank vs Gismo summarizer ", fontsize="x-large")

    ax.plot(x_axes, scores_gismo, "g2", label="Gismo summary")
    ax.plot(x_axes, scores_textrank, "b.", label="Textrank summary")

    legend = ax.legend(loc="upper right", fontsize="x-large")
    plt.show()


def make_diff_scores_plot(scores_gismo: list, scores_textrank: list, score_name: str, num_documents: int,
                          save: bool = True):
    """
    Plots the difference between two scores (can be saved into a file).
    Args:
        scores_gismo: A list of scores.
        scores_textrank: A list of scores.
        score_name: A string corresponding to the score name.
        num_documents: An int corresponding to the number of non-empty summaries' scores.
        save: A bool corresponding to the saving option, if true the figure is saved into a file.
    """

    x_vect = [i for i in range(0, len(scores_gismo))]
    x_axes = [(100 / len(scores_gismo)) * i for i in x_vect]
    y_axes = [scores_gismo[i] - scores_textrank[i] for i in range(len(scores_gismo))]
    y_axes.sort()

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    # plt.xlabel("pourcentage de documents") in figure comment
    plt.ylabel(score_name, fontsize="x-large")
    plt.title("Scores differences between summaries generated by us and Textrank on %d documents" % num_documents,
              fontsize="x-large")

    plt.ylim(- (max(scores_gismo) + max(scores_textrank)), max(scores_gismo) + max(scores_textrank))
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")
    ax.xaxis.set_ticks_position("bottom")
    ax.spines["bottom"].set_position(("data", 0))
    ax.yaxis.set_ticks_position("left")
    ax.spines["left"].set_position(("data", 0))

    ax.plot(x_axes, y_axes, label="Delta between methods", alpha=1.0, color="green")
    if score_name == "Kullback-Leibler Divergence":
        position1 = np.less(np.array(y_axes), np.zeros(np.size(y_axes)))
        position2 = np.greater(np.array(y_axes), np.zeros(np.size(y_axes)))
    else:
        position1 = np.greater(np.array(y_axes), np.zeros(np.size(y_axes)))
        position2 = np.less(np.array(y_axes), np.zeros(np.size(y_axes)))

    plt.fill_between(
        x_axes,
        y_axes,
        where=position1,
        color='blue',
        alpha=0.25,
        label="Our summarizer gets better scores"
    )
    plt.fill_between(
        x_axes,
        y_axes,
        where=position2,
        color='red',
        alpha=0.25,
        label="TextRank gets better scores"
    )
    legend = ax.legend(loc="lower right", fontsize="x-large")
    if save:
        path = "results/quality/%s.svg" % score_name
        plt.savefig(path)
    plt.show()
