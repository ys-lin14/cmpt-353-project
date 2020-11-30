import numpy as np
import pandas as pd
import re

from sklearn.feature_extraction.text import CountVectorizer

def get_ngram_counts(documents, num_ngrams=10, ngram_range=(1, 1)):
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
            contains the top n-grams along with their counts in 'ngram' and
            'count' columns
    """
    
    vectorizer = CountVectorizer(
        lowercase=False, 
        max_features=num_ngrams,
        ngram_range=ngram_range
    )
    
    # number of documents (row) by number of grams (column)
    X = vectorizer.fit_transform(documents)
    ngrams = vectorizer.get_feature_names()
    document_ngram_df = pd.DataFrame(X.toarray(), columns=ngrams)
    ngram_counts = document_ngram_df.sum(axis=0).reset_index()
    ngram_counts.rename(columns={'index': 'ngram', 0: 'count'}, inplace=True)
    return ngram_counts   

def sort_ngram_counts(ngram_counts, ascending=False):
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

def get_sorted_ngram_counts(documents, num_ngrams=10, ngram_range=(1, 1), ascending=False):
    """Get n-grams sorted by their count

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

        ascending (bool): 
            determines whether the counts are sorted in ascending or descending
            order

    Returns:
        sorted_ngram_counts (dataframe):
            n-grams sorted by count
    """
    
    ngram_counts = get_ngram_counts(documents, num_ngrams, ngram_range)
    sorted_ngram_counts = sort_ngram_counts(ngram_counts, ascending)
    return sorted_ngram_counts

def get_match(pattern, text):
    """Get the regex match object for pattern from text
    
    Args:
        pattern (str): pattern to be matched
        
        text (str): Wikidata description
        
    Returns:
        match (regex match / None): 
            regex match object if pattern was found, else None
    """
    
    match = re.search(pattern, text)
    return match

def get_chain_restaurant_qids(chain_restaurant_wikidata):
    """Get a dictionary which maps chain restaurant qids to 1
    
    Args:
        chain_restaurant_wikidata (dataframe):
            Wikidata for chain restaurants 
        
    Returns:
        chain_restaurant_qids (dict):
            contains (qid, 1) key value pairs for qids associated
            with chain restaurants
    """
    
    num_chain_restaurant_qids = chain_restaurant_wikidata.shape[0]
    chain_restaurant_qids = dict(zip(
        chain_restaurant_wikidata['qid'], 
        np.ones(num_chain_restaurant_qids, dtype=int)
    ))
    return chain_restaurant_qids
    
def get_num_chain_restaurants(osm_data, chain_restaurant_qids):
    """Get the (estimated) number of chain restaurants from the OSM data
    using chain restaurant qids
    
    Args:
        osm_data (dataframe):
            OSM data preprocessed using preprocess_osm_data.py
        
    Returns:
        num_chain_restaurants (int):
            the number of chain restaurants within the OSM data
    """
    
    num_chain_restaurants = osm_data['qid'].map(chain_restaurant_qids).sum()
    num_chain_restaurants = int(num_chain_restaurants)
    return num_chain_restaurants

def num_to_long_df(num_chain_qids, num_chains, approach):
    """Create a dataframe using the number of chain restaurant qids 
    and chain restaurants 
    
    Args:
        num_chain_qids (int): 
            number of qids for chain restaurants 
        
        num_chains (int): 
            number of chain restaurants 
        
        approach (str): 
            whether the numbers were obtained from the 'regex' or
            'mixed' approach
        
    Returns:
        long_df (dataframe): 
            contains the number of chain restaurants and chain restaurant
            qids from the given approach
        
    Example:
        calling num_to_long_df with updated number of chain restaurant and
        chain restaurant qids from the mixed approach returns
        
            type         value    approach
        0   wikidata     45       mixed
        1   restaurant   746      mixed
    """
    
    data = {
        'wikidata': num_chain_qids,
        'restaurant': num_chains,
        'approach': approach
    }
    # index=[0] adapted from https://stackoverflow.com/questions/17839973/
    df = pd.DataFrame(data, index=[0])
    long_df = pd.melt(df, id_vars=['approach'], var_name='type')
    return long_df[['type', 'value', 'approach']]
