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
    
    plt.figure(figsize=(20, 10)) # adjust overall size of wordcloud
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def plot_word_counts(word_counts, wikidata_label):
    num_words = word_counts.shape[0]
    word_count_plot = sns.barplot(data=word_counts, x='word', y='count')
    word_count_plot.set(
        title=f'Top {num_words} Words in Wikidata {wikidata_label}', 
        xlabel='Word', 
        ylabel='Count'
    )
    xlabels = word_count_plot.get_xticklabels()
    word_count_plot.set_xticklabels(xlabels, rotation=30, ha='right')
    plt.show()
