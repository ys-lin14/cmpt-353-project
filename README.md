# Required Libraries
    bs4
    folium
    gensim
    haversine
    lxml
    matplotlib
    nltk 
    numpy
    pandas
    tqdm
    requests
    scipy
    seaborn
    scikit-learn

# Commands, Arguments and Order of Execution
**Main Pipeline**

    01-preprocess-osm-data.py data/amenities-vancouver.json.gz data/preprocessed-osm-data.json.gz
    02-scrape-wikidata.py data/preprocessed-osm-data.json.gz data/wikidata.json
    03-preprocess-wikidata.py data/wikidata.json data/preprocessed-wikidata.json
    04-identify-chain-restaurants.py data/preprocessed-osm-data.json.gz data/wikidata.json data/preprocessed-wikidata.json data/chain-restaurant-qids.json
    05-analyze-and-visualize.py 

**Optional**

    data_exploration.ipynb
    data_exploration_2.ipynb 
    identify_chain_restaurants.ipynb
    identify_restaurants.ipynb

# Files Expected and Produced
**Main Pipeline**

    01-preprocess-osm-data.py
         input: amenities-vancouver.json.gz
        output: preprocessed-osm_data.json.gz

    02-scrape-wikidata.py
         input: preprocessed-osm_data.json.gz
        output: wikidata.json

    03-preprocess-wikidata.py 
         input: wikidata.json 
        output: preprocessed_wikidata.json

    04-identify-chain-restaurants.py 
         input: preprocessed-osm-data.json.gz, wikidata.json, preprocessed-wikidata.json
        output: chain-restaurant-qids.json

    05-analyze-and-visualize.py
         input: preprocessed-osm-data.json.gz, chain-restaurant-qids.json
        output: map.html, heat_map.html

**Optional**

    data_exploration.ipynb
         input: amenities-vancouver.json.gz
        output: None

    data_exploration_2.ipynb 
         input: preprocessed-wikidata.json
        output: None

    identify_chain_restaurants.ipynb
         input: preprocessed-osm-data.json.gz, wikidata.json, preprocessed-wikidata.json
        output: chain-restaurant-qids.json

    identify_restaurants.ipynb
         input: preprocessed-osm-data.json.gz, chain-restaurant-qids.json
        output: None

# Other - Project Planning / Notes / Report 
https://docs.google.com/document/d/1hRqKuATGqSuzJBPyZvFewi4v1Qc9qja8qKg3TIALynw/edit
    


    