import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

def get_ngram_counts(documents, num_top_ngrams=10, ngram_range=(1, 1)):
    """Get the counts of the most frequent n-grams within a collection 
    of documents - the variable name ngram_range was taken from the 
    documentation for sklearn's CountVectorizer 
    
    Args:
        documents (series): 
            preprocessed names or description columns from
            preprocessed_wikidata.json 
            
        num_top_ngrams (int):
            number of top n-grams to be returned
            
        ngram_range (tuple):
            range of n-grams to be counted - (1, 1) returns single words
            and their counts, (1, 2) for single words and pairs of words, 
            (2, 2) for pairs of words, etc
        
    Returns:
        ngram_counts (dataframe): 
            contains the top n-grams along with their counts 
            in 'ngram' and 'count' columns
    """
    
    vectorizer = CountVectorizer(
        lowercase=False, 
        max_features=num_top_words,
        ngram_range=ngram_range
    )
    
    # number of documents (row) by number of grams (column)
    X = vectorizer.fit_transform(documents)
    ngrams = vectorizer.get_feature_names()
    document_ngram_df = pd.DataFrame(X.toarray(), columns=ngrams)
    ngram_counts = document_ngram_df.sum(axis=0).reset_index()
    ngram_counts.rename(columns={'index': 'ngram', 0: 'count'}, inplace=True)
    return ngram_counts   

def sort_ngram_counts(ngram_counts):
    """Sort n-grams by their count 
    
    Args:
        ngram_counts (dataframe): 
            n-grams along with their counts in the columns 'ngram' and 'count' 
            
        ascending (bool): 
            determines whether the counts are sorted in ascending or descending
            order
        
    Returns:
        sorted_ngram_counts (dataframe):
            n-grams sorted by count
    """
    
    sorted_ngram_counts = ngram_counts.sort_values(
        by=['count'],
        ascending=ascending
    )
    sorted_ngram_counts.reset_index(drop=True, inplace=True)
    return sorted_ngram_counts
