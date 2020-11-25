import matplotlib.pyplot as plt
import seaborn as sns

from wordcloud import WordCloud

def plot_wordcloud(text):
    """Plot a wordcloud - adapted from 
    https://github.com/amueller/word_cloud/blob/master/examples/simple.py
    
    Args:
        text (str): 
            preprocessed_names or preprocessed_descriptions combined
            into a single string
        
    Returns:
        None
    """
    
    # width and height appear to affect how sharp the words are
    wordcloud = WordCloud(
        width=2400, 
        height=1200,
        collocations=False # exclude bigrams
    ).generate(text)

    # adjust overall size of wordcloud
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def plot_ngram_counts(ngram_counts, title, xlabel):
    """Plot n-grams along with their counts

    Args:
        ngram_counts (dataframe):
            n-grams along with their counts in the columns 'ngram' and 'count'

        title (str):
            title of barplot for n-gram counts

    Returns:
        None
    """
    
    num_ngram = ngram_counts.shape[0]
    ngram_count_plot = sns.barplot(data=ngram_counts, x='ngram', y='count')
    ngram_count_plot.set(title=title, xlabel=xlabel, ylabel='Count')
    x_ticks = ngram_count_plot.get_xticklabels()
    ngram_count_plot.set_xticklabels(x_ticks, rotation=30, ha='right')
    plt.show()
