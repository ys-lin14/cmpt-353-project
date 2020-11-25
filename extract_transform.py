import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

def get_word_counts(documents, max_words=10):
    # can add ngram_range parameter to get bigrams - max_ngram
    vectorizer = CountVectorizer(lowercase=False, max_features=max_words)
    
    # number of documents (row) by number of words (column)
    X = vectorizer.fit_transform(documents)
    words = vectorizer.get_feature_names()
    document_term_df = pd.DataFrame(X.toarray(), columns=words)
    word_counts = document_term_df.sum(axis=0).reset_index()
    word_counts.rename(columns={'index': 'word', 0: 'count'}, inplace=True)
    return word_counts   

def sort_word_counts(word_counts):
    # sort descending by word count
    sorted_word_counts = word_counts.sort_values(
        by=['count'],
        ascending=False
    )
    sorted_word_counts.reset_index(drop=True, inplace=True)
    return sorted_word_counts
