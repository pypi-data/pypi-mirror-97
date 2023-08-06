#!/usr/http://localhost:8888/edit/notebooks/summarizer/language_filtering.py#bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of newdle
# Copyright © 2020 Nokia Corporation and/or its subsidiary(-ies). All rights reserved. *
#
# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@nokia-bell-labs.com>
#   Mélanie Cambus    <melanie.cambus@nokia.com>

import copy, re, scipy, spacy
import sys

import numpy as np
# from sklearn.metrics.pairwise    import cosine_similarity
from sknetwork.clustering import Louvain
from scipy import sparse
# from summarizer.embedding_idf    import IdfEmbedding
from gismo import Gismo
from gismo.embedding import Embedding
from sklearn.metrics.pairwise import cosine_similarity
from sisu.pit.building_summary import is_relevant_sentence, RE_CITATION, RE_URL
from sisu.pit.gismo_wrapper import make_gismo
from sisu.preprocessing.tokenizer import num_words, make_sentences_wiki

# try:
#     import neuralcoref
#
#     nlp = spacy.load("en_core_web_sm")
#     try:
#         neuralcoref.add_to_pipe(nlp)
#         print("neuralcoref is installed in spacy pipeline :-)")
#     except ValueError:
#         print("neuralcoref is not installed in spacy pipeline")
# except ImportError:
#     print(
#         "\n".join([
#             "Please neuralcoref:",
#             "sudo pip3 install neuralcoref"
#         ]),
#         file=sys.stderr
#     )


def get_structure_from_gismo_cluster(gismo, cluster, depth=3):
    """
    Builds a tree structure from Gismo clusterising method.
    Args:
        gismo: A `Gismo` object used for the clustering.
        cluster: The root Cluster of the tree, returned by `gismo.get_clustered_features`
    Returns:
        A `dict` representing the tree structure.
    """

    if depth == 0:
        members = [gismo.embedding.features[indice] for indice in cluster.members]
        return {
            "members": members,
            "title": [
                         gismo.embedding.features[i]
                         for i in gismo.diteration.y_order
                         if gismo.embedding.features[i] in members
                     ][:10],
            "text": "",
            "centroid": sum([gismo.embedding.query_projection(member)[0] for member in members]),  # word_centroid
            "siblings_centroids": list(),
            "children": []
        }

    members = [gismo.embedding.features[indice] for indice in cluster.members]
    return {
        "members": members,
        "title": [
                     gismo.embedding.features[i]
                     for i in gismo.diteration.y_order
                     if gismo.embedding.features[i] in members
                 ][:10],
        "text": "",
        "centroid": sum([gismo.embedding.query_projection(member)[0] for member in members]),  # word_centroid
        "siblings_centroids": list(),
        "children": [get_structure_from_gismo_cluster(gismo, c, depth - 1) for c in cluster.children]
    }


def make_siblings_centroids(root):
    """
    Computes the centroids of siblings clusters and directly modifies the structure.
    Args:
        root: The root Cluster of the tree that in which we want to compute the siblings centroids
    """

    def remove_elt_csr_list(csr_list: list, elt) -> list:
        return [csr for csr in csr_list if not (csr - elt).nnz == 0]

    queue = []
    visited = []
    queue.append(root)
    visited.append(root)
    while queue:
        node = queue.pop(0)
        tmp_siblings_centroids = [child["centroid"] for child in node["children"]]
        for child in node["children"]:
            child["siblings_centroids"] = copy.copy(tmp_siblings_centroids)
            child["siblings_centroids"] = remove_elt_csr_list(
                child["siblings_centroids"],
                child["centroid"]
            )

            if child not in visited:
                visited.append(child)
                queue.append(child)


class Node:
    """
    Object representing a node of a tree needed for hierarchical summaries

    Atributes:
        members: elements of the node/cluster
        title: the string that will represent the node/cluster
        centroid: csr_matrix representing the centroid of the node/cluster
        siblings_centroid: list of centroid of siblings nodes/clusters
        children: list of Nodes, children of this node
        tf: frequences of a list of keywords in the subtree whose root is self
    """

    def __init__(self):
        self.members = list()
        self.title = ""
        self.text = ""
        self.centroid = None
        self.siblings_centroids = None
        self.children = list()
        self.tf = list()

    def make_structure(self):
        return {
            "members": self.members,
            "title": self.title,
            "text": self.text,
            "centroid": self.centroid,
            "siblings_centroids": self.siblings_centroids,
            "children": [child.make_structure() for child in self.children]
        }

    def __delete__(self):
        del self.members
        del self.title
        del self.text
        del self.centroid
        del self.siblings_centroids
        del self.children
        del self.tf
        del self
        print("Node deleted")


