__author__ = 'Gabriel Oliveira'
__version__ = '0.1.1'

from typing import Optional

import matplotlib.pyplot as plt

from wordcloud import WordCloud


def plot_word_cloud(ngram_dict: dict,
                    background_color: str = 'white',
                    width: float = 6.4,
                    height: float = 4.8,
                    max_words: int = 200,
                    save_path: Optional[str] = None) -> None:
    """Generate image of the word cloud of the n-grams

    :param ngram_dict: Dictionary with n-grams and they frequency.
    :type ngram_dict: dict
    :param background_color: Background color. Default is 'white'.
    :type background_color: str
    :param width: Width of the figure. Default is 6.4
    :type width: float
    :param height: Height of the figure. Default is 4.8
    :type height: float
    :param max_words: Max of words in the word cloud. Default is 200.
    :type max_words: int
    :param save_path: Path to save the word cloud image. Default is None.
    :type save_path: Optional[str]
    """
    wc = WordCloud(background_color=background_color,
                   max_words=max_words,
                   height=1000,
                   width=1000).generate_from_frequencies(ngram_dict)
    plt.figure(figsize=(width, height))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    if save_path:
        wc.to_file(save_path)
