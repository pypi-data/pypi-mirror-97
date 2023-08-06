#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#This file is part of newdle
#Copyright © 2020 Nokia Corporation and/or its subsidiary(-ies). All rights reserved. *
#
# Author:
#   Mélanie Cambus    <melanie.cambus@nokia.com>

from sisu.pit.hierarchical_functions import Node
import re

TITLES = [
    re.compile(r"\n\n==[\s\w]+\s==\n"),
    re.compile(r"\n\n===[\s\w]+\s===\n"),
    re.compile(r"\n\n====[\s\w]+\s====\n")
]

def cut_text_into_sections(tree :Node, doc :str, pattern) -> Node:# keywords
    if pattern.search(doc) == None:
        tree.text = doc
        return tree
    sections = [section for section in pattern.finditer(doc)]
    tree.text = doc[:sections[0].span()[0]]
    num_sections = len(sections)
    for (s_index, section) in enumerate(sections):
        child = Node()
        child.title = section.group()
        if s_index < num_sections - 1:
            # Le texte va de la fin de mon titre au début du titre suivant
            child.text = doc[section.span()[1]:sections[s_index + 1].span()[0] - 1]
        else:
            child.text = doc[section.span()[1]:]
        tree.children.append(child)
    return tree

# TO DO : remplacer le compteur par un countVectorizer
def make_structure_from_wiki(doc :dict, titles :list = TITLES, keywords :list = []) -> Node:
    tree = Node()
    tree.title = doc["title"]
    tree.text = doc["contents"]
    tree.members = keywords
    tree = cut_text_into_sections(tree, tree.text, titles[0])
    grandchildren = list()
    for child in tree.children:
        child = cut_text_into_sections(child, child.text, titles[1])
        for grandchild in child.children:
            grandchildren.append(grandchild)
            grandchild = cut_text_into_sections(grandchild, grandchild.text, titles[2])
    for keyword in keywords:
        counts_children = list()
        for child in tree.children:
            count = len([oc for oc in re.finditer(keyword, child.text)])
            counts_children.append(count)
        tree.children[counts_children.index(max(counts_children))].members.append(keyword)

        counts_grandchildren = list()
        for grandchild in grandchildren:
            count = len(re.findall(keyword, grandchild.text))
            counts_grandchildren.append(count)
        grandchildren[counts_grandchildren.index(max(counts_grandchildren))].members.append(keyword)
    for child in tree.children:
        if len(child.members) == 0:
            del child
    for grandchild in grandchildren:
        if len(grandchild.members) == 0:
            del grandchild
    return tree
