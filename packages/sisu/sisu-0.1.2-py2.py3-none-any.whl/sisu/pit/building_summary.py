import re
from collections import OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
from gismo.gismo import Gismo
from gismo.embedding import Embedding
from gismo.corpus import Corpus
from sisu.pit.gismo_wrapper import make_gismo, simplified_document_to_string
from sisu.preprocessing.language import MAP_LANG_STOP_WORDS
from sisu.preprocessing.tokenizer import num_words, make_sentences, words

RE_URL = re.compile("https?://[a-zA-Z.:0-9]+.*|www.|.org|.net|.com|[a-zA-Z.:0-9]+/")
RE_CITATION = re.compile(r"[\[(]\s*\d+(,\s*\d+)*[)\]]")


def is_relevant_sentence(sentence: str, min_num_words: int = 6, max_num_words: int = 60) -> bool:
    """
    Ignore sentences that are too short, too long, that contain a URL or a citation.

    Parameters
    ----------
    sentence: :class:`str`
        Sentence to analyze.
    min_num_words: :class:`int`, optional
        Minimal number of words.
    max_num_words: :class:`int`, optional
        Maximal number of words.

    Returns
    -------
    :class:`bool`
        Is the sentence OK?

    Examples
    --------
    >>> is_relevant_sentence("This is a short sentence!")
    False
    >>> is_relevant_sentence("This is a sentence with reference to the url http://www.ix.com!")
    False
    >>> is_relevant_sentence("This is a a sentence with some citations [3, 7]!")
    False
    >>> is_relevant_sentence("I have many things to say in that sentence, to the point "
    ...                      "I do not know if I will stop anytime soon but don't let it stop"
    ...                      "you from reading this meaninless garbage and this goes on and "
    ...                      "this goes on and this goes on and this goes on and this goes on and "
    ...                      " this goes on and  this goes on and  this goes on and  this goes on "
    ...                      "and  this goes on and  this goes on and  this goes on and  this goes "
    ...                      "on and  this goes on and  this goes on and  this goes on and  this goes "
    ...                      "on and  this goes on and ")
    False
    >>> is_relevant_sentence("This sentence is not too short and not too long, without URL and without citation.")
    True
    """
    n = num_words(sentence)
    return (
        min_num_words <= n <= max_num_words
        and re.search(RE_CITATION, sentence) is None
        and re.search(RE_URL, sentence) is None
    )


