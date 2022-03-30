# Results

**Word Cloud and Count Plot for Wikidata Descriptions**<br>
![Word Cloud and Count Plot for Wikidata Descriptions](https://github.com/ys-lin14/cmpt-353-project/blob/master/screenshots/word_cloud_count_plot.PNG?raw=true)
<br><br>

**Visualization of Predictions**<br>
![Chain Restaurants and Non-Chain Restaurants](https://github.com/ys-lin14/cmpt-353-project/blob/master/screenshots/predictions.PNG?raw=true)
<br><br>

# General Process
**1. Data Extraction**<br>
![Wikidata for Starbucks](https://github.com/ys-lin14/cmpt-353-project/blob/master/screenshots/data_extraction.PNG?raw=true)
<br><br>

**2. Preprocessing**<br>
![Preprocessing OSM Data](https://github.com/ys-lin14/cmpt-353-project/blob/master/screenshots/data_preprocessing.PNG?raw=true)
<br><br>

![Wikidata Description for Swiss Chalet](https://github.com/ys-lin14/cmpt-353-project/blob/master/screenshots/text_processing.PNG?raw=true)
<br><br>

**3. Clustering**<br>
![Clustering Steps](https://github.com/ys-lin14/cmpt-353-project/blob/master/screenshots/flow_chart.PNG?raw=true)
<br><br>

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
    wordcloud

# Commands, Arguments and Order of Execution
**Main Pipeline (Linux)**

    python3 01-preprocess-osm-data.py data/amenities-vancouver.json.gz data/preprocessed-osm-data.json.gz
    python3 02-scrape-wikidata.py data/preprocessed-osm-data.json.gz data/wikidata.json
    python3 03-preprocess-wikidata.py data/wikidata.json data/preprocessed-wikidata.json
    python3 04-identify-chain-restaurants.py data/preprocessed-osm-data.json.gz data/wikidata.json data/preprocessed-wikidata.json data/chain-restaurant-qids.json
    python3 05-analyze-and-visualize.py 

**Main Pipeline (Windows)**

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
    


    
