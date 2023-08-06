import re

toy_covid_article = {
    'metadata': {'title': "Predator"},
    'abstract': [{'text': "In the jungle, no-one hears you far cry. And vice-versa."},
                 {'text': "They say to make a long abstract, with the number 42 in it, so here I am."}],
    'body_text': [{'section': 'introduction',
                   'text': "There is no-one in the trees. Is there?"},
                  {'section': 'conclusion',
                   'text': "Predators don't like to lose."}]
}
"""
A toy document with the same structure as the json in the COVID-19 dataset.
"""


def get_title(document: dict) -> str:
    """
    Get the title of a document from a document with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`str`
        The title of the document.

    Examples
    --------

    >>> get_title(toy_covid_article)
    'Predator'
    """
    return document["metadata"]["title"]


def get_abstract(document: dict) -> str:
    """
    Get the abstract of a document with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`str`
        Abstract of the document.

    Examples
    --------

    >>> get_abstract(toy_covid_article) # doctest: +NORMALIZE_WHITESPACE
    'In the jungle, no-one hears you far cry. And vice-versa.
    They say to make a long abstract, with the number 42 in it, so here I am.'
    """
    abstract_list = document["abstract"]
    if abstract_list:
        return " ".join(
            [dict_abstract["text"] for dict_abstract in abstract_list]
        )
    else:
        return ""


def get_content(document: dict) -> str:
    """
    Get the content of a document with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`str`
        Content of the document.

    Examples
    --------

    >>> get_content(toy_covid_article)
    "introduction. There is no-one in the trees. Is there? conclusion. Predators don't like to lose."
    """
    return " ".join(
        [". ".join(
            [
                chapter["section"],
                chapter["text"]
            ]
        )
            for chapter in document["body_text"]
        ]
    )


def get_all_titles(document: dict) -> str:
    """
    Gets the main title and sections titles of a document with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`str`
        Titles of the document.

    Examples
    --------

    >>> get_all_titles(toy_covid_article)
    'introduction conclusion Predator'
    """
    return " ".join([chapter["section"] for chapter in document["body_text"]] + [get_title(document)])


def make_abstract_doc(document: dict) -> dict:
    """
    Make a simplified document from abstracts with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`dict`
        Simplified document.

    Examples
    --------

    >>> make_abstract_doc(toy_covid_article) # doctest: +NORMALIZE_WHITESPACE
    {'title': 'Predator', 'abstract': 'In the jungle, no-one hears you far cry. And vice-versa.
                                       They say to make a long abstract, with the number 42 in it, so here I am.'}
    """
    return {
        "title": get_title(document),
        "abstract": get_abstract(document)
    }


def make_content_doc(document: dict) -> dict:
    """
    Make a simplified document representation from contents with the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`dict`
        Simplified document.

    Examples
    --------

    >>> make_content_doc(toy_covid_article) # doctest: +NORMALIZE_WHITESPACE
    {'title': 'Predator',
     'content': "introduction. There is no-one in the trees. Is there? conclusion. Predators don't like to lose."}
    """
    return {
        "title": get_title(document),
        "content": get_content(document)
    }


def make_clean_doc(document: dict) -> dict:
    """
    Make a simplified clean representation of documents to initialize "proper" vocabulary
    when documents have the same structure as the json in the COVID-19 dataset.

    Parameters
    ----------
    document: :class:`dict`
        A `dict` representing a document.

    Returns
    -------
    :class:`dict`
        Simplified cleaned document.

    Examples
    --------

    >>> make_clean_doc(toy_covid_article) # doctest: +NORMALIZE_WHITESPACE
    {'title': 'Predator',
     'abstract': 'In the jungle no-one hears you far cry And vice-versa
                  They say to make a long abstract with the number  in it so here I am',
      'content': "introduction There is no-one in the trees Is there? conclusion Predators don't like to lose"}
    """
    pattern = re.compile(r"[,.:;()0-9+=%\[\]_]")
    return {
        "title": re.sub(pattern, "", get_title(document)),
        "abstract": re.sub(pattern, "", get_abstract(document)),
        "content": re.sub(pattern, "", get_content(document))
    }