def make_structure_louvain_gismo_embedding(
    gismo,
    tree,
    keywords_indexes,
    root=True,
    depth=3
):
    """
    Builds a tree structure from Louvain clusterising method
    Args:
        gismo: the gismo built from the dataset
        tree: the empty node that will contain
        keywords_indexes:
        root:
        depth:
    Returns:
        None, it fills in the empty note that is given at first recursively
    """

    # À la racine, tous les mots sont dans le cluster
    if root:
        tree.members = [gismo.embedding.features[indice] for indice in keywords_indexes]
        tree.centroid = sum([gismo.embedding.query_projection(member)[0] for member in tree.members])
        tree.title = " ".join([
                                  gismo.embedding.features[i]
                                  for i in gismo.diteration.y_order
                                  if gismo.embedding.features[i] in tree.members
                              ][:10])

    if depth == 0 or len(tree.members) == 1:
        return None

    # Clustering des membres
    words_vectors = gismo.embedding.y[keywords_indexes, :]
    words_adjacency = cosine_similarity(words_vectors, dense_output=False)
    # words_adjacency.setdiag(scipy.zeros(len(keywords_indexes)))

    # à initialiser avant le premier appel de fonction pour ne pas le refaire plusieurs fois ?
    louvain = Louvain()
    labels = louvain.fit_transform(words_adjacency)
    labels_unique, counts = np.unique(labels, return_counts=True)

    # Il y a autant d'enfants que de clusters
    children = [Node() for i in range(len(labels_unique))]
    for l in labels_unique:  # on remplit members de chaque dico
        words_indexes = keywords_indexes[np.where(labels == l)]
        words = [gismo.embedding.features[word_index] for word_index in words_indexes]
        children[l].members = words
        children[l].centroid = sum([gismo.embedding.query_projection(word)[0] for word in words])
        children[l].title = " ".join([
                                         gismo.embedding.features[i]
                                         for i in gismo.diteration.y_order
                                         if gismo.embedding.features[i] in words
                                     ][:10])
    tree.children = children

    for child in tree.children:
        make_structure_louvain_gismo_embedding(
            gismo,
            child,
            np.array([gismo.embedding.features.index(word) for word in child.members]),
            root=False,
            depth=depth - 1
        )


def is_relevant_sentence(sentence: str, min_num_words: int = 5, max_num_words: int = 60) -> bool:
    n = num_words(sentence)
    # parsed_sentence = nlp(sentence)
    return (
        min_num_words <= n
        and n <= max_num_words
        and re.search(RE_CITATION, sentence) is None
        and re.search(RE_URL, sentence) is None
        #    and "VBZ" in {token.tag_ for token in parsed_sentence}
    )


