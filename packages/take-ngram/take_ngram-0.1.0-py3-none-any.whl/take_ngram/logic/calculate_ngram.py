__author__ = 'Gabriel Oliveira'
__version__ = '0.1.0'

import ast
from typing import Optional, Any, Tuple

from nltk.util import ngrams

from .utils import add_frequency, filter_words_in_sentence


def remove_stop_words(msg: str,
                      stop_words: list) -> str:
    """ Return msg without given stop_words

    :param msg: A sentence to be processed.
    :type msg: str
    :param stop_words: A list with all the stop words to be removed.
    :type stop_words: str
    :return: Sentence processed.
    :rtype: str
    """
    if stop_words:
        msg = filter_words_in_sentence(msg=msg,
                                       stop_words=stop_words)
    return msg


def generate_ngram(reader: Any,
                   size: int,
                   msg_position: int,
                   stop_words: Optional[list] = None) -> dict:
    """Generate dictionary with n-grams and frequency

    :param reader: CSV reader of the file.
    :type reader: _reader
    :param size: Size of the n-gram.
    :type size: int
    :param msg_position: Index of the column message.
    :type msg_position: int
    :param stop_words: A list with all the stop words to be removed. Default is None.
    :type stop_words: Optional[list]
    :return: Dictionary with n-grams and they frequency.
    :rtype: dict
    :raise ValueError: If size is grater than the sentences.
    """
    ngram_dict = {}
    valid_size = False

    for row in reader:
        ngram_dict, valid_size = add_ngram_sentence(msg=row[msg_position],
                                                    stop_words=stop_words,
                                                    size=size,
                                                    ngram_dict=ngram_dict,
                                                    valid_size=valid_size)
    if not valid_size:
        raise ValueError('N-gram size larger than the largest sentence')
    return ngram_dict


def generate_ngram_cluster(reader: Any,
                           size: int,
                           msg_position: int,
                           group_position: int,
                           groups_list: list,
                           stop_words: Optional[list] = None) -> dict:
    """
    Generate dictionary with n-grams and frequency for sentences for sentences
    of a cluster.

    :param reader: CSV reader of the file.
    :type reader: _reader
    :param size: Size of the n-gram.
    :type size: int
    :param msg_position: Index of the column message.
    :type msg_position: int
    :param group_position: Index of the column group.
    :type msg_position: int
    :param groups_list: List of groups to be analysis.
    :type groups_list: list
    :param stop_words: A list with all the stop words to be removed. Default is None.
    :type stop_words: list
    :return: Dictionary with n-grams and they frequency.
    :rtype: dict
    :raise ValueError: If size is grater than the sentences.
    """
    ngram_dict = {}
    valid_size = False
    for row in reader:
        entities_group = ast.literal_eval(row[group_position])
        if len(entities_group) > 1 and any([group in groups_list
                                            for group in entities_group]):
            ngram_dict, valid_size = add_ngram_sentence(msg=row[msg_position],
                                                        stop_words=stop_words,
                                                        size=size,
                                                        ngram_dict=ngram_dict,
                                                        valid_size=valid_size)
    if not valid_size:
        raise ValueError('N-gram size larger than the largest sentence')
    return ngram_dict


def add_ngram_sentence(msg: str,
                       stop_words: list,
                       size: int,
                       ngram_dict: dict,
                       valid_size: bool) -> Tuple[dict, bool]:
    """
    :param msg: Sentence to be generate the N-grams
    :type msg: str
    :param stop_words: A list with all the stop words to be removed.
    :type stop_words: list
    :param size: Size of the n-gram.
    :type size: int
    :param ngram_dict: Ngram to be add in the dictionary.
    :type ngram_dict: dict
    :param valid_size: Auxiliary logical value. True if the sentences size is greater than the size of the ngram.
    :type valid_size: bool
    :return: A tuple with the dictionary of ngram and frequency, and the auxiliary logical value.
    :rtype: Tuple[dict, bool]
    """
    msg_split = remove_stop_words(msg=msg,
                                  stop_words=stop_words).split()
    if len(msg_split) >= size:
        for ngram in ngrams(msg_split, size):
            ngram_dict = add_frequency(ngram=' '.join(ngram),
                                       ngram_dict=ngram_dict)
        valid_size = True
    return ngram_dict, valid_size
