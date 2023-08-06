__author__ = 'Gabriel Oliveira'
__version__ = '0.1.0'

import re


def add_frequency(ngram: str,
                  ngram_dict: dict) -> dict:
    """Return ngram_dict with ngram as key for it's frequency.

    :param ngram: Ngram to be add in the dictionary.
    :type ngram: dict
    :param ngram_dict: Dictionary with n-grams and they frequency.
    :type ngram_dict: dict
    :return: Dictionary with n-grams and they frequency.
    :rtype: dict
    """
    ngram_dict[ngram] = ngram_dict.get(ngram, 0) + 1
    return ngram_dict


def filter_words_in_sentence(msg: str,
                             stop_words: list) -> str:
    """Remove stop words in the sentence

    :param msg: A sentence do be processed.
    :type msg: str
    :param stop_words: A list with all the stop words to be removed.
    :type stop_words: list
    :return: Sentence processed.
    :rtype: str
    """
    for word in stop_words:
        pattern = f'(\s|^){word}(\s|$)'
        for match in re.finditer(pattern, msg):
            msg = msg[:match.start()] + ' ' + msg[match.end():]
    return ' '.join(msg.split())