def summarize_cluster(
    documents: list,
    centroid,  # csr_matrix
    siblings_centroids,  # csr_matrix
    query: str = "",
    num_documents: int = None,
    num_sentences: int = None,
    ratio: float = 0.05,
    embedding: Embedding = None,
    is_documents_embedding: bool = False,
    num_keywords: int = 15,
    size_generic_query: int = 5,
    used_sentences: set = None,
    filter_sentences=is_relevant_sentence,
    get_content=lambda x: x["content"] + x["summary"]
) -> tuple:
    """
    Extended summarizer that produces a list of sentences and a list of keywords.
    Args:
        documents: A list of dict corresponding to documents.
        query: A string.
        num_documents: An int corresponding to the number of top documents
                        to be taking into account for the summary.
        num_sentences: An int corresponding of the number of sentences wanted in the summary.
        ratio: A float in [0, 1] giving the length of the summary
                as a proportion of the length of the num_documents kept.
        embedding: An Embedding fitted on a bigger corpus than documents.
        num_keywords: An int corresponding to the number of keywords returned
        used_sentences: A set of "forbidden" sentences.
        filter_sentences: A function returning a bool, allowing the selection of a sentence.
        get_content: A function that allows the retrieval of a document's content.
        centroid: the centroid of the cluster that is summarized.
        centroid_siblings: the siblings centroids of the cluster that is summarized.
    Returns:
        A tuple containing:
            A list of the summary sentences,
            A list of keywords.
    """
    nlp = spacy.load('en_core_web_sm')

    assert num_sentences or ratio
    assert type(documents) == list

    if used_sentences is None:
        used_sentences = set()

    # Get number of documents
    if num_documents is None:
        num_documents = len(documents)
    else:
        num_documents = min(len(documents), num_documents)

    # Find best documents
    #    start_time = time.clock()
    assert num_documents != 0
    if num_documents == 1:
        best_documents = [documents[0]]

    else:
        documents_gismo = make_gismo(
            documents=documents,
            other_embedding=embedding,
            is_documents_embedding=is_documents_embedding
        )
        documents_gismo.rank(query)
        best_documents = documents_gismo.get_documents_by_rank(k=num_documents)
        if query == "":
            query = " ".join(documents_gismo.get_features_by_rank(k=size_generic_query))
    #    print("finding best documents : ", time.clock() - start_time)
    # Split best document into sentences.
    #    start_time = time.clock()
    contents_sentences = [
        sentence
        for document in best_documents
        for sentence in make_sentences_wiki(get_content(document))
    ]

    assert contents_sentences is not None

    #    print("Splitting best docs in sentences : ", time.clock() - start_time)
    # Scale the number of sentences proportionally to the total number
    # of sentences in the top documents.
    if num_sentences is None:
        num_sentences = max(int(ratio * len(contents_sentences)), 1)

    streching_for_duplicates = 7

    # Computation of the score and selection of sentences
    if siblings_centroids is not None:
        number_of_siblings = len(siblings_centroids)
    else:
        number_of_siblings = 0
    summary = sorted(
        [
            {
                "sentence": contents_sentences[i],
                "index": i,
                "score": 2 * (number_of_siblings + 1) * cosine_similarity(
                    embedding.query_projection(contents_sentences[i])[0],
                    centroid
                ) - sum([
                    cosine_similarity(
                        embedding.query_projection(contents_sentences[i])[0],
                        siblings_centroids[sibling_index]
                    )
                    for sibling_index in range(number_of_siblings)
                ])
            }
            for i in range(len(contents_sentences))
            if is_relevant_sentence(contents_sentences[i]) and \
               (contents_sentences[i] not in used_sentences)
        ],
        key=lambda k: k["score"],
        reverse=True
    )[:(streching_for_duplicates * num_sentences)]

    # Removing adverbs and nominal sentences, pronoun resolution
    sentences_to_remove = list()
    for (sum_index, sentence_dict) in enumerate(summary):
        sentence = nlp(sentence_dict["sentence"])
        if sentence[0].pos_ == "ADV":
            if sentence[1].pos_ == "PUNCT":
                sentence = sentence[2:]
            else:
                sentence = sentence[1:]
            sentence_dict["sentence"] = sentence.text
        if "VBZ" not in {token.tag_ for token in sentence}:
            sentences_to_remove.append(sentence_dict)
        if "PRP" in {token.tag_ for token in sentence}:  # elif si VBZ ici
            i = int(sentence_dict["index"])
            extract_str = " ".join([sentence for sentence in contents_sentences[i - 2: i + 1]])
            extract = nlp(extract_str)
            if extract._.has_coref:
                resolved_extract = extract._.coref_resolved
                sentence_dict["sentence"] = make_sentences_wiki(resolved_extract)[-1]

    summary = [sentence for sentence in summary if (sentence not in sentences_to_remove)]

    return [sentence_dict["sentence"] for sentence_dict in summary[:num_sentences]]  # , keywords)


def fill_structure(tree: dict, documents: list, embedding: Embedding, query: str, used_sentences: set = None,
                   num_sentences=1):
    """
    Fills a tree structure of words with text to create a hierarchical summary
    Args:
        tree: The tree structure of keywords.
        embedding: the embedding of the complete dataset.
        query: A string corresponding to the query.
        used_sentences: A set of forbidden sentences.
    Returns:
        Nothing, it directly fills the structure tree.
    """
    if used_sentences is None:
        used_sentences = set()
    query = query + " " + 2 * " ".join(tree["members"])
    tree["text"] = summarize_cluster(
        documents=documents,
        query=query,  # query used for getting the most relevant documents !
        num_documents=5,
        num_sentences=num_sentences,
        embedding=embedding,
        is_documents_embedding=True,
        used_sentences=used_sentences,
        centroid=tree["centroid"],
        siblings_centroids=tree["siblings_centroids"]
    )
    used_sentences |= {sentence for sentence in tree["text"]}
    for child in tree["children"]:
        fill_structure(
            child,
            documents,
            embedding,
            query,
            used_sentences
        )


def fill_structure_from_leaves(
    tree: dict,
    documents: list,
    embedding: Embedding,
    query: str,
    used_sentences: set = None,
    num_sentences=1,
    num_documents=5,
    get_content=lambda x: x["content"]
):
    """
    Fills a tree structure of words with text to create a hierarchical summary
    Args:
        tree: The tree structure of keywords.
        embedding: the embedding of the complete dataset.
        query: A string corresponding to the query.
        used_sentences: A set of forbidden sentences.
    Returns:
        Nothing, it directly fills the structure tree.
    """
    if used_sentences is None:
        used_sentences = set()

    for child in tree["children"]:
        fill_structure_from_leaves(
            child,
            documents,
            embedding,
            query,
            used_sentences,
            num_sentences=num_sentences
        )

    query = query + " " + 2 * " ".join(tree["members"])
    tree["text"] = summarize_cluster(
        documents=documents,
        query=query,  # query used for getting the most relevant documents !
        num_documents=num_documents,
        num_sentences=num_sentences,
        embedding=embedding,
        is_documents_embedding=True,
        used_sentences=used_sentences,
        centroid=tree["centroid"],
        siblings_centroids=tree["siblings_centroids"],
        get_content=get_content
    )
    used_sentences |= {sentence for sentence in tree["text"]}


