import pandas as pd

def nonRestaurestaurant(): 
    return [
    'ATLAS_clean_room' ,'EVSE','Observation Platform' ,'Pharmacy','animal_shelter','arts_centre','atm','atm;bank',
    'bank','bench','bicycle_parking','bicycle_rental','bicycle_repair_station','car_rental','car_rep','car_sharing',
    'car_wash','casino','charging_station','childcare','chiropractor','cinema','clinic','clock','college',
    'community_centre','compressed_air','conference_centre','construction','courthouse','cram_school','dentist',
    'events_venue','family_centre','ferry_terminal','fire_station','first_aid','fountain','fuel','gambling','gym',
    'healthcare','hospital','housing co-op','hunting_stand','kindergarten','language_school','leisure','letter_box',
    'library','loading_dock','lobby','lounge','luggage_locker','marketplace','meditation_centre','monastery',
    'money_transfer','motorcycle_parking','motorcycle_rental','music_school','nightclub','nursery',
    'office|financial','park','parking','parking_entrance','parking_space','payment_terminal','pharmacy',
    'photo_booth','place_of_worship','playground','police','post_box','post_depot','post_office','prep_school',
    'public_bookcase','public_building','ranger_station','recycling','research_institute','safety',
    'sanitary_dump_station','school','science','scrapyard','seaplane terminal','shelter','shop|clothes','shower',
    'smoking_area','social_centre','social_facility','spa','storage','storage_rental','stripclub','studio',
    'taxi','telephone','theatre','toilets','townhall','training','trash','trolley_bay','university','vacuum_cleaner',
    'vending_machine','driving_school','veterinary','waste_basket','waste_disposal','waste_transfer_station',
    'water_point','watering_place','workshop''bureau_de_change','bus_station','internet_cafe',

    ]

def getdata(file):
    osm_data = pd.read_json(file, lines=True)
    columns=list(osm_data.columns)
    columns.remove('tags')
    return osm_data[columns].dropna()

def main(file):
    osm_data = getdata(file)
    restaurant=list(dict.fromkeys([i for i in amenity if i not in nonrestaurant]))
    clean_osm_data=osm_data[osm_data['amenity'].isin(restaurant)]
    clean_osm_data.to_json("clean_osm_data.JSON")




if __name__ == '__main__':
    file='data/amenities-vancouver.json.gz'
    main(file)