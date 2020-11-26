import pandas as pd
import sys

def get_tag_data(tags, tag_name):
    """Get the OSM entry's Wikidata identifier (QID) from the tags field in 
    amenities-vancouver.json.gz
    
    Args:
        tags (dict): contains the tags for the OSM entry
        tag_name (str): key for the tag data
        
    Returns
        tag_data (str or None): tag data if the tag_name is a valid key, else None
    """
    
    try:
        tag_data = tags[tag_name]
    except:
        tag_data = None
        
    return tag_data

def main(input_file, output_file):
    """Preprocess OSM data by filling in wikidata identifiers (qid)
    for OSM entries that have a Wikidata entry but are not associated with one.
        - write preprocessed OSM data to output_file

    Args:
        input_file (str):
            osm_output_file from scrape_wikidata.py - should include the data
            from amenities-vancouver.json.gz along with an additional column
            for qid
            
        output_file (str):
            json file in which some qids have been filled in
    """
    # trailing data error - line adapted from
    # https://stackoverflow.com/questions/30088006/
    osm_data = pd.read_json(input_file, read_lines=True)

    osm_data['qid'] = osm_data['tags'].apply(
        lambda tags: get_qid(tags, 'brand:wikidata')
    )
    
    has_qid = osm_data['qid'].notna()
    has_name = osm_data['name'].notna()

    # create dict with (name, qid) key value pairs - dict zip adapted from
    # Wouter Overmeire's answer at https://stackoverflow.com/questions/17426292/
    valid_name_qid = osm_data.loc[has_qid & has_name, ['name', 'qid']].copy()
    name_qid = dict(zip(valid_name_qid['name'], valid_name_qid['qid']))

    # fill in missing qids for OSM data that have a Wikidata entry
    osm_data['mapped_qid'] = osm_data['name'].map(name_qid)

    # set mapped_qid of OSM data that have a qid but do not have a name
    # equal to qid 
    osm_data.loc[has_qid & ~has_name, 'mapped_qid'] = (
        osm_data.loc[has_qid & ~has_name, 'qid']
    )

    # qid and mapped_qid for OSM data associated with a Wikidata entry should
    # be the same
    assert (
        all(osm_data.loc[has_qid, 'qid'] == osm_data.loc[has_qid, 'mapped_qid'])
    )

    # replace qid column values with mapped_qid
    preprocessed_osm_data = osm_data.drop(['qid'], axis=1)
    preprocessed_osm_data.rename(columns={'mapped_qid': 'qid'}, inplace=True)
    preprocessed_osm_data.to_json(output_file)
    
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
