import pandas as pd
import sys

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.utils import simple_preprocess

stopwords = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def remove_stopwords(tokens):
    """Remove words that do not contain any additional information 
    (nltk stopwords) from a list of words
    
    Args:
        tokens (list): list of words which may contain stopwords
        
    Returns:
        filtered_tokens (list): list of words without stopwords
    """
    
    filtered_tokens = [token for token in tokens if token not in stopwords]
    return filtered_tokens

def lemmatize_tokens(tokens):
    """Reduce words to their base (lemmatization) - the base words should
    be actual words
    
    Args:
        tokens (list): words
    
    Returns:
        lemmatized_tokens (list): lemmatized words
    """
    
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

def preprocess_text(text):
    """Preprocess text by tokenizing it, converting it to lowercase,
    removing punctuation along with stopwords and lemmatizing it
    
    Args:
        text (str): wikidata names or descriptions 
    
    Returns:
        preprocessed_tokens (list): 
            tokens that have been converted to lowercase, lemmatized and
            have had punctuation/stopwords removed

    Example:
        Calling preprocess_text with the description for Pizza Factory 
        (Q39054369):
        'chain of pizza restaurants' -> ['chain', 'pizza', 'restaurant']
    """
    
    preprocessed_tokens = simple_preprocess(text)
    preprocessed_tokens = remove_stopwords(preprocessed_tokens)
    preprocessed_tokens = lemmatize_tokens(preprocessed_tokens)
    return preprocessed_tokens

def main(input_file, output_file):
    """Preprocess Wikidata entry names and descriptions.
        - write preprocessed Wikidata to output_file

    Args:
        input_file (str):
            json file containing qid, names and descriptions of the Wikidata
            entries
        
        output_file (str):
            json file containing qid, preprocessed names and preprocessed
            descriptions of the Wikidata entries
        
    Returns:
        None
    """

    wikidata = pd.read_json(input_file)

    # convert list of names into string and preprocess
    wikidata['names'] = wikidata['names'].apply(' '.join)
    wikidata['name_tokens'] = wikidata['names'].apply(preprocess_text)

    wikidata['description_tokens'] = (
        wikidata['description'].apply(preprocess_text)
    )

    # convert description and name tokens back into strings
    wikidata['preprocessed_description'] = (
        wikidata['description_tokens'].apply(' '.join)
    )
    wikidata['preprocessed_names'] = (wikidata['name_tokens'].apply(' '.join))

    # get a subset of wikidata that contains qid along with the preprocessed
    # data
    preprocessed_columns = [
        'qid', 'preprocessed_names', 'preprocessed_description'
    ]
    preprocessed_wikidata = (
        wikidata[preprocessed_columns].copy()
    )

    preprocessed_wikidata.to_json(output_file)
    
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
