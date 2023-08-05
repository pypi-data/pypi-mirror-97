__author__ = 'Gabriel Oliveira'
__version__ = '0.1.0'

import os
import csv
from typing import Tuple, Optional, Any


def get_column_index(header: list,
                     column_name: str) -> int:
    """Validate the existence of the columns in the file

    :param header: Columns name of the file.
    :type header: list
    :param column_name: Column name to validate.
    :type column_name: str
    :return: The index of the column.
    :rtype: int
    :raise ValueError: If header does not have column as index.
    """
    try:
        index = header.index(column_name)
        return index
    except ValueError:
        raise ValueError(f'File does not have "{column_name}" column.')


def read_data(path: str,
              message_column: str,
              group_column: Optional[str] = None,
              sep: str = '|',
              encoding: str = 'utf-8') -> Tuple[Any, int, Optional[int]]:
    """Read data file

    :param path: Path of file.
    :type path: str
    :param message_column: Name of message column.
    :type message_column: str
    :param group_column: Name of group column. Default is None.
    :type group_column: Optional[str]
    :param sep: The separator of columns. Default is '|'.
    :type sep: str
    :param encoding: File encoding. Default is 'utf-8'.
    :type encoding:  str
    :return: A tuple containing the reader of the file, the index of the
    message and of the group column (if exist).
    :rtype: Tuple[_reader, int, Optional[int]]
    :raise FileNotFoundError: If path does not exist.
    """
    if os.path.isfile(path):
        file = open(path, encoding=encoding)
        reader = csv.reader(file, delimiter=sep)
        header = next(reader)
        message_index = get_column_index(header=header,
                                         column_name=message_column)
        if group_column:
            group_index = get_column_index(header=header,
                                           column_name=group_column)
            return reader, message_index, group_index
        else:
            return reader, message_index, None
    else:
        raise FileNotFoundError(f"File at '{path}' not found")