def make_adjacency_matrix(keywords_indices, gismo):
    words_vectors = gismo.embedding.y[keywords_indices, :]
    words_adjacency = cosine_similarity(words_vectors, dense_output=False)

    return words_adjacency


def make_map_adj_index_word(keywords_indices: list, gismo: Gismo) -> dict:
    map_emb_index_adj_index = {
        i_emb: i_adj
        for (i_adj, i_emb) in enumerate(keywords_indices)
    }
    map_emb_index_word = {
        i_emb: gismo.embedding.features[i_emb]
        for i_emb in keywords_indices
    }
    return {
        map_emb_index_adj_index[i_emb]: map_emb_index_word[i_emb]
        for i_emb in keywords_indices
    }


def reverse_dict(d: dict) -> dict:
    return {v: k for (k, v) in d.items()}


def hierarchical_summary_to_sknetwork_tree(hierarchical_summary: dict, map_word_index: dict) -> list:
    if len(hierarchical_summary["children"]) == 0:
        if len(hierarchical_summary["members"]) > 1:
            return [[map_word_index[word]] for word in hierarchical_summary["members"]]
        else:
            assert len(hierarchical_summary["members"]) > 0
            return [map_word_index[hierarchical_summary["members"][0]]]
    else:
        return [
            hierarchical_summary_to_sknetwork_tree(child, map_word_index)
            for child in hierarchical_summary["children"]
        ]


def building_distances_matrix(words_vectors):
    number_of_words = np.shape(words_vectors)[0]
    words_adjacency = np.empty((number_of_words, number_of_words))
    for i in range(number_of_words):
        for j in range(number_of_words):
            words_adjacency[i][j] = np.linalg.norm(
                (words_vectors[i, :] -
                 words_vectors[j, :]).todense()
            )
    return sparse.csr_matrix(words_adjacency)


def make_structure_louvain_W2V(
    keywords,
    words_vectors,
    tree,
    gismo,
    root=True,
    depth=3,
):
    """
    Builds a tree structure from Louvain clusterising method
    Args:
        tree: the empty node that will contain
        root:
        depth:
    Returns:
        None, it fills in the empty note that is given at first recursively
    """

    # À la racine, tous les mots sont dans le cluster
    if root:
        tree.members = keywords
        tree.centroid = sum([gismo.embedding.query_projection(member)[0] for member in tree.members])
        tree.title = " ".join([
                                  gismo.embedding.features[i]
                                  for i in gismo.diteration.y_order
                                  if gismo.embedding.features[i] in tree.members
                              ][:10])

    if depth == 0 or len(tree.members) == 1:
        return None

    # Creation de la matrice des mots
    # words_adjacency = cosine_similarity(words_vectors, dense_output = False)
    words_adjacency = building_distances_matrix(words_vectors)
    max_vector = np.ones(np.shape(words_adjacency.data)) * np.max(words_adjacency)
    words_adjacency.data = max_vector - words_adjacency.data
    if sum([i for i in words_adjacency.data]) == 0:
        return None

    # Clustering
    louvain = Louvain()
    labels = louvain.fit_transform(words_adjacency)
    labels_unique, counts = np.unique(labels, return_counts=True)
    if len(labels_unique) == 1:
        return None

    # Il y a autant d'enfants que de clusters
    children = [Node() for l in labels_unique]
    children_members_indexes = [[] for child in children]
    print(labels_unique)
    print(keywords)
    for l in labels_unique:  # on remplit members de chaque dico
        children_members_indexes[l] = np.where(labels == l)[0].tolist()
        try:
            words = [keywords[word_index] for word_index in children_members_indexes[l]]
        except:
            print("plantage avec les mots clef : ", keywords, " et les étiquettes : ", labels_unique)
            return None
        children[l].members = words
        children[l].centroid = sum([gismo.embedding.query_projection(word)[0] for word in words])
        tree.title = " ".join([
                                  gismo.embedding.features[i]
                                  for i in gismo.diteration.y_order
                                  if gismo.embedding.features[i] in words
                              ][:10])
    tree.children = children

    for (l, child) in enumerate(tree.children):
        make_structure_louvain_W2V(
            keywords=child.members,
            words_vectors=words_vectors[children_members_indexes[l], :],  # to do
            gismo=gismo,
            tree=child,
            root=False,
            depth=depth - 1
        )
