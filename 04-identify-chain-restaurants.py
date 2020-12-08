import numpy as np
import pandas as pd
import sys

from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import transform

def main(preprocessed_osm_data, raw_wikidata, preprocessed_wikidata, output_file):
    # load data
    osm_data = pd.read_json(preprocessed_osm_data)

    raw_wikidata = pd.read_json(raw_wikidata)
    preprocessed_wikidata = pd.read_json(preprocessed_wikidata)
    wikidata = raw_wikidata.merge(preprocessed_wikidata, on='qid')

    wikidata['name'] = wikidata['names'].apply(lambda names: names[0])
    descriptions = wikidata['preprocessed_description']

    # check for the words 'chain' and 'restaurant' in Wikidata descriptions
    contains_chain = wikidata['preprocessed_description'].apply(
        lambda description: transform.get_match('chain', description)
    ).notna()
    contains_restaurant = wikidata['preprocessed_description'].apply(
        lambda description: transform.get_match('restaurant', description)
    ).notna()

    contains_chain_and_restaurant = (contains_chain & contains_restaurant)

    # include entries that contain the words 'chain' and 'restaurant'
    chain_restaurant_wikidata = wikidata[contains_chain_and_restaurant]

    # calculate cosine similarities between each Wikidata description
    vectorizer = CountVectorizer(lowercase=False)
    document_term_matrix = vectorizer.fit_transform(descriptions)
    cosine_similarities = cosine_similarity(document_term_matrix)

    # get names of chain restaurants 
    chain_restaurant_names = chain_restaurant_wikidata['name'].values
    names = wikidata['name']

    Z = linkage(cosine_similarities, method='complete')
    clusters = fcluster(Z, t=3, criterion='maxclust')
    
    # create dataframe containing columns for name and cluster
    name_cluster = pd.DataFrame.from_dict(
        dict(zip(names, clusters)), 
        orient='index'
    ).reset_index().rename(columns={'index': 'name', 0:'cluster'})

    # find the cluster with the most chain restaurants 
    chain_restaurant_wikidata = chain_restaurant_wikidata.merge(name_cluster, on='name')
    chain_restaurant_cluster = chain_restaurant_wikidata['cluster'].value_counts().idxmax()

    is_within_chain_restaurant_cluster = (name_cluster['cluster'] == chain_restaurant_cluster)
    is_chain_restaurant = (contains_chain_and_restaurant | is_within_chain_restaurant_cluster)

    # include entries within the cluster with the most chain restaurants 
    updated_chain_restaurant_wikidata = wikidata[is_chain_restaurant]
    updated_chain_restaurant_qids = transform.get_chain_restaurant_qids(updated_chain_restaurant_wikidata)

    # map back to OSM data to get the updated number of chain restaurants
    updated_num_chain_restaurants = transform.get_num_chain_restaurants(
        osm_data, 
        updated_chain_restaurant_qids
    )

    # convert to dataframe and write to json
    final_chain_restaurant_qids = pd.DataFrame.from_dict(
        updated_chain_restaurant_qids, 
        orient='index'
    )
    final_chain_restaurant_qids.reset_index(inplace=True)
    final_chain_restaurant_qids.rename(
        columns={'index': 'qid', 0:'is_chain_restaurant'},
        inplace=True
    )
    final_chain_restaurant_qids.to_json(output_file)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