def summarize(documents, query="", num_documents=None, num_sentences=None, ratio=0.05,
              embedding=None, num_keywords: int = 15, size_generic_query: int = 5,
              used_sentences: set = None, get_content=lambda x: x["content"]) -> tuple:
    """
    Produces a list of sentences and a list of keywords.

    Parameters
    ----------
    documents: :class:`list`
        A list of documents.
    query: :class:`str`, optional
        Textual query to focus the summary on one subject.
    num_documents: :class:`int`, optional
        Number of top documents to be taking into account for the summary.
    num_sentences: :class:`int`, optional
        Number of sentences wanted in the summary. Overrides ratio.
    ratio: :class:`float` in ]0, 1], optional
        length of the summary as a proportion of the length of the num_documents kept.
    embedding: :class:`~gismo.embedding.Embedding`, optional
        An Embedding fitted on a bigger corpus than documents.
    num_keywords: :class:`int`, optional
        An int corresponding to the number of keywords returned
    size_generic_query: :class:`int`, optional
        size generic query
    used_sentences: :class:`set`, optional
        A set of "forbidden" sentences. Will be updated inplace.
    get_content: callable, optional
        A function that allows the retrieval of a document's content.

    Returns
    -------
    List
        A list of the summary sentences,
        A list of keywords.

    Examples
    --------
    >>> from gismo.datasets.reuters import get_reuters_news
    >>> summarize(get_reuters_news(), num_documents=10, num_sentences=4) # doctest: +NORMALIZE_WHITESPACE
    (['Gum arabic has a history dating back to ancient times.',
      'Hungry nomads pluck gum arabic as they pass with grazing goats and cattle.',
      'For impoverished sub-Saharan states producing the bulk of world demand, gum arabic simply means export currency.',
      "After years of war-induced poverty, gum arabic is offering drought-stricken Chad's rural poor a lifeline to the production plants of the world's food and beverage giants."],
      ['norilsk', 'icewine', 'amiel', 'gum', 'arabic', 'her', 'tibet', 'chad', 'deng', 'oil', 'grapes', 'she', 'his', 'czechs', 'chechnya'])
    >>> summarize(get_reuters_news(), query="Ericsson", num_documents=10, num_sentences=5) # doctest: +NORMALIZE_WHITESPACE
    (['The restraints are few in areas such as consumer products, while in sectors such as banking, distribution and insurance, foreign firms are kept on a very tight leash.',
      'These latest wins follow a recent $350 million contract win with Telefon AB L.M.',
      'Pocket is the first from the high-priced 1996 auction known to have filed for bankruptcy protection.',
      '"That is, assuming the deal is done right," she added.',
      '"Generally speaking, the easiest place to make a profit tends to be in the consumer industry, usually fairly small-scale operations," said Anne Stevenson-Yang, director of China operations for the U.S.-China Business Council.'],
      ['ericsson', 'sweden', 'motorola', 'telecommuncation', 'communciation', 'bolstering', 'priced', 'sectors', 'makers', 'equipment', 'schaumberg', 'lm', 'done', 'manufacturing', 'consumer'])
    """
    if used_sentences is None:
        used_sentences = set()

    if num_documents is None:
        num_documents = len(documents)

    doc_corpus = Corpus(source=documents, to_text=get_content)

    if embedding:
        doc_embedding = Embedding()
        doc_embedding.fit_ext(embedding)
        doc_embedding.transform(corpus=doc_corpus)
    else:
        vectorizer = CountVectorizer(dtype=float)
        doc_embedding = Embedding(vectorizer=vectorizer)
        doc_embedding.fit_transform(corpus=doc_corpus)

    documents_gismo = Gismo(corpus=doc_corpus, embedding=doc_embedding, alpha=.2)

    #        print("- Running D-iteration (query = %s)" % query)
    documents_gismo.rank(query)
    #        print("- Extracting results (gismo = %s)" % documents_gismo)
    best_documents = documents_gismo.get_documents_by_rank(k=num_documents)

    #    Split best document into sentences. Remove duplicates
    #    print("Splitting documents into sentences")
    contents_sentences = sorted({
        sentence
        for document in best_documents
        for sentence in make_sentences(get_content(document))
    })

    # Scale the number of sentences proportionally to the total number
    # of sentences in the top documents.
    if num_sentences is None:
        num_sentences = int(ratio * len(contents_sentences))
    #        print("Scaling num_sentences to %d (ratio = %s)" % (num_sentences, ratio))

    #    print("Preparing sentence-based gismo")

    sent_corpus = Corpus(source=contents_sentences)

    sent_embedding = Embedding()
    if embedding:
        sent_embedding.fit_ext(embedding)
    else:
        sent_embedding.fit_ext(doc_embedding)

    sent_embedding.transform(corpus=sent_corpus)
    sentences_gismo = Gismo(corpus=sent_corpus, embedding=sent_embedding, alpha=.2)

    #    print("Preparing sentence-based gismo")
    sentences_gismo.rank(query)
    keywords = sentences_gismo.get_features_by_rank(k=num_keywords)
    if query == "":
        sentences_gismo.rank(" ".join(keywords[:size_generic_query]))
    sentences_ranks = sentences_gismo.diteration.x_order  # List of sentence indices by decreasing relevance
    #    print("Extracting %d-top sentences" % num_sentences)

    num_kept_sentences = 0
    i = 0
    ranked_sentences = list()
    while num_kept_sentences < num_sentences and i < len(contents_sentences):
        sentence = contents_sentences[sentences_ranks[i]]
        if sentence not in used_sentences and is_relevant_sentence(sentence):
            used_sentences.add(sentence)
            ranked_sentences.append(sentence)
            num_kept_sentences += 1
        i += 1
    return ranked_sentences, keywords


def make_query(sentence: str, language='en') -> str:
    """
    Builds a query from a sentence.

    Parameters
    ----------
    sentence: :class:`str`
        A string from which we want to build a query.
    language: :class:`str`
        Language use
    Returns
    -------
        A string corresponding to the query.

    Examples
    ---------
    >>> make_query("Life is something nice!")
    'life nice'
    >>> make_query("La vie est belle !", language='fr')
    'vie belle'
    """
    stop_words = set(MAP_LANG_STOP_WORDS[language])
    return " ".join([w for w in words(sentence) if w not in stop_words])


