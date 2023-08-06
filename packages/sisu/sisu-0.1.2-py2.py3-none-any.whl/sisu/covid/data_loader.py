import json
import zlib
from pathlib import Path
from zipfile import ZipFile

import dill as pickle
import numpy as np
from gismo.filesource import FileSource

from sisu.preprocessing.covid19 import get_content
from sisu.preprocessing.language import guess_language


def load_dataset(dataset_dir: str, getters: dict = None, max_documents: int = None,
                 save='dump.pkl', erase=False) -> list:
    """
    Load files of the COVID-19 dataset or any dataset containing only json files.

    Parameters
    ----------
    dataset_dir: :class:`~pathlib.Path` or :class:`str`
        Directory of the uncompressed dataset.
    getters: :class:`dict`, optional
        Key getters.
    max_documents: :class:`int`, optional
        max_documents: How many documents must be loaded (default: load all documents).
    save: :class:`str` or :class:`~pathlib.Path` or None
        If not `None`, name of the save file to use.
    erase: :class:`bool`, optional
        If `True`, will rebuild the save even if it exists.

    Returns
    -------
    :class:`list` of :class:`dict`
        A list of dict, where each dict represents a document (each dict corresponds to a json file of the dataset).

    Examples
    --------

    We locate a place where json files of covid-related papers lie.

    >>> data_dir = Path("data/covid_sample")

    We check that there is no save at this point.

    >>> save_location = data_dir / "dump.pkl"
    >>> save_location.exists()
    False

    We now load the available json and extract the titles

    >>> documents = load_dataset(data_dir)
    >>> sorted([doc['metadata']['title'] for doc in documents])
    ['"Multi-faceted" COVID-19: Russian experience', 'COVID-19-Pneumonie', 'Community frailty response service: the ED at your front door']

    Now the save file is there.

    >>> save_location.exists()
    True

    Reloading the dataset will now go through the pickle file (the only difference you should observe is speed).

    >>> documents = load_dataset(data_dir)
    >>> sorted([doc['metadata']['title'] for doc in documents])
    ['"Multi-faceted" COVID-19: Russian experience', 'COVID-19-Pneumonie', 'Community frailty response service: the ED at your front door']

    Let's remove the save.

    >>> save_location.unlink()

    Now, we use getters to preprocess the documents and we limit the results to 2 documents. we also do not want a save to be made.

    >>> from sisu.preprocessing.covid19 import get_title, get_abstract
    >>> documents = load_dataset(data_dir, max_documents=2, getters={'title': get_title, 'abstract': get_abstract}, save=None)
    >>> len(documents)
    2
    >>> [k for k in documents[0].keys()]
    ['title', 'abstract']

    We can check that no save file was produced.

    >>> save_location.exists()
    False


    """
    dataset_dir = Path(dataset_dir)
    assert dataset_dir.exists()

    if save is not None:
        save_location = dataset_dir / save
        file_exist = save_location.exists()
    else:
        file_exist = False

    if file_exist and not erase:
        with open(save_location, 'rb') as f:
            return pickle.load(f)
    documents = list()
    i = 0
    for file in dataset_dir.rglob("*.json"):
        with open(file) as f:
            document = json.load(f)
            if getters is not None:
                document = {key: get(document) for (key, get) in getters.items()}
            documents.append(document)
            i += 1  # PATCH
        if max_documents != None and i == max_documents:
            break
    if save is not None:
        with open(save_location, 'wb') as f:
            pickle.dump(documents, f)
    return documents


def filesource_loader_covid(d: Path, lang: str = "en", zipname="CORD-19-research-challenge.zip",
                            fsname="covid_corpus") -> FileSource:
    """
    Create and return a Gismo :class:`~gismo.filesource.FileSource` from a covid zipfile.

    Parameters
    ----------
    d: :class:`~pathlib.Path` or :class:`str`
        Data directory
    lang: :class:`str`, optional
        Language to keep`
    zipname: :class:`~pathlib.Path` or :class:`str`, optional
        Name of the covid zip archive
    fsname: :class:`str`
        Prefix of the :class:`~gismo.filesource.FileSource`

    Returns
    -------
    :class:`~gismo.filesource.FileSource`
        List-like object that reads its content from file.

    Examples
    --------

    We load the filesource, make a copy in memory and close it.

    >>> data_folder = Path("data")
    >>> fsource = filesource_loader_covid(d=data_folder, zipname="covid_sample.zip")
    >>> source = [a for a in fsource]
    >>> fsource.close()

    How many articles?

    >>> len(source)
    2

    Title and url?

    >>> sorted([{'title': a['metadata']['title'], 'url': a['url']} for a in source], key=lambda d: len(d['title'])) # doctest: +NORMALIZE_WHITESPACE
    [{'title': '"Multi-faceted" COVID-19: Russian experience',
      'url': 'file:///%sdata0000028b5cc154f68b8a269f6578f21e31f62977.json'},
     {'title': 'Community frailty response service: the ED at your front door',
      'url': 'file:///%sdata000680e3114af4aa10e8f208cd162a61195f4465.json'}]

    One article was in german. Can we retrieve it?

    >>> fsource = filesource_loader_covid(d=data_folder, zipname="covid_sample.zip", lang='de')
    >>> source = [a for a in fsource]
    >>> fsource.close()

    How many articles?

    >>> len(source)
    1

    Is it in German?

    >>> from sisu.preprocessing.covid19 import get_content
    >>> get_content(source[0]) # doctest: +ELLIPSIS
    '. der Entwicklung einer schweren Pneumonie im Vordergrund, die in der Regel prognostisch bestimmend ist. Sehr...'

    :class:`~gismo.filesource.FileSource` objects rely on a `.data` file and a `.index` file. They can be re-used, or removed if it is not planned.

    >>> Path(data_folder / "covid_corpus.data").unlink()
    >>> Path(data_folder / "covid_corpus.index").unlink()
    """
    d = Path(d)
    source = d / zipname
    target = d / fsname
    with ZipFile(source) as z:
        index = [0]
        with open(target.with_suffix(".data"), "wb") as data:
            for filename in z.namelist():
                if not filename.endswith('.json'):
                    continue
                with z.open(filename) as f:
                    dic = json.load(f)
                    dic["url"] = "file:///%s" + str(d) + filename
                if guess_language(get_content(dic)) == lang:
                    data.write(zlib.compress(json.dumps(dic).encode('utf8')))
                    index.append(data.tell())
        with open(target.with_suffix(".index"), "wb") as g:
            pickle.dump(np.array(index), g)
    return FileSource(target)
