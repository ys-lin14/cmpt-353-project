import folium
from folium.plugins import HeatMap
from haversine import haversine, Unit, haversine_vector
import pandas as pd

def make_matrix(location, size):
    return [location for i in range(size)]

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
    'water_point','watering_place','workshop''bureau_de_change','bus_station','internet_cafe', 'doctors',
    'dojo','bureau_de_change', 'boat_rental', 'workshop', 'drinking_water'

    ]
    

def main(file1, file2, location1, location2, dist):
    osm_data = pd.read_json(file1)
    
    # chain restaurant data using qid
    chain_qids=pd.read_json(file2)
    
    # merge osm_data and chain_qid to identify chain restaurants in 
    osm_data=osm_data.merge(chain_qids, how='left', on='qid')
    osm_data['is_chain_restaurant']=osm_data.is_chain_restaurant.fillna(0)
    
    # filter restaurants from non restaurant in osm_data
    amenity=osm_data['amenity']
    restaurant=list(dict.fromkeys([i for i in amenity if i not in nonRestaurestaurant()]))
    #print(restaurant)
    osm_data=osm_data[osm_data['amenity'].isin(restaurant)]
    
    size=osm_data.lat.size
    
        
    #convert locations list to matrix for haversine_vector(), distance calculation
    location1_matrix=make_matrix(location1, size)
    location2_matrix=make_matrix(location2, size)

    #distance between location 1 and osm_data locations
    osm_data['dist1']=haversine_vector(
        osm_data[['lat', 'lon']].values.tolist(), [location1 for i in range(size)], 
        Unit.KILOMETERS
    )

    #distance between location 2 and osm_data locations
    osm_data['dist2']=haversine_vector(
        osm_data[['lat', 'lon']].values.tolist(), [location2 for i in range(size)], 
        Unit.KILOMETERS
    )
    
    
    # number of chain restaurants with chosen distance of location 1
    dist1_and_chain=osm_data[(osm_data.dist1<dist)&(osm_data.is_chain_restaurant==1)].shape[0]
    
    # number of chain restaurants with chosen distance of location 2
    dist2_and_chain=osm_data[(osm_data.dist2<dist)&(osm_data.is_chain_restaurant==1)].shape[0]
    
    # number of non chain restaurants with chosen distance of location 1
    dist1_and_nonchain=osm_data[(osm_data.dist1<dist)&(osm_data.is_chain_restaurant==0)].shape[0]
    
    # number of non chain restaurants with chosen distance of location 2
    dist2_and_nonchain=osm_data[(osm_data.dist2<dist)&(osm_data.is_chain_restaurant==0)].shape[0]
    
    
   
    
    #Chi-Squared with the filtered data to compare the density of chain restaurants by two locations
    location = {
        'location 1': [dist1_and_nonchain, dist2_and_nonchain],
        'location 2': [dist1_and_chain, dist2_and_chain]
    }
    chi_squared=pd.DataFrame(location, 
        columns = [ 'location 1', 'location 2'],
        index=['chain restaurant', 'non chain restaurant']
    )
    print(chi_squared)
    
    
    # for map visualization
    
    # put a marker on location 1 and 2 on map
    m3=folium.Map(location=location2, zoom_start=100)
    folium.Marker(location1, popup='<b>Location 1</b>').add_to(m3)
    folium.Marker(location2, popup='<b>Location 2</b>').add_to(m3)
    
    
    # select only restauarnts with distance of your chosen distance
    within_distance=osm_data[(osm_data.dist2<dist)|(osm_data.dist1<dist)]
    chain_restaurant = within_distance[within_distance.is_chain_restaurant==1][["lat","lon"]].values
    non_chain_restaurant = within_distance[within_distance.is_chain_restaurant==0][["lat","lon"]].values
    
    
    # blue for restaurants within chosen distance of location 1
    for i in range(len(chain_restaurant)):
        folium.CircleMarker(chain_restaurant[i], radius=8, color='blue', fill=True).add_to(m3)
    

    # red for restaurants within chosen distance of location 2   
    for i in range(len(non_chain_restaurant)):
        folium.CircleMarker(non_chain_restaurant[i], radius=2, color='red', s=25, fill=True).add_to(m3)
        
    m3.save('map.html')
    display(m3)
    
    
    # For heat map visualization - with similar procedure
    m=folium.Map(location=location2, zoom_start=100)
    folium.Marker(location1, popup='<b>SFU Burnaby</b>').add_to(m)
    folium.Marker(location2, popup='<b>SFU Vancouver</b>').add_to(m)
    latlons = osm_data[["lat","lon"]].values
    HeatMap(latlons).add_to(m)
    m.save('heat_map.html')
    display(m)
    



if __name__ == '__main__':
    # default intializations
    file1='data/preprocessed-osm-data.json.gz'
    file2='data/chain-restaurant-qids.json'
    
    while True:
    
        flag=int(input("Choose:\n0 - to enter your own values\n1 - to use default values: \n"))
        
    
    
    
        if flag==0:

            print("Enter coordinations for location 1:\n")
            lat1=float(input("Enter latitude 1: "))
            lon1=float(input("Enter Longitude 1: "))


            print("Enter coordinations for location 2:\n")
            lat2=float(input("Enter latitude 2: "))
            lon2=float(input("Enter Longitude 2: "))

            dist=float(input("Enter the distance within location 1 and 2 you are interested in(km): "))

            location1 = [lat1,  lon1]
            location2 = [lat2,  lon2]

            print('\n\n\n')
            main(file1, file2, location1, location2, dist)
            break

        if flag==1:

            location1 = [49.2768,  -122.9180] #SFU Burnaby
            print('location 1(SFU Burnaby): ', location1)

            location2 = [49.284478, -123.112349]  #SFU Vancouver
            print('location 2(SFU Vancouver): ', location2)

            dist=5
            print('distance within location 1 and 2  interested in: ', dist,'km')

            print('\n\n\n')
            main(file1, file2, location1, location2, dist)
            break
        
        
    