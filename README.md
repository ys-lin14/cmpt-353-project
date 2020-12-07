- required libraries
    bs4
        lxml
    folium
    gensim
    haversine
    matplotlib
    nltk 
    numpy
    pandas
    tqdm
    requests
    scipy
    seaborn
    sklearn
    sys
    time

- commands (and arguments)
    01-preprocess-osm-data.py data/amenities-vancouver.json.gz data/preprocessed-osm_data.json.gz
    02-scrape-wikidata.py data/preprocessed-osm_data.json.gz data/data/wikidata.json
    03-preprocess-wikidata.py data/wikidata.json data/preprocessed_wikidata.json
    04-identify-chain-restaurants.py data/preprocessed-osm-data.json.gz data/wikidata.json data/preprocessed-wikidata.json data/chain-restaurant-qids.json
    05-analyze-and-visualize.py 
    
- order of execution

- files produced/expected 

    