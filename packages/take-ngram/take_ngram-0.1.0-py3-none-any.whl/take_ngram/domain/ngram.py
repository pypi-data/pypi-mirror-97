__author__ = 'Gabriel Oliveira'
__version__ = '0.1.0'

from typing import Tuple, Optional, Any

from take_ngram.persistence import read_data
from take_ngram.logic import generate_ngram, generate_ngram_cluster
from take_ngram.presentation import plot_word_cloud


class NGram:
    """
    Create and visualize n-grams for a set of messages.

    """

    def __init__(self,
                 path: str,
                 message_column: str,
                 n: int = 2,
                 subject_column: str = None,
                 subject_list: list = None,
                 encoding: str = 'utf-8',
                 sep: str = '|',
                 stop_words: list = None,
                 remove_prepositions: bool = True) -> None:
        """

        :param path: Path of the file.
        :type path: str
        :param message_column: Name of message column.
        :type message_column: str
        :param n: Size of the n-gram. Default is 2.
        :type n: int
        :param subject_column: Name of group column. Default is None.
        :type subject_column: str
        :param subject_list: List of subjects sentences to be analysed. Default is None.
        :type subject_list: list
        :param encoding: File encoding. Default is 'utf-8'.
        :type encoding: str
        :param sep: The separator of columns. Default is '|'
        :type sep: str
        :param stop_words: A list with initial stop words to be removed.
        Default is None.
        :type stop_words: list
        :param remove_prepositions: Add preposition to stop words list.
        Default is True.
        :type remove_prepositions: bool
        """

        self._stop_words = self.__process_stop_word(stop_words_list=stop_words,
                                                    remove_prep=remove_prepositions)
        self._reader, self._msg_ind, self._group_ind = self.__read_data(
            path=path,
            message_column=message_column,
            cluster_column=subject_column,
            encoding=encoding,
            sep=sep)
        self.ngrams = self.__get_ngrams(n=n,
                                        group_list=subject_list)

    def __process_stop_word(self,
                            stop_words_list: list,
                            remove_prep: bool) -> list:
        """Set the stop words list

        :param stop_words_list: A list with initial stop words to be removed.
        :type stop_words_list: list
        :param remove_prep: Add preposition to stop words list.
        :type remove_prep: bool
        :return: A list with all stop words to be removed.
        :rtype: list
        """
        if stop_words_list:
            stop_words = stop_words_list
        else:
            stop_words = []
        if remove_prep:
            stop_words += ['do', 'da', 'dos', 'das', 'de',
                           'mais', 'sobre', 'em']
        return stop_words

    def __read_data(self,
                    path: str,
                    message_column: str,
                    encoding: str,
                    sep: str,
                    cluster_column: str) -> Tuple[Any, int, Optional[int]]:
        """Create reader of the csv file

        :param path: Path of the file.
        :type path: str
        :param message_column: Name of message column.
        :type message_column: str
        :param encoding: File encoding.
        :type encoding: str
        :param sep: The separator of columns.
        :type sep: str
        :param cluster_column: Name of cluster column.
        :type cluster_column: str
        :return: A tuple containing the reader of the file, the index of the
        message and of the group column (if exist).
        :rtype: Tuple[_reader, int, Optional[int]]
        """
        return read_data(path=path,
                         message_column=message_column,
                         group_column=cluster_column,
                         encoding=encoding,
                         sep=sep)

    def __get_ngrams(self,
                     n: int,
                     group_list: Optional[list] = None) -> dict:
        """Create the n-grams

        :param n: Size of the n-grams.
        :type n: int
        :param group_list: List of groups to be analysed, if None is passed
        it analyses the whole file. Default is None.
        :type group_list: list
        :return:
        :rtype: dict
        """

        if group_list:
            if self._group_ind is None:
                raise ValueError(f'Missing group column name')
            ngrams = generate_ngram_cluster(reader=self._reader,
                                            size=n,
                                            msg_position=self._msg_ind,
                                            group_position=self._group_ind,
                                            groups_list=group_list,
                                            stop_words=self._stop_words)
        else:
            ngrams = generate_ngram(reader=self._reader,
                                    size=n,
                                    msg_position=self._msg_ind,
                                    stop_words=self._stop_words)
        return ngrams

    def get_word_cloud(self,
                       background_color: str = 'white',
                       width: float = 6.4,
                       height: float = 4.8,
                       max_words: int = 200,
                       file_path: Optional[str] = None) -> None:
        """Plot a word cloud based on the ngrams

        :param background_color: Background color. Default is white.
        :type background_color: str
        :param width: Width of the figure. Default is 6.4.
        :type width: float
        :param height: Height of the figure. Default is 4.8.
        :type height: float
        :param max_words: Max of words in the word cloud. Default is 200.
        :type max_words: int
        :param file_path: Path to save the word cloud image. Default is None.
        :type file_path: Optional[str]
        """

        plot_word_cloud(ngram_dict=self.ngrams,
                        background_color=background_color,
                        width=width,
                        height=height,
                        max_words=max_words,
                        save_path=file_path)
