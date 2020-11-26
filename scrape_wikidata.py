import pandas as pd
import requests
import sys
import time

from bs4 import BeautifulSoup
from tqdm import tqdm

def scrape_wikidata(qid):
    """Request the identifier's Wikidata page 
    
    Args:
        qid (str): Wikidata identifier 
        
    Returns:
        wikidata_response (requests.models.Response): Wikidata response 
    """
    
    wikidata_url = (f'https://www.wikidata.org/wiki/{qid}')
    wikidata_response = requests.get(wikidata_url)
    return wikidata_response

def get_names(wikidata_response):
    """Get the names from the Wikidata response
    
    Args:
        wikidata_response (requests.models.Response): Wikidata response 
        
    Returns:
        names (list): names for the Wikidata entry
        
    Example:
        Calling get_names with the response from McDonald's (Q38076) Wikidata page 
        returns [
            'McDonald’s', 'McD', 'Mcdonalds', "McDonald's Corporation",
            "McDonald's Restaurant", "McDonald's", 'McDonald', "Mickey D's"
        ]
    """
    
    soup = BeautifulSoup(wikidata_response.text, 'lxml')
    names = [soup.find(property='og:title').get('content')]
    other_name_tags = soup.findAll(
        'li', 
        {'class': 'wikibase-entitytermsview-aliases-alias'}
    )
    names.extend(name_tag.text for name_tag in other_name_tags)
    return names

def get_description(wikidata_response):
    """Get the description from the Wikidata response
    
    Args:
        wikidata_response (requests.models.response): Wikidata response
        
    Returns:
        description (str): 
            description for the Wikidata entry - returns an empty string 
            if the Wikidata page does not have a description
    
    Example:
        Calling get_description with the reponse from McDonald's (Q38076) Wikidata 
        page returns 'American fast food restaurant chain'
    """
    
    soup = BeautifulSoup(wikidata_response.text, 'lxml')
    try:
        description = soup.find(property='og:description').get('content')
    except:
        description = ''
    return description

def main(input_file, output_file):
    """Scrape Wikidata entries for their names and descriptions.
        - write the qid, names and description of the Wikidata entries to
          output_file

    Args:
        input_file (str):
            json file from running preprocess_osm_data.py with the provided 
            'amenities-vancouver.json.gz'

        output_file (str):
            json output file containing qid, names and descriptions of
            the Wikidata entries

    Returns:
        None

    Notes:
        - It takes approximately 1 to 2 seconds to scrape each Wikidata
          entry. Running the program with the preprocessed OSM data may take
          a few minutes.
        - Upon receiving a bad request the program will stop scraping Wikidata
          and process the data it managed to retrieve.
    """
    
    osm_data = pd.read_json(input_file)
    unique_qids = osm_data['qid'].dropna().unique()

    # create dict with (qid, response) key value pairs
    wikidata_responses = {} 
    for qid in tqdm(unique_qids):
        # exception handling adapted from jouell's answer at
        # https://stackoverflow.com/questions/16511337/ 
        try:
            wikidata_response = scrape_wikidata(qid)
            wikidata_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # print the error and stop scraping if we get a bad HTTP response
            print("Http Error:", e)
            break
        
        wikidata_responses[qid] = wikidata_response
        time.sleep(1)

    # create dataframe with the qids that were successfully fetched
    fetched_qids = list(wikidata_responses.keys())
    wikidata = pd.DataFrame(fetched_qids, columns=['qid'])
    
    # get names and descriptions for each Wikidata entry using qid
    wikidata['names'] = (
        wikidata['qid'].apply(lambda qid: get_names(wikidata_responses[qid]))
    )
    wikidata['description'] = (
        wikidata['qid'].apply(lambda qid: get_description(wikidata_responses[qid]))
    )

    # write wikidata qid, names and description to json
    wikidata.to_json(output_file)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])