def make_tree(
    documents: list, query: str = "", depth: int = 1, trees: list = None, documents_gismo: Gismo = None,
    num_documents: int = None, num_sentences: int = None, embedding: Embedding = None, used_sentences: set = None
) -> list:
    r"""
    Builds a hierarchical summary.

    Parameters
    ----------
    documents: :class:`list` of :class:`dict`
        A list of dict corresponding to documents, only the values of the "content" key will be summarized.
    query: :class:`str`, optional
        Textual query to focus the summary on one subject.
    depth: :class:`int`, optional
        An int giving the depth of the summary (depth one is a sequential summary).
    trees: :class:`list`, optional
        A list of dict being completed, necessary for the recursivity.
    documents_gismo: :class:`~gismo.gismo.Gismo`
        Pre-existing Gismo
    num_documents: :class:`int`, optional
        Number of top documents to be taking into account for the summary.
    num_sentences: :class:`int`, optional
        Number of sentences wanted in the summary.
    embedding: :class:`~gismo.embedding.Embedding`, optional
        An Embedding fitted on a bigger corpus than documents.
    used_sentences: :class:`set`, optional
        A set of "forbidden" sentences. Will be updated inplace.

    Returns
    -------
    :class:`list` of :class:`dict`
        A list of dict corresponding to the hierarchical summary

    Examples
    --------
    >>> from gismo.datasets.reuters import get_reuters_news
    >>> make_tree(get_reuters_news(), query="Orange", num_documents=10, num_sentences=3, depth=2) # doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
    [{'text': 'But some analysts still believe Orange is overvalued.',
      'current_keywords': ['orange', 'one', 'is', 'at', 'on', 'in', 'and', 'its', 'shares', 'has', 'analysts', 'of', 'market', 'believe', 'overvalued'],
      'url': None,
      'children': [{'text': 'Trading sources said China was staying out of the market, and that Indian meal was currently overvalued by a good $20 a tonne.',
                    'current_keywords': ['orange', 'overvalued', 'analysts', 'that', 'and', 'are', 'compared', 'believe', 'market', 'but', 'some', 'still', 'of', 'said', 'we'],
                    'url': None, 'children': []},
                   {'text': 'Since the purchase, widely seen by analysts as overvalued, Quaker has struggled with the line of ready-to-drink teas and juices.',
                    'current_keywords': ['orange', 'overvalued', 'analysts', 'that', 'and', 'are', 'compared', 'believe', 'market', 'but', 'some', 'still', 'of', 'said', 'we'],
                    'url': None, 'children': []},
                   {'text': '"No question that if the dollar continues to be overvalued and continues to be strong, we\'ll see some price erosion later in the year."',
                    'current_keywords': ['orange', 'overvalued', 'analysts', 'that', 'and', 'are', 'compared', 'believe', 'market', 'but', 'some', 'still', 'of', 'said', 'we'],
                    'url': None, 'children': []}]},
     {'text': 'Orange shares were 2.5p higher at 188p on Friday.',
      'current_keywords': ['orange', 'one', 'is', 'at', 'on', 'in', 'and', 'its', 'shares', 'has', 'analysts', 'of', 'market', 'believe', 'overvalued'],
      'url': None,
      'children': [{'text': 'Orange, Calif.-based Bergen is the largest U.S. distributor of generic drugs, while Miami-based Ivax is a generic drug manufacturing giant.',
                    'current_keywords': ['orange', 'higher', 'shares', 'friday', 'on', 'at', 'and', 'in', 'its', 'of', 'percent', 'one', 'mobile', 'to', 'market'],
                    'url': None, 'children': []},
                   {'text': 'One-2-One and Orange ORA.L, which offer only digital services, are due to release their connection figures next week.',
                    'current_keywords': ['orange', 'higher', 'shares', 'friday', 'on', 'at', 'and', 'in', 'its', 'of', 'percent', 'one', 'mobile', 'to', 'market'],
                    'url': None, 'children': []},
                   {'text': "Dodd noted that BT's plans to raise the price of calls to Orange and One 2 One handsets would be beneficial.",
                    'current_keywords': ['orange', 'higher', 'shares', 'friday', 'on', 'at', 'and', 'in', 'its', 'of', 'percent', 'one', 'mobile', 'to', 'market'],
                    'url': None, 'children': []}]},
     {'text': 'Orange already has a full roaming agreement in Germany and a partial one in France, centred on Paris.',
      'current_keywords': ['orange', 'one', 'is', 'at', 'on', 'in', 'and', 'its', 'shares', 'has', 'analysts', 'of', 'market', 'believe', 'overvalued'],
      'url': None,
      'children': [{'text': 'Orange says its offer of roaming services between the UK and other countries is part of its aim to provide customers with the best value for money.',
                    'current_keywords': ['orange', 'roaming', 'partial', 'centred', 'paris', 'france', 'germany', 'agreement', 'full', 'on', 'and', 'in', 'of', 'for', 'with'],
                    'url': None, 'children': []},
                   {'text': 'As with all roaming agreements, the financial details of the Swiss deal remain a trade secret.',
                    'current_keywords': ['orange', 'roaming', 'partial', 'centred', 'paris', 'france', 'germany', 'agreement', 'full', 'on', 'and', 'in', 'of', 'for', 'with'],
                    'url': None, 'children': []},
                   {'text': '"We look forward in 1997 to continuing to move ahead and to extending our international service through new roaming agreements and the introduction of dual band handsets."',
                    'current_keywords': ['orange', 'roaming', 'partial', 'centred', 'paris', 'france', 'germany', 'agreement', 'full', 'on', 'and', 'in', 'of', 'for', 'with'],
                    'url': None, 'children': []}]}]
    """
    num_keywords = 15
    if used_sentences == None:
        used_sentences = set()

    if depth == 0:
        return list()
    if documents_gismo == None:
        doc_corpus = Corpus(source=documents, to_text=simplified_document_to_string)
        if embedding:
            doc_embedding = Embedding()
            doc_embedding.fit_ext(embedding)
            doc_embedding.transform(corpus=doc_corpus)
        else:
            vectorizer = CountVectorizer(dtype=float)
            doc_embedding = Embedding(vectorizer=vectorizer)
            doc_embedding.fit_transform(corpus=doc_corpus)

        documents_gismo = Gismo(corpus=doc_corpus, embedding=doc_embedding, alpha=.2)

    documents_gismo.rank(query)
    best_documents = [ (i, documents_gismo.corpus[i]) for i in documents_gismo.diteration.x_order[:num_documents]]
        # documents_gismo.get_documents_by_rank(k=num_documents)
    sentences_dictionnaries = [
        {
            "sentence": sentence,
            "url": document.get("url"),
            "doc_index": i,
        }
        for i, document in best_documents
        for sentence in list(OrderedDict.fromkeys(make_sentences(document["content"])))
    ]

    sent_corpus = Corpus(source=sentences_dictionnaries, to_text=lambda s: s['sentence'])
    if embedding:
        sent_embedding = Embedding()
        sent_embedding.fit_ext(embedding)
        sent_embedding.transform(corpus=sent_corpus)
    else:
        vectorizer = CountVectorizer(dtype=float)
        sent_embedding = Embedding(vectorizer=vectorizer)
        sent_embedding.fit_transform(corpus=sent_corpus)

    sentences_gismo = Gismo(corpus=sent_corpus, embedding=sent_embedding, alpha=.2)
    sentences_gismo.rank(query)
    keywords = sentences_gismo.get_features_by_rank(k=num_keywords)
    sentences_ranks = sentences_gismo.diteration.x_order

    num_kept_sentences = 0
    ranked_sentences_dict = list()
    for rank in sentences_ranks:
        sentence_dict = sentences_dictionnaries[rank]
        sentence = sentence_dict["sentence"]
        if sentence not in used_sentences and is_relevant_sentence(sentence):
            ranked_sentences_dict.append(sentence_dict)
            used_sentences.add(sentence)
            num_kept_sentences += 1
            if num_kept_sentences >= num_sentences:
                break
    children = ranked_sentences_dict
    return [
        {
            "text": child["sentence"],
            "current_keywords": keywords,
            "url": child.get("url"),
            "children": make_tree(
                trees=trees,
                depth=depth - 1,
                documents_gismo=documents_gismo,
                documents=documents,
                query=make_query(" ".join([query, child["sentence"]])),
                num_sentences=num_sentences,
                embedding=embedding,
                used_sentences=used_sentences
            )
        } for child in children
    ]
