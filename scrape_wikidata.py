import pandas as pd
import requests
import sys
import time

from bs4 import BeautifulSoup
from tqdm import tqdm

def get_qid(tags):
    """Get the OSM entry's Wikidata identifier (QID) from the tags field in 
    amenities-vancouver.json.gz
    
    Args:
        tags (dict): contains the tags for the OSM entry
        
    Returns
        qid (str or None): QID if the entry is on Wikidata, else None
    """
    
    try:
        qid = tags['brand:wikidata']
    except:
        qid = None
        
    return qid

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
        Calling get_names with the reponse for McDonald's Wikidata page 
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
            description for the Wikidata entry - returns empty string if
            the Wikidata page does not have a description
    
    Example:
        Calling get_description with the reponse for McDonald's Wikidata page 
        returns 'American fast food restaurant chain'
    """
    
    soup = BeautifulSoup(wikidata_response.text, 'lxml')
    try:
        description = soup.find(property='og:description').get('content')
    except:
        description = ''
    return description

def main(input_file, osm_output_file, wikidata_output_file):
    """Scrape Wikidata entries for their names and descriptions.
        - write OSM data with a column for the Wikidata identifier (qid)
          to osm_output_file
        - write the qid, names and description of the Wikidata entries to
          wikidata_output_file

    Args:
        input_file (str):
            file provided for OSM, Photos, and Tours
            ('amenities-vancouver.json')

        osm_output_file (str):
            json output file containing the original OSM data with an
            additional column for the Wikidata identifier

        wikidata_output_file (str):
            json output file containing qid, names and descriptions of
            the Wikidata entries

    Returns:
        None

    Notes:
        - It takes approximately 1 to 2 seconds to scrape each Wikidata
          entry. Running the program with the provided OSM data may take
          a few minutes.
        - Upon receiving a bad request the program will stop scraping Wikidata
          and process the data it managed to retrieve.
    """
    
    # trailing data error - line adapted from
    # https://stackoverflow.com/questions/30088006/
    osm_data = pd.read_json(input_file, lines=True)

    osm_data['qid'] = osm_data['tags'].apply(get_qid)
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

    fetched_qids = list(wikidata_responses.keys())
    wikidata = pd.DataFrame(fetched_qids, columns=['qid'])
    
    # get names and descriptions for each Wikidata entry using qid
    wikidata['names'] = (
        wikidata['qid'].apply(lambda qid: get_names(wikidata_responses[qid]))
    )
    wikidata['description'] = (
        wikidata['qid'].apply(lambda qid: get_description(wikidata_responses[qid]))
    )

    # write osm_data with qid column to json
    osm_data.to_json(osm_output_file)

    # write wikidata qid, names and description to json
    wikidata.to_json(wikidata_output_file)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